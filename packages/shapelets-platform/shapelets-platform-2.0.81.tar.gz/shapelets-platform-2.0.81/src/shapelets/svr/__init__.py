from logging import warning
import subprocess
import os
import time
import sys

from requests import Session
from requests.auth import AuthBase
from rodi import Container, Services
from typing import Optional, Type, Union, TypeVar
from urllib.parse import urljoin

from . import app
from . import authn
from . import dataapps
from . import db
from . import execution
from . import groups
from . import mustang
from . import settings
from . import users
from . import telemetry

# Public APIs
from .authn import (
    IAuthService, UserAlreadyExists, InvalidLength,
    VerificationError, UnknownUser, InvalidUserName,
    Challenge, Addresses, gc_flow)
from .model import (
    DataAppProfile, FunctionProfile, GCPrincipalId,
    GroupAttributes, GroupField, GroupProfile,
    PrincipalId, ResolvedPrincipalId, SignedPrincipalId,
    UserAllFields, UserAttributes, UserField,
    UserId, UserProfile)

from .dataapps import IDataAppsService
from .execution import IExecutionService
from .groups import IGroupsService, InvalidGroupName
from .server import InProcServer, launch_in_process, run_dedicated
from .settings import *
from .users import IUsersService
from .utils import FlexBytes, crypto
from .telemetry import ITelemetryService, TelemetryService


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = f"Bearer {token}"

    def __call__(self, r):
        r.headers["Authorization"] = self.token
        return r


class PrefixedSession(Session):
    def __init__(self, prefix_url: str, *args, **kwargs):
        self.prefix_url = prefix_url
        super(PrefixedSession, self).__init__(*args, **kwargs)

    def set_authorization(self, token: str):
        self.auth = BearerAuth(token)

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(PrefixedSession, self).request(method, url, verify=False, *args, **kwargs)


def setup_http_server(cfg: Settings, tel: ITelemetryService, blocking: bool, pid_file: Optional[str] = None) -> Optional[InProcServer]:
    """
    Creates an HTTP server capable of hosting the UI and the APIs

    Parameters
    ----------
    cfg: Settings
        Configuration settings 

    blocking: bool
        Should the server block the main thread or run on the background

    Returns
    -------
    When the server is run in blocking mode, this code never returns.  However,
    when the server is not run in blocking mode, an instance of `InProcServer`
    is returned to stop gracefully the background instance.
    """
    # create the database
    db.setup_database(cfg.database)
    # create the application
    application = app.setup_app(cfg)
    # add settings to D.I. container
    application.services.add_instance(cfg, Settings)
    # add telemetry
    application.services.add_instance(tel, ITelemetryService)
    # full services for authn
    authn.setup_services(application.services)
    # users services
    users.setup_services(application.services)
    # groups services
    groups.setup_services(application.services)
    # data apps services
    dataapps.setup_services(application.services)
    # execution services
    execution.setup_services(application.services)
    # run in process, non main thread blocking
    if blocking:
        try:
            run_dedicated(application, cfg, pid_file)
        finally:
            exit()

    # return a instance of InProcServer
    return launch_in_process(application, cfg)


def setup_remote_client(cfg: Settings, tel: ITelemetryService) -> Services:
    """
    Creates a stack of services required to connect to an
    HTTP API front end.
    """
    container = Container()
    container.add_instance(cfg, Settings)
    container.add_instance(PrefixedSession(cfg.client.server_url), Session)
    container.add_instance(tel, ITelemetryService)
    authn.setup_remote_client(container)
    users.setup_remote_client(container)
    groups.setup_remote_client(container)
    dataapps.setup_remote_client(container)
    execution.setup_remote_client(container)
    return container.build_provider()


def setup_headless(cfg: Settings, tel: ITelemetryService) -> Services:
    """
    Creates a headless environment, where the services are running 
    fully in process, without going through an HTTP comms stack.
    """
    db.setup_database(cfg.database)
    container = Container()
    container.add_instance(cfg, Settings)
    container.add_instance(tel, ITelemetryService)
    authn.setup_services(container)
    users.setup_services(container)
    groups.setup_services(container)
    dataapps.setup_services(container)
    execution.setup_services(container)
    return container.build_provider()


class SharedState:
    __slots__ = ('__services', '__local_server', '__settings', '__telemetry')

    def __init__(self) -> None:
        self.__services = None
        self.__local_server = None
        self.__settings = Settings()
        self.__telemetry = TelemetryService(self.__settings)

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def telemetry(self) -> ITelemetryService:
        return self.__telemetry

    @property
    def services(self) -> Services:
        return self.__services

    @services.setter
    def services(self, value: Services):
        self.__services = value

    @property
    def local_server(self) -> Optional[InProcServer]:
        return self.__local_server

    @local_server.setter
    def local_server(self, value: InProcServer):
        self.__local_server = value


