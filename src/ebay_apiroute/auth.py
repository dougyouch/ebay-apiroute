"""Authentication for the generated eBay clients.

This file is written by hand: the generated clients extend these classes (through the
`base_class` entries in apis.yaml), so regenerating never touches it.
"""

import dataclasses
from collections.abc import Callable
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from apiroute import Client, RequestSpec

from ebay_apiroute.trading_version import TRADING_VERSION

Token = str | Callable[[], str]


class EbayAuth(Client):
    """OAuth for eBay's REST APIs.

        api = SellInventoryApi(token="v^1.1#i^1#...", marketplace_id="EBAY_US")
        api = SellInventoryApi(token=oauth.current_token, sandbox=True)

    token is an application or user access token, or a function returning the current one
    (so a refreshing OAuth helper can be passed directly). marketplace_id is sent as the
    X-EBAY-C-MARKETPLACE-ID header. sandbox=True uses eBay's sandbox hosts.
    """

    headers = {
        "Authorization": lambda self: f"Bearer {self.current_token()}" if self._token else None,
        "X-EBAY-C-MARKETPLACE-ID": lambda self: self.marketplace_id,
    }

    def __init__(
        self,
        token: Token | None = None,
        *,
        marketplace_id: str | None = None,
        sandbox: bool = False,
        **kwargs: Any,
    ):
        if sandbox and "base_url" not in kwargs and type(self)._config.base_url:
            kwargs["base_url"] = sandbox_url(type(self)._config.base_url)
        super().__init__(**kwargs)
        self._token = token
        self.marketplace_id = marketplace_id

    def current_token(self) -> str | None:
        return self._token() if callable(self._token) else self._token


class TradingAuth(Client):
    """Credentials for eBay's Trading API (SOAP).

        trading = TradingApi(token="AgAAAA...", app_id="MyApp-...", site_id=0)
        trading.get_item(body={"ItemID": "123456789"})

    The token (an Auth'n'Auth token, or a function returning one) goes in the envelope's
    RequesterCredentials header; eBay's SOAP endpoint also wants the call name, site,
    application ID and version in the query string.
    """

    def __init__(
        self,
        token: Token,
        *,
        app_id: str,
        site_id: int = 0,
        version: str = TRADING_VERSION,
        sandbox: bool = False,
        **kwargs: Any,
    ):
        if sandbox and "base_url" not in kwargs and type(self)._config.base_url:
            kwargs["base_url"] = sandbox_url(type(self)._config.base_url)
        super().__init__(**kwargs)
        self._token = token
        self.app_id = app_id
        self.site_id = site_id
        self.version = version

    def current_token(self) -> str:
        return self._token() if callable(self._token) else self._token

    def soap_header(self, operation: str) -> dict[str, Any]:
        return {"RequesterCredentials": {"eBayAuthToken": self.current_token()}}

    def on_request(self, request: RequestSpec) -> RequestSpec:
        query = [
            ("callname", request.operation),
            ("siteid", str(self.site_id)),
            ("appid", self.app_id),
            ("version", self.version),
            ("routing", "new"),
        ]
        return dataclasses.replace(request, params=[*request.params, *query])


def sandbox_url(url: str) -> str:
    """api.ebay.com -> api.sandbox.ebay.com (likewise apiz, apix and apim)."""
    parts = urlsplit(url)
    host = parts.netloc
    if host.endswith(".ebay.com") and ".sandbox." not in host:
        host = host.removesuffix(".ebay.com") + ".sandbox.ebay.com"
    return urlunsplit(parts._replace(netloc=host))
