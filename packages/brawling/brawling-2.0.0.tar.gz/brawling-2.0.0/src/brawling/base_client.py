from typing import Union, Any, Iterable
from urllib.parse import quote_plus
from dataclasses import dataclass

from .exceptions import *
from .__version__ import __version__

import re
import logging
from datetime import timedelta
from pathlib import Path
from difflib import SequenceMatcher

try:
    from requests_cache import CachedSession
    CACHE_ENABLED = True
except ModuleNotFoundError:
    CACHE_ENABLED = False

try:
    import aiohttp
    import asyncio
    HAS_AIOHTTP = True
except (ModuleNotFoundError, ImportError):
    HAS_AIOHTTP = False

try:
    from aiohttp_client_cache import CachedSession as CachedAiohttpSession, SQLiteBackend as AIOSQLiteBackend
    HAS_ASYNC_CACHE = True
except (ModuleNotFoundError, ImportError):
    HAS_ASYNC_CACHE = False

from requests import Session
from .models import BaseModel, SoloBattle, TeamBattle, DuelsBattle
from .util import BrawlerID

@dataclass
class ErrorResponse:
    error: APIException

USER_AGENT = f"brawling/{__version__}"

__all__ = [
    "ErrorResponse",
    "BaseClient",
    "BaseSyncClient",
    "BaseAsyncClient",
    "AuthTokenMixin"
]

# self._headers = {"Authorization": f"Bearer {self._parse_token(token)}", "User-Agent": USER_AGENT}

class BaseClient:
    """Base client for both sync + async clients"""
    def __init__(self, base_url: str, strict_errors: bool, caching: bool) -> None:
        logging.basicConfig()
        self._logger = logging.getLogger('brawling')
        self._logger.propagate = True
        self._debug(False)
        self._base = base_url
        self._strict_errors = strict_errors
        self._caching = caching
        self._bid_cache = {}

    def _debug(self, debug: bool):
        """Toggle debug mode on/off"""

        self._logger.setLevel(logging.DEBUG if debug else logging.WARNING)

    def _url(self, path: str):
        """Concatenate path to base URL"""

        return self._base + (path if path.startswith("/") else ("/" + path))

    def _verify_tag(self, tag: str):
        if not tag.startswith('#'):
            tag = '#' + tag

        regex = re.compile(r"(#)[0289CGJLPOQRUVY]{3,}", re.IGNORECASE | re.MULTILINE)
        match = regex.match(tag)
        if not match:
            return InvalidTag("Invalid tag", "Incorrect tag was provided")

        return match.group().upper()

    def _unwrap_list(self, json_list, cls: BaseModel):
        return [cls.from_json(x) for x in json_list]

    def _exc_handler(self, code: int, exc_json: dict):
        return generate_exception(code, exc_json.get("reason", ''), exc_json.get("message", ''))

    def _exc_wrapper(self, exc: Exception) -> ErrorResponse:
        """Either raise or return an `ErrorResponse` depending on `strict_errors`"""
        if self._strict_errors:
            raise exc
        else:
            return ErrorResponse(exc)

    def _parse_battles(self, battles: list) -> list[BaseModel]:
        out = []

        for b in battles:
            if 'players' not in b['battle']:
                out.append(TeamBattle.from_json(b))
            else:
                if 'brawlers' in b['battle']['players'][0]:
                    out.append(DuelsBattle.from_json(b))
                else:
                    out.append(SoloBattle.from_json(b))

        # most recent battles first
        out.sort(key=lambda x: x.battle_time, reverse=True)

        return out

    def _add_headers(self, headers: dict):
        """Override this to add HTTP headers, see AuthTokenMixin"""
        pass

    def __repr__(self) -> str:
        return f"<{type(self).__name__}(base={self._base}, strict_errors={self._strict_errors}, cachhing={self._caching})>"

    def _brawler_id(self, bid: str | int | BrawlerID) -> str:
        if isinstance(bid, BrawlerID):
            return str(bid.value)

        val = str(bid).upper()
        if val.isdigit():
            return val

        if not self._bid_cache:
            return None

        if val in self._bid_cache:
            return self._bid_cache[val]

        # not found
        success, value = self._match_name(val, self._bid_cache)

        if success:
            return self._bid_cache[value]
        else:
            raise ValueError(f"Failed to find brawler by name, closest match: {value}")

    def _match_name(self, val: str, table: Iterable[str]) -> tuple[bool, str]:
        closest = (0, None)
        for name in table:
            match = SequenceMatcher(lambda x: x in " \t-.", name, val).ratio()
            if match > closest[0]:
                closest = (match, name)

        if closest[0] == 1:
            return True, table[closest[1]]

        return False, closest[1]

    def flush_brawler_cache(self):
        self._bid_cache = {}

