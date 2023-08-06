import os

from typing import Optional
from typing_extensions import Literal
from requests import Session

from .svr import (
    gc_flow, get_service, get_service_optional, defaults,
    crypto,
    UserAttributes, IAuthService, Settings, IAuthService,
    PrefixedSession)

EnterpriseLoginType = Literal['azure', 'linkedin', 'google', 'github']


def forget_me():
    """
    Forgets credentials stored in configuration files 
    """
    defaults(signed_token=None)


def login(*,
          authn_provider: Optional[EnterpriseLoginType] = None,
          user_name: Optional[str] = None,
          password: Optional[str] = None,
          remember_me: bool = True,
          user_settings: Optional[Settings] = None):
    """
    Login to Shapelets.

    This function is quite versatile and provides multiple methods of authentication. 

    When `authn_provider` is set, it will take preference over user name / password 
    combinations, even when found in the environment variables.  When login through 
    an external authentication provider for the very first time, a user will be 
    automatically created using the information shared by the authentication
    provider.

    If `authn_provider` is left unset, the code will try to log in using an user name 
    and password combination.  This information can be set directly as parameters, 
    through environment variables or by configuration files.  The recommended 
    method is to use environment variables to avoid exposing plain passwords.  Bear 
    in mind the credentials should have been created beforehand.

    If no external authentication or no user name / password combination is found, 
    the system will try to login the user using a previous login. 

    Parameters
    ----------
    authn_provider: optional, one of `azure`, `linkedin`, `google`, `github`
        Determines which external authentication provider should be used.

    user_name: optional, string 
        User name.  The preferred method for setting this value is through 
        the environment variable `SHAPELETS_CLIENT__USERNAME`

    password: optional, string 
        Password associated with `user_name`.  The preferred method for 
        setting this value is through the environment variable 
        `SHAPELETS_CLIENT__PASSWORD`

    remember_me: optional, bool, defaults to True
        Upon a successful login, stores the credentials in the default 
        user configuration file.  

    user_settings: optional, Settings, defaults to None
        Optional user settings.

    """

    settings = user_settings or get_service(Settings)
    auth_svc = get_service(IAuthService)
    signed_token: Optional[str] = None

    if authn_provider is not None:
        if not auth_svc.available(authn_provider):
            raise RuntimeError(f"Authentication flow for {authn_provider} is not available at the moment.")

        id = settings.telemetry.id.hex
        addresses = auth_svc.compute_addresses(authn_provider, id)
        gc_principal_id, user_details = gc_flow(addresses)
        signed_principal = auth_svc.auth_token(gc_principal_id, user_details)
        signed_token = signed_principal.to_token()

    else:
        user_name: str = user_name or os.environ.get('SHAPELETS_CLIENT__USERNAME', None)
        password: str = password or os.environ.get('SHAPELETS_CLIENT__PASSWORD', None)

        if user_name is not None and password is not None:
            challenge = auth_svc.generate_challenge(user_name)
            token = crypto.sign_challenge(challenge.salt, challenge.nonce, password.encode('ascii'))
            signed_principal = auth_svc.verify_challenge(user_name, challenge.nonce, token)
            signed_token = signed_principal.to_token()
        else:
            signed_token = settings.client.signed_token
            if signed_token is not None:
                if not auth_svc.verify(signed_token):
                    defaults(signed_token=None)  # Remove it from file
                    raise RuntimeError("Invalid cached credentials.  Please login again.")

    if signed_token is None:
        raise RuntimeError("No login credentials.")

    if remember_me:
        defaults(signed_token=signed_token)

    session: PrefixedSession = get_service_optional(Session)
    if session is not None:
        session.set_authorization(signed_token)


def register(user_name: str, password: str, user_details: Optional[UserAttributes] = None, also_login: bool = True, remember_me: bool = True, force: bool = False):
    """
    Registers a new user in Shapelets

    Parameters
    ----------
    user_name: str, required
        New user name.  This name should be unique in the system

    password: str, required
        Password associated with the new user 

    user_details: UserAttributes, optional
        User profile

    also_login: bool, defaults to True 
        Executes a login right after the registration

    remember_me: bool, defaults to True 
        Only used if `also_login` is set

    force: bool, defaults to False 
        Set this flag to overwrite the user attributes if the user already exists
    """
    auth_svc = get_service(IAuthService)
    if auth_svc.user_name_exists(user_name):
        if force:
            result = auth_svc.remove_user(user_name)
            if not result:
                raise ValueError("Unable to remove user name")
        else:
            raise ValueError(
                "User name already exists. To force registration with new UserAttributes, set flag force to True.")

    salt = crypto.generate_salt()
    pk = crypto.derive_verify_key(salt, password.encode('ascii'))
    if not auth_svc.register(user_name, salt, pk, user_details):
        raise RuntimeError("Unable to register a new user")

    if also_login:
        login(user_name=user_name, password=password, remember_me=remember_me)

def unregister(user_name: str):
    """
    Unregisters an existing user in Shapelets

    Parameters
    ----------
    user_name: str, required
        Existing user name.
    """
    auth_svc = get_service(IAuthService)
    if auth_svc.user_name_exists(user_name):
        result = auth_svc.remove_user(user_name)
        if not result:
            raise ValueError("Error happens while removing user name")
    else:
        raise ValueError("User does not exist. Unable to unregister user name")