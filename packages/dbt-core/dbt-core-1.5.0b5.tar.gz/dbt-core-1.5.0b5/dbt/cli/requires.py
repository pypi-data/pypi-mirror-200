import dbt.tracking
from dbt.version import installed as installed_version
from dbt.adapters.factory import adapter_management, register_adapter
from dbt.flags import set_flags, get_flag_dict
from dbt.cli.flags import Flags
from dbt.config import RuntimeConfig
from dbt.config.runtime import load_project, load_profile, UnsetProfile
from dbt.events.functions import setup_event_logger, fire_event, LOG_VERSION
from dbt.events.types import (
    CommandCompleted,
    MainReportVersion,
    MainReportArgs,
    MainTrackingUserState,
)
from dbt.events.helpers import get_json_string_utcnow
from dbt.exceptions import DbtProjectError
from dbt.parser.manifest import ManifestLoader, write_manifest
from dbt.profiler import profiler
from dbt.tracking import active_user, initialize_from_flags, track_run
from dbt.utils import cast_dict_to_dict_of_strings, ExitCodes

from click import Context
from click.exceptions import ClickException
from functools import update_wrapper
import time
import traceback


class HandledExit(ClickException):
    def __init__(self, result, success, exit_code: ExitCodes) -> None:
        self.result = result
        self.success = success
        self.exit_code = exit_code

    def show(self):
        pass


class UnhandledExit(ClickException):
    exit_code = ExitCodes.UnhandledError.value

    def __init__(self, exception: Exception, message: str) -> None:
        self.exception = exception
        self.message = message

    def format_message(self) -> str:
        return self.message


def preflight(func):
    def wrapper(*args, **kwargs):
        ctx = args[0]
        assert isinstance(ctx, Context)
        ctx.obj = ctx.obj or {}

        # Flags
        flags = Flags(ctx)
        ctx.obj["flags"] = flags
        set_flags(flags)

        # Tracking
        initialize_from_flags(flags.SEND_ANONYMOUS_USAGE_STATS, flags.PROFILES_DIR)
        ctx.with_resource(track_run(run_command=flags.WHICH))

        # Logging
        # N.B. Legacy logger is not supported
        callabcks = ctx.obj.get("callbacks", [])
        setup_event_logger(flags=flags, callbacks=callabcks)

        # Now that we have our logger, fire away!
        fire_event(MainReportVersion(version=str(installed_version), log_version=LOG_VERSION))
        flags_dict_str = cast_dict_to_dict_of_strings(get_flag_dict())
        fire_event(MainReportArgs(args=flags_dict_str))

        # Deprecation warnings
        flags.fire_deprecations()

        if active_user is not None:  # mypy appeasement, always true
            fire_event(MainTrackingUserState(user_state=active_user.state()))

        # Profiling
        if flags.RECORD_TIMING_INFO:
            ctx.with_resource(profiler(enable=True, outfile=flags.RECORD_TIMING_INFO))

        # Adapter management
        ctx.with_resource(adapter_management())

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def postflight(func):
    def wrapper(*args, **kwargs):
        ctx = args[0]
        start_func = time.perf_counter()
        success = False

        try:
            result, success = func(*args, **kwargs)
        except Exception as e:
            raise UnhandledExit(e, message=traceback.format_exc())
        finally:
            fire_event(
                CommandCompleted(
                    command=ctx.command_path,
                    success=success,
                    completed_at=get_json_string_utcnow(),
                    elapsed=time.perf_counter() - start_func,
                )
            )

        if not success:
            raise HandledExit(
                result=result,
                success=success,
                exit_code=ExitCodes.ModelError.value,
            )

        return (result, success)

    return update_wrapper(wrapper, func)