this = sys.modules[__name__]
this._state: SharedState = SharedState()


def _is_server_up(session: Session, retries: int = 10, wait_seconds: float = 0.3) -> bool:
    """
    Tries to connect with Shapelets Server
    """
    serverUp = False
    c = 0
    while not serverUp and c < retries:
        try:
            pong_response = session.get("api/ping")
            pong_response.raise_for_status()
            serverUp = pong_response.text == "pong"
        except:
            c += 1
            time.sleep(wait_seconds)

    return serverUp


def initialize_svr(server_mode: Optional[ServerModeType] = None, **kwargs):
    # resolve settings from files and environment.
    settings = this._state.settings
    telemetry = this._state.telemetry
    server_mode = server_mode or settings.client.server_mode

    if server_mode == 'out-of-process':
        # now, build a stack of proxies to remote services
        this._state.services = setup_remote_client(settings, telemetry)
    elif server_mode == 'standalone':
        # run the server in standalone mode, set blocking param to True
        # the program terminates after this call
        setup_http_server(settings, telemetry, True, kwargs.get('pid_file', None))

    elif server_mode == 'in-process':
        # make sure the client will point to the in-proc server
        settings.client = settings.client.copy(update={
            'host': settings.server.host,
            'port': settings.server.port
        })
        # run the server in the same process
        this._state.local_server = setup_http_server(settings, telemetry, False)
        # build the proxies
        this._state.services = setup_remote_client(settings, telemetry)
    else:
        # run in headless mode
        this._state.services = setup_headless(settings, telemetry)

    if server_mode != 'headless':
        # Ping the server to ensure it is running
        session = this._state.services.get(Session)

        # check the server is running and reachable
        server_up = _is_server_up(session, 10 if server_mode == 'in-process' else 1)

        if not server_up and server_mode == 'out-of-process':
            # using sys executable to this code works with virtual environments
            args = [sys.executable, '-m', 'shapelets', 'server', 'run']
            log_file = os.path.join(os.getcwd(), 'shapelets_server.log')

            with open(log_file, "wb") as outfile:
                params = {
                    'cwd': os.getcwd(),
                    'close_fds': True,
                    'stderr': outfile,
                    'stdout': outfile,
                }

                if os.name == 'nt':
                    params['creationflags'] = subprocess.CREATE_NO_WINDOW
                else:
                    params['start_new_session'] = True

                process = subprocess.Popen(args, **params)
                print(f'Server process launched with pid {process.pid}.  Log file {log_file}')
                if os.name == 'nt':
                    print(f'You may stop the process by executing: taskkill /F /PID {process.pid}')

            server_up = _is_server_up(session)

        if not server_up:
            raise RuntimeError(f"No timely response from {settings.client.server_url}")


T = TypeVar("T", covariant=True)


def get_service(desired_type: Union[Type[T], str]) -> T:
    if desired_type == Settings:
        return this._state.settings

    if desired_type == ITelemetryService:
        return this._state.telemetry

    if this._state.services is None:
        initialize_svr()

    return this._state.services.get(desired_type)


def get_service_optional(desired_type: Union[Type[T], str]) -> Optional[T]:
    try:
        return get_service(desired_type)
    except:
        return None


__all__ = [
    'get_service', 'get_service_optional', 'initialize_svr'
]

# public classes, services accessible through get_service
__all__ += [
    'IAuthService', 'UserAlreadyExists', 'InvalidLength',
    'VerificationError', 'UnknownUser', 'InvalidUserName',
    'Challenge', 'Addresses', 'gc_flow',
    'DataAppProfile', 'FunctionProfile', 'GCPrincipalId',
    'GroupAttributes', 'GroupField', 'GroupProfile',
    'PrincipalId', 'ResolvedPrincipalId', 'SignedPrincipalId',
    'UserAllFields', 'UserAttributes', 'UserField',
    'UserId', 'UserProfile',
    'IDataAppsService',
    'IExecutionService',
    'IGroupsService',
    'InvalidGroupName',
    'InProcServer', 'launch_in_process', 'run_dedicated',
    'IUsersService',
    'FlexBytes',
    'ITelemetryService'
]

# modules exported as a whole
__all__ += ['crypto', 'mustang']

# export all setting classes
__all__ += settings.__all__