class BaseSyncClient(BaseClient):
    """Base client for all synchronous clients"""
    def __init__(self, base_url: str, strict_errors: bool = True, caching: bool = False) -> None:
        super().__init__(base_url, strict_errors, caching)

        if caching:
            if not CACHE_ENABLED:
                raise ValueError(f'caching was enabled but the \'requests_cache\' module is not installed')

            self.session = CachedSession(cache_name=".brawling_cache", use_temp=True, expire_after=timedelta(minutes=10), cache_control=True)
        else:
            self.session = Session()

        self._session_open = True

    def get(self, url: str, params: dict = None) -> Union[ErrorResponse, Union[dict, list]]:
        """Get a JSON response from a URL, returning/throwing an exception if needed.

        Args:
            url (str): the URL

        Raises:
            Exception: If the status code is not 200 but there was no error information (shouldn't ever happen!)
            APIException: If the API returned an error

        Returns:
            Any or ErrorResponse: Either a JSON object (list/dict) or an ErrorResponse if an error has happened and strict mode is disabled.
        """
        if not self._session_open:
            raise RuntimeError("Client has already been closed")

        if not url.startswith(self._base):
            url = self._base + quote_plus(url, safe='/')
        else:
            url = self._base + quote_plus(url[len(self._base):], safe='/')

        headers = {'User-Agent': USER_AGENT}
        # FIXME i'm sorry. this just seemed to be the best way to do it
        # because of mro, a Client that inherits (BaseSyncClient, AuthTokenMixin) will execute BaseClient._add_headers
        # and ignore AuthTokenMixin._add_headers

        for cls in type(self).mro():
            if '_add_headers' in dir(cls):
                cls._add_headers(self, headers)

        r = self.session.get(url, headers=headers, params=params)

        self._logger.info("got url %s, status: %d", url, r.status_code)
        if r.status_code != 200:
            if not r.text:
                raise Exception(f"Got an error and no message, code: {r.status_code}")

            json = r.json()
            exc = self._exc_handler(r.status_code, json)

            self._logger.info("generated exception: %s", str(exc))

            return self._exc_wrapper(exc)

        json = r.json()

        return json

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        if self._session_open:
            self.session.close()
            self._session_open = False

class BaseAsyncClient(BaseClient):
    def __init__(self, base_url: str, strict_errors: bool = True, caching: bool = False) -> None:
        if not HAS_AIOHTTP:
            raise NotImplementedError("async support not installed")

        super().__init__(base_url, strict_errors, caching)

        if caching:
            if not CACHE_ENABLED:
                raise ValueError(f'caching was enabled but the \'aiohttp-client-cache\' module is not installed')

            self.session = CachedAiohttpSession(cache=AIOSQLiteBackend(
                    expire_after=timedelta(minutes=10),
                    cache_control=True,
                    use_temp=True,
                    cache_name='.brawling_acache'
                ))
        else:
            self.session = aiohttp.ClientSession()

        self._session_open = True

    async def get(self, url: str, params: dict = None) -> Union[ErrorResponse, Union[dict, list]]:
        if not self._session_open:
            raise RuntimeError("Client has already been closed")

        if not url.startswith(self._base):
            url = self._base + quote_plus(url, safe='/')
        else:
            url = self._base + quote_plus(url[len(self._base):], safe='/')

        headers = {'User-Agent': USER_AGENT}

        for cls in type(self).mro():
            if '_add_headers' in dir(cls):
                cls._add_headers(self, headers)

        async with self.session.get(url, headers=headers, params=params) as r:
            self._logger.info(f"got url {url}, status {r.status}")

            if r.status != 200:
                if not await r.text():
                    raise Exception(f"Got an error and no message, code: {r.status}")

                json: dict = await r.json()
                exc = self._exc_handler(r.status, json)

                self._logger.info("generated exception: %s", str(exc))

                return self._exc_wrapper(exc)

            json = await r.json()
            return json

    async def aclose(self):
        self._session_open = False
        await self.session.close()

    def __del__(self):
        if self._session_open:
            self._logger.error("Client destructed before calling aclose()")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

class AuthTokenMixin:
    def __init__(self, token: Union[str, Path]):
        self._token = 'Bearer ' + self._parse_token(token)

    def _parse_token(self, token: Union[str, Path]) -> str:
        if isinstance(token, Path):
            return token.read_text().strip()
        else:
            if token.startswith('eyJ0'):
                return token

            ppath = Path(token)
            if ppath.exists():
                return ppath.read_text().strip()
            else:
                # Supposedly dead code, unless they switch from JWT
                return token

    def _add_headers(self, headers: dict):
        headers['Authorization'] = self._token
