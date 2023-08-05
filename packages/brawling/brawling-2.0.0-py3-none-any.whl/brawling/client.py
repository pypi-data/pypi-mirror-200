from typing import Iterator, Optional, Union
from pathlib import Path
from difflib import SequenceMatcher

from .models import *
from .exceptions import *
from .util import *
from .base_client import *

__all__ = [
    "Client",
    "AsyncClient",
]

BASE_URL = "https://api.brawlstars.com/v1"
PROXY_URL = "https://bsproxy.royaleapi.dev/v1"

class Client(BaseSyncClient, AuthTokenMixin):
    """Brawl Stars API client

    To obtain data from the API, use methods starting with get_*. They return a simple response model

    To paginate over data, use methods starting with page_*. They return iterators that yield response models.
    """
    def __init__(self, token: Union[str, Path], *, proxy: bool = False, strict_errors: bool = True, cache: bool = False):
        """Initialize the main client

            `token (str | Path)` - auth token or a Path object to a file with it

            `proxy (bool, optional, default False)` - whether to use [a 3rd party proxy](https://docs.royaleapi.com/#/proxy). DISCLAIMER: Use at your own risk. The safety of this proxy is not guaranteed by the developer of brawling.

            `strict_errors (bool, optional, default True)` - whether to raise exceptions if API returned a failure status code, or to return them. Will still raise non-API related exceptions.

            `cache (bool, optional, default False)` - whether to cache responses, need to have `requests_cache` module installed to work
        """
        AuthTokenMixin.__init__(self, token)
        super().__init__(PROXY_URL if proxy else BASE_URL, strict_errors, cache)

    def _brawler_id(self, bid: Union[Union[int, str], BrawlerID]):
        result = super()._brawler_id(bid)
        if result:
            return result

        # we got a name
        all_brawlers = self.get_brawlers()
        table = {b.name.upper(): str(b.id) for b in all_brawlers}
        self._bid_cache = table

        return super()._brawler_id(bid)

    # helper methods to massively decrease boilerplate code

    def _endp_ranking(self, region, uri, cls):
        if region is None:
            region = 'global'

        res = self.get(uri % region)
        if isinstance(res, ErrorResponse):
            return res

        return self._unwrap_list(res["items"], cls)

    def _endp_tag(self, tag, uri, cls):
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = self.get(uri % tag)
        if isinstance(res, ErrorResponse):
            return res

        return cls.from_json(res)

    def _endp_tag_list(self, tag, uri, cls):
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = self.get(uri % tag)
        if isinstance(res, ErrorResponse):
            return res

        lst = self._unwrap_list(res["items"], cls)

        return lst

    # players

    def get_battle_log(self, tag: str) -> list[Battle]:
        """Get a list of recent battles of a player by their tag. According to the API, it may take up to 30 minutes for a new battle to appear."""
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = self.get(f"/players/{tag}/battlelog")
        if isinstance(res, ErrorResponse):
            return res

        battle_list = res["items"]
        return self._parse_battles(battle_list)

    def get_player(self, tag: str) -> Player:
        """Get information about a player by their tag."""
        return self._endp_tag(tag, '/players/%s', Player)

    # clubs

    def get_club_members(self, tag: str) -> list[ClubMember]:
        """Get members of a club by its tag."""
        return self._endp_tag_list(tag, '/clubs/%s/members', ClubMember)

    def get_club(self, tag: str) -> Club:
        """Get the information about a club by its tag."""
        return self._endp_tag(tag, '/clubs/%s', Club)

    # rankings

    # -- power play seasons not included due to being obsolete -- #

    def get_club_rankings(self, region: Optional[str] = None) -> list[ClubRanking]:
        return self._endp_ranking(region, f'/rankings/%s/clubs', ClubRanking)

    def get_brawler_rankings(self, brawler_id: Union[Union[int, str], BrawlerID], region: Optional[str] = None) -> list[BrawlerRanking]:
        return self._endp_ranking(region, f'/rankings/%s/brawlers/{self._brawler_id(brawler_id)}', BrawlerRanking)

    def get_player_rankings(self, region: Optional[str] = None) -> list[PlayerRanking]:
        return self._endp_ranking(region, f'/rankings/%s/players', PlayerRanking)

    # brawlers

    def get_brawlers(self) -> list[Brawler]:
        """Get a list of all the brawlers available in game"""
        res = self.get("/brawlers")
        if isinstance(res, ErrorResponse):
            return res

        lst = self._unwrap_list(res["items"], Brawler)

        return lst

    def get_brawler(self, id: Union[Union[int, str], BrawlerID]) -> Brawler:
        """Get a single brawler by their ID or an enumeration value.

        If for some reason the enum `BrawlerID` is not up to date, you can specify the literal brawler name instead.
        It will fetch all the brawlers and use the ID of the brawler you specified
        """
        res = self.get(f"/brawlers/{self._brawler_id(id)}")
        if isinstance(res, ErrorResponse):
            return res

        return Brawler.from_json(res)

    # events

    def get_event_rotation(self) -> EventRotation:
        """Get currently ongoing event rotation"""
        res = self.get(f"/events/rotation")
        if isinstance(res, ErrorResponse):
            return res

        return EventRotation.from_json(res)

    # --- paging methods --- #

    def page_club_members(
            self, tag: str, per_page: int, *, max: int = 0
    ) -> Iterator[list[ClubMember]]:
        """Return a paginator over members of a club"""

        return RequestPaginator(self, f"/clubs/{tag}/members", per_page, max, ClubMember)

    def page_club_rankings(
            self, per_page: int, region: Optional[str] = None, *, max: int = 0
    ) -> Iterator[list[ClubRanking]]:
        """Return a paginator over club rankings in a region (or worldwide if no region specified)"""

        if region is None:
            region = "global"

        return RequestPaginator(self, f"/rankings/{region}/clubs", per_page, max, ClubRanking)

    def page_brawler_rankings(
        self, brawler_id: Union[Union[int, str], BrawlerID], per_page: int, region: Optional[str] = None, *, max: int = 0
    ) -> Iterator[list[BrawlerRanking]]:
        """Return a paginator over brawler rankings in a region (or worldwide if no region specified)
        NOTE: look at `Client.get_brawler` documentation for more information about `brawler_id`"""
        if region is None:
            region = "global"

        return RequestPaginator(self, f"/rankings/{region}/brawlers/{self._brawler_id(brawler_id)}", per_page, max, BrawlerRanking)

    def page_player_rankings(
        self, per_page: int, region: Optional[str] = None, *, max: int = 0
    ) -> Iterator[list[PlayerRanking]]:
        """Return a paginator over player rankings in a region (or worldwide if no region specified)"""
        if region is None:
            region = "global"

        return RequestPaginator(self, f"/rankings/{region}/players", per_page, max, PlayerRanking)

    def page_brawlers(
        self, per_page: int, *, max: int = 0
    ) -> Iterator[list[Brawler]]:
        """Return a paginator over all the brawlers present in game at current time"""
        return RequestPaginator(self, f"/brawlers", per_page, max, Brawler)

