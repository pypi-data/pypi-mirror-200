from typing import Iterator, Optional, Union
from pathlib import Path
from difflib import SequenceMatcher

from .models import *
from .exceptions import *
from ..util import *
from ..base_client import *

BASE_URL = "https://api.brawlapi.com/v1"

class BrawlAPIClient(BaseSyncClient):
    def __init__(self, strict_errors: bool = True, cache: bool = False) -> None:
        super().__init__(BASE_URL, strict_errors, cache)

    def _exc_handler(self, code: int, exc_json: dict = None):
        return generate_exception(code, exc_json.get("reason", ''))

    def _brawler_id(self, bid: Union[Union[int, str], BrawlerID]):
        result = super()._brawler_id(bid)
        if result:
            return result

        # we got a name
        all_brawlers = self.get_brawlers()
        table = {b.name.upper(): str(b.id) for b in all_brawlers}
        self._bid_cache = table

        return super()._brawler_id(bid)

    def _endpoint(self, path: str, cls, is_list: bool = False):
        data = self.get(path)

        if isinstance(data, ErrorResponse):
            return data

        if is_list:
            return self._unwrap_list(data['list'], cls)

        return cls.from_json(data)

    def get_events(self) -> EventData:
        return self._endpoint('/events', EventData, False)

    def get_brawlers(self) -> list[Brawler]:
        return self._endpoint('/brawlers', Brawler, True)

    def get_brawler(self, brawler: str | int | BrawlerID) -> Brawler:
        id = self._brawler_id(brawler)
        return self._endpoint(f'/brawlers/{id}', Brawler, False)

    def get_maps(self) -> list[Map]:
        return self._endpoint('/maps', Map, True)

    def get_map(self, id: int) -> Map:
        return self._endpoint(f'/maps/{id}', Map, False)

    def get_game_modes(self) -> list[GameMode]:
        return self._endpoint('/gamemodes', GameMode, True)

    def get_game_mode(self, id: int) -> GameMode:
        return self._endpoint(f'/gamemodes/{id}', GameMode, False)

    def get_icons(self) -> Icons:
        return self._endpoint('/icons', Icons, False)

class AsyncBrawlAPIClient(BaseAsyncClient):
    def __init__(self, strict_errors: bool = True, cache: bool = False) -> None:
        super().__init__(BASE_URL, strict_errors, cache)

    def _exc_handler(self, code: int, exc_json: dict = None):
        return generate_exception(code, exc_json.get("reason", ''))

    async def _brawler_id(self, bid: Union[Union[int, str], BrawlerID]):
        result = super()._brawler_id(bid)
        if result:
            return result

        # we got a name
        all_brawlers = await self.get_brawlers()
        table = {b.name.upper(): str(b.id) for b in all_brawlers}
        self._bid_cache = table

        return super()._brawler_id(bid)

    async def _endpoint(self, path: str, cls, is_list: bool = False):
        data = await self.get(path)

        if isinstance(data, ErrorResponse):
            return data

        if is_list:
            return self._unwrap_list(data['list'], cls)

        return cls.from_json(data)

    async def get_events(self) -> EventData:
        return await self._endpoint('/events', EventData, False)

    async def get_brawlers(self) -> list[Brawler]:
        return await self._endpoint('/brawlers', Brawler, True)

    async def get_brawler(self, brawler: str | int | BrawlerID) -> Brawler:
        id = await self._brawler_id(brawler)
        return await self._endpoint(f'/brawlers/{id}', Brawler, False)

    async def get_maps(self) -> list[Map]:
        return await self._endpoint('/maps', Map, True)

    async def get_map(self, id: int) -> Map:
        return await self._endpoint(f'/maps/{id}', Map, False)

    async def get_game_modes(self) -> list[GameMode]:
        return await self._endpoint('/gamemodes', GameMode, True)

    async def get_game_mode(self, id: int) -> GameMode:
        return await self._endpoint(f'/gamemodes/{id}', GameMode, False)

    async def get_icons(self) -> Icons:
        return await self._endpoint('/icons', Icons, False)