# TODO: UnsetProfile is necessary for deps and clean to load a project.
# This decorator and its usage can be removed once https://github.com/dbt-labs/dbt-core/issues/6257 is closed.
def unset_profile(func):
    def wrapper(*args, **kwargs):
        ctx = args[0]
        assert isinstance(ctx, Context)

        if ctx.obj.get("profile") is None:
            profile = UnsetProfile()
            ctx.obj["profile"] = profile

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def profile(func):
    def wrapper(*args, **kwargs):
        ctx = args[0]
        assert isinstance(ctx, Context)

        if ctx.obj.get("profile") is None:
            flags = ctx.obj["flags"]
            # TODO: Generalize safe access to flags.THREADS:
            # https://github.com/dbt-labs/dbt-core/issues/6259
            threads = getattr(flags, "THREADS", None)
            profile = load_profile(
                flags.PROJECT_DIR, flags.VARS, flags.PROFILE, flags.TARGET, threads
            )
            ctx.obj["profile"] = profile

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def project(func):
    def wrapper(*args, **kwargs):
        ctx = args[0]
        assert isinstance(ctx, Context)

        if ctx.obj.get("project") is None:
            # TODO: Decouple target from profile, and remove the need for profile here:
            # https://github.com/dbt-labs/dbt-core/issues/6257
            if not ctx.obj.get("profile"):
                raise DbtProjectError("profile required for project")

            flags = ctx.obj["flags"]
            project = load_project(
                flags.PROJECT_DIR, flags.VERSION_CHECK, ctx.obj["profile"], flags.VARS
            )
            ctx.obj["project"] = project

            if dbt.tracking.active_user is not None:
                project_id = None if project is None else project.hashed_name()

                dbt.tracking.track_project_id({"project_id": project_id})

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def runtime_config(func):
    """A decorator used by click command functions for generating a runtime
    config given a profile and project.
    """

    def wrapper(*args, **kwargs):
        ctx = args[0]
        assert isinstance(ctx, Context)

        req_strs = ["profile", "project"]
        reqs = [ctx.obj.get(req_str) for req_str in req_strs]

        if None in reqs:
            raise DbtProjectError("profile and project required for runtime_config")

        config = RuntimeConfig.from_parts(
            ctx.obj["project"],
            ctx.obj["profile"],
            ctx.obj["flags"],
        )

        ctx.obj["runtime_config"] = config

        if dbt.tracking.active_user is not None:
            adapter_type = (
                getattr(config.credentials, "type", None)
                if hasattr(config, "credentials")
                else None
            )
            adapter_unique_id = (
                config.credentials.hashed_unique_field()
                if hasattr(config, "credentials")
                else None
            )

            dbt.tracking.track_adapter_info(
                {
                    "adapter_type": adapter_type,
                    "adapter_unique_id": adapter_unique_id,
                }
            )

        return func(*args, **kwargs)

    return update_wrapper(wrapper, func)


def manifest(*args0, write=True, write_perf_info=False):
    """A decorator used by click command functions for generating a manifest
    given a profile, project, and runtime config. This also registers the adaper
    from the runtime config and conditionally writes the manifest to disc.
    """

    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            ctx = args[0]
            assert isinstance(ctx, Context)

            req_strs = ["profile", "project", "runtime_config"]
            reqs = [ctx.obj.get(dep) for dep in req_strs]

            if None in reqs:
                raise DbtProjectError("profile, project, and runtime_config required for manifest")

            runtime_config = ctx.obj["runtime_config"]
            register_adapter(runtime_config)

            # a manifest has already been set on the context, so don't overwrite it
            if ctx.obj.get("manifest") is None:
                manifest = ManifestLoader.get_full_manifest(
                    runtime_config, write_perf_info=write_perf_info
                )

                ctx.obj["manifest"] = manifest
                if write and ctx.obj["flags"].write_json:
                    write_manifest(manifest, ctx.obj["runtime_config"].target_path)

            return func(*args, **kwargs)

        return update_wrapper(wrapper, func)

    # if there are no args, the decorator was used without params @decorator
    # otherwise, the decorator was called with params @decorator(arg)
    if len(args0) == 0:
        return outer_wrapper
    return outer_wrapper(args0[0])