class AsyncClient(BaseAsyncClient, AuthTokenMixin):
    """Asynchronous Brawl Stars API client

    To obtain data from the API, use methods starting with get_*. They return a simple response model

    To paginate over data, use methods starting with page_*. They return iterators that yield response models.
    """
    def __init__(self, token: Union[str, Path], *, proxy: bool = False, strict_errors: bool = True, cache: bool = False):
        """Initialize the main client

            `token (str | Path)` - auth token or a Path object to a file with it

            `proxy (bool, optional, default False)` - whether to use [a 3rd party proxy](https://docs.royaleapi.com/#/proxy). DISCLAIMER: Use at your own risk. The safety of this proxy is not guaranteed by the developer of brawling.

            `strict_errors (bool, optional, default True)` - whether to raise exceptions if API returned a failure status code, or to return them. Will still raise non-API related exceptions.

            `cache (bool, optional, default False)` - whether to cache responses, need to have `requests_cache` module installed to work
        """
        AuthTokenMixin.__init__(self, token)
        super().__init__(PROXY_URL if proxy else BASE_URL, strict_errors, cache)

    async def _brawler_id(self, bid: Union[Union[int, str], BrawlerID]):
        result = super()._brawler_id(bid)
        if result:
            return result

        # we got a name
        all_brawlers = await self.get_brawlers()
        table = {b.name.upper(): str(b.id) for b in all_brawlers}
        self._bid_cache = table

        return super()._brawler_id(bid)

    # decreasing boilerplate again

    async def _endp_tag(self, tag, uri, cls):
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = await self.get(uri % tag)
        if isinstance(res, ErrorResponse):
            return res

        return cls.from_json(res)

    async def _endp_tag_list(self, tag, uri, cls):
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = await self.get(uri % tag)
        if isinstance(res, ErrorResponse):
            return res

        lst = self._unwrap_list(res["items"], cls)

        return lst

    async def _endp_ranking(self, region, uri, cls):
        if region is None:
            region = 'global'

        res = await self.get(uri % region)
        if isinstance(res, ErrorResponse):
            return res

        return self._unwrap_list(res["items"], cls)

    # players

    async def get_battle_log(self, tag: str) -> list[Battle]:
        """Get a list of recent battles of a player by their tag. According to the API, it may take up to 30 minutes for a new battle to appear."""
        tag = self._verify_tag(tag)
        if isinstance(tag, Exception):
            return self._exc_wrapper(tag)

        res = await self.get(f"/players/{tag}/battlelog")
        if isinstance(res, ErrorResponse):
            return res

        battle_list = res["items"]

        return self._parse_battles(battle_list)

    async def get_player(self, tag: str) -> Player:
        """Get information about a player by their tag."""
        return await self._endp_tag(tag, '/players/%s', Player)

    # clubs

    async def get_club_members(self, tag: str) -> list[ClubMember]:
        """Get members of a club by its tag."""
        return await self._endp_tag_list(tag, '/clubs/%s/members', ClubMember)

    async def get_club(self, tag: str) -> Club:
        """Get the information about a club by its tag."""
        return await self._endp_tag(tag, '/clubs/%s', Club)

    # rankings

    # -- power play seasons not included due to being obsolete -- #

    async def get_club_rankings(self, region: Optional[str] = None) -> list[ClubRanking]:
        return await self._endp_ranking(region, '/rankings/%s/clubs', ClubRanking)

    async def get_brawler_rankings(self, brawler_id: Union[Union[int, str], BrawlerID], region: Optional[str] = None) -> list[BrawlerRanking]:
        return await self._endp_ranking(region, f"/rankings/%s/brawlers/{await self._brawler_id(brawler_id)}", BrawlerRanking)

    async def get_player_rankings(self, region: Optional[str] = None) -> list[PlayerRanking]:
        return await self._endp_ranking(region, '/rankings/%s/players', PlayerRanking)

    # brawlers

    async def get_brawlers(self) -> list[Brawler]:
        """Get a list of all the brawlers available in game.

        `sort_factor` is ignored if sorting was disabled."""
        res = await self.get("/brawlers")
        if isinstance(res, ErrorResponse):
            return res

        lst = self._unwrap_list(res["items"], Brawler)

        return lst

    async def get_brawler(self, id: Union[Union[int, str], BrawlerID]) -> Brawler:
        """Get a single brawler by their ID or an enumeration value.

        If for some reason the enum `BrawlerID` is not up to date, you can specify the literal brawler name instead.
        It will fetch all the brawlers and use the ID of the brawler you specified
        """
        res = await self.get(f"/brawlers/{await self._brawler_id(id)}")
        if isinstance(res, ErrorResponse):
            return res

        return Brawler.from_json(res)

    # events

    async def get_event_rotation(self) -> EventRotation:
        """Get currently ongoing event rotation"""
        res = await self.get(f"/events/rotation")
        if isinstance(res, ErrorResponse):
            return res

        return EventRotation.from_json(res)

    # --- paging methods --- #

    async def page_club_members(
            self, tag: str, per_page: int, *, limit: int = 0
    ) -> Iterator[list[ClubMember]]:
        """Return a paginator over members of a club"""

        return AsyncRequestPaginator(self, f"/clubs/{tag}/members", per_page, limit, ClubMember)

    async def page_club_rankings(
            self, per_page: int, region: Optional[str] = None, *, limit: int = 0
    ) -> Iterator[list[ClubRanking]]:
        """Return a paginator over club rankings in a region (or worldwide if no region specified)"""

        if region is None:
            region = "global"

        return AsyncRequestPaginator(self, f"/rankings/{region}/clubs", per_page, limit, ClubRanking)

    async def page_brawler_rankings(
        self, brawler_id: Union[Union[int, str], BrawlerID], per_page: int, region: Optional[str] = None, *, limit: int = 0
    ) -> Iterator[list[BrawlerRanking]]:
        """Return a paginator over brawler rankings in a region (or worldwide if no region specified)
        NOTE: look at `Client.get_brawler` documentation for more information about `brawler_id`"""
        if region is None:
            region = "global"

        return AsyncRequestPaginator(self, f"/rankings/{region}/brawlers/{await self._brawler_id(brawler_id)}", per_page, limit, BrawlerRanking)

    async def page_player_rankings(
        self, per_page: int, region: Optional[str] = None, *, limit: int = 0
    ) -> Iterator[list[PlayerRanking]]:
        """Return a paginator over player rankings in a region (or worldwide if no region specified)"""
        if region is None:
            region = "global"

        return AsyncRequestPaginator(self, f"/rankings/{region}/players", per_page, limit, PlayerRanking)

    async def page_brawlers(
        self, per_page: int, *, limit: int = 0
    ) -> Iterator[list[Brawler]]:
        """Return a paginator over all the brawlers present in game at current time"""
        return AsyncRequestPaginator(self, f"/brawlers", per_page, limit, Brawler)

