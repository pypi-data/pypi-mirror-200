import os
from typing import Any

import requests
from requests import Response, Session

from patterns.cli.config import (
    read_devkit_config,
    CliConfig,
    write_devkit_config,
    AuthServer,
)
from patterns.cli.services.output import abort, abort_on_error

API_BASE_URL = os.environ.get(
    "PATTERNS_API_URL",
    "https://api-production.patterns.app/",
)

AUTH_TOKEN_ENV_VAR = "PATTERNS_AUTH_TOKEN"
AUTH_TOKEN_PREFIX = "JWT"

PUBLIC_API_BASE_URL = "api/v1"

s = requests.Session()
s.headers["Accept"] = "application/json"


def _get_api_session() -> Session:
    if "Authorization" not in s.headers:
        auth_token = _get_auth_token()
        s.headers["Authorization"] = f"{AUTH_TOKEN_PREFIX} {auth_token}"
    return s


def reset_session_auth():
    s.headers.pop("Authorization", None)


def get_auth_server() -> AuthServer:
    with abort_on_error("Failed getting the auth server"):
        resp = requests.get(build_url(API_BASE_URL, Endpoints.TOKEN_AUTHSERVER))
        resp.raise_for_status()
        return AuthServer(**resp.json())


def _get_auth_token(base_url: str = API_BASE_URL) -> str:
    override = os.environ.get(AUTH_TOKEN_ENV_VAR)
    if override:
        return override

    cfg = read_devkit_config()
    if not cfg.token:
        abort("You must be logged in to use this command. Run [code]patterns login")

    with abort_on_error("Failed verifying auth token"):
        resp = requests.post(
            build_url(base_url, Endpoints.TOKEN_VERIFY), json={"token": cfg.token}
        )
    if resp.status_code == 401:
        if cfg.refresh:
            cfg = _refresh_token(cfg)
    else:
        resp.raise_for_status()
    return cfg.token


def _refresh_token(cfg: CliConfig) -> CliConfig:
    auth_server = cfg.auth_server
    if not auth_server or not cfg.refresh:
        abort("Not logged in\n[info]You can log in with [code]patterns login")

    with abort_on_error("Failed to refresh access token"):
        resp = requests.post(
            f"https://{auth_server.domain}/oauth/token",
            data={
                "client_id": auth_server.devkit_client_id,
                "refresh_token": cfg.refresh,
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()

    cfg.token = resp.json()["access_token"]
    write_devkit_config(cfg)

    return cfg


def get_json(
    path: str,
    params: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Any:
    resp = get(path, params, session, base_url, **kwargs)
    resp.raise_for_status()
    return resp.json()


def get(
    path: str,
    params: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Response:
    session = session or _get_api_session()
    resp = session.get(build_url(base_url, path), params=params or {}, **kwargs)
    resp.raise_for_status()
    return resp


def post_for_json(
    path: str,
    json: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Any:
    resp = post(path, json, session, base_url, **kwargs)
    resp.raise_for_status()
    return resp.json()


def post(
    path: str,
    json: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Response:
    session = session or _get_api_session()
    resp = session.post(build_url(base_url, path), json=json or {}, **kwargs)
    resp.raise_for_status()
    return resp


def delete(
    path: str,
    params: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Response:
    session = session or _get_api_session()
    resp = session.delete(build_url(base_url, path), params=params or {}, **kwargs)
    resp.raise_for_status()
    return resp


def patch(
    path: str,
    json: dict = None,
    session: Session = None,
    base_url: str = API_BASE_URL,
    **kwargs,
) -> Response:
    session = session or _get_api_session()
    resp = session.patch(build_url(base_url, path), json=json or {}, **kwargs)
    resp.raise_for_status()
    return resp


def build_url(base_url: str, url: str) -> str:
    return "/".join((base_url.rstrip("/"), url.lstrip("/")))


class Endpoints:
    TOKEN_CREATE = "auth/jwt/create"
    TOKEN_AUTHSERVER = f"{PUBLIC_API_BASE_URL}/auth/jwt/authserver"
    TOKEN_VERIFY = f"{PUBLIC_API_BASE_URL}/auth/jwt/verify"
    ACCOUNTS_ME = f"{PUBLIC_API_BASE_URL}/accounts/me"
    ORGANIZATIONS_LIST = f"{PUBLIC_API_BASE_URL}/organizations"
    COMPONENTS_CREATE = f"{PUBLIC_API_BASE_URL}/marketplace/components/versions"

    @classmethod
    def organization_by_slug(cls, slug: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/organizations/slug/{slug}"

    @classmethod
    def organization_by_id(cls, organization_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/organizations/{organization_uid}"

    @classmethod
    def webhooks_list(cls, graph_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graphs/{graph_uid}/webhooks"

    @classmethod
    def graphs_list(cls, organization_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/organizations/{organization_uid}/graphs"

    @classmethod
    def graphs_latest(cls, graph_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graphs/{graph_uid}/latest"

    @classmethod
    def graph_update(cls, graph_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graphs/{graph_uid}"

    @classmethod
    def graph_version_download(cls, graph_version_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graph_versions/{graph_version_uid}/zip"

    @classmethod
    def graph_delete(cls, graph_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graphs/{graph_uid}"

    @classmethod
    def component_download(cls, organization: str, component: str, version: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/marketplace/components/{organization}/{component}/{version}/zip"

    @classmethod
    def component_update(cls, graph_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/marketplace/components/graph/{graph_uid}"

    @classmethod
    def graph_by_slug(cls, organization_uid: str, slug: str) -> str:
        return (
            f"{PUBLIC_API_BASE_URL}/organizations/{organization_uid}/graphs/slug/{slug}"
        )

    @classmethod
    def graph_version_by_id(cls, graph_version_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graph_versions/{graph_version_uid}"

    @classmethod
    def graph_version_create(cls, organization_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/organizations/{organization_uid}/graph_versions"

    @classmethod
    def trigger_node(cls, graph_uid: str, node_id: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/graphs/{graph_uid}/nodes/{node_id}/trigger"

    @classmethod
    def org_secrets(cls, organization_uid: str) -> str:
        return f"{PUBLIC_API_BASE_URL}/organizations/{organization_uid}/secrets"
