from dataclasses import dataclass
from datetime import datetime
import dateutil.parser

from ...models.base import BaseModel
from .maps import MapEnvironment, Map
from .modes import PartialGameMode

__all__ = [
    "EventSlot",
    "EventMapBrawlerStat",
    "EventMapTeamStat",
    "EventMap",
    "EventModifier",
    "Event",
    "EventData",
]

@dataclass
class EventSlot(BaseModel):
    id: int
    name: str
    emoji: str # jesus christ.
    hash: str
    list_alone: bool
    hideable: bool
    hide_for_slot: None # ???
    background: None # ??? pl maybe?

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, "id name emoji hash listAlone hideable hideForSlot background")

@dataclass
class EventMapBrawlerStat(BaseModel):
    brawler: int
    win_rate: float
    use_rate: float
    star_player_rate: float | None

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, "brawler winRate useRate starRate")

@dataclass
class EventMapTeamStat(BaseModel):
    name: str
    hash: str
    brawler_1: str
    brawler_2: str
    brawler_3: str | None

    win_rate: float
    use_rate: float
    wins: int
    losses: int
    draws: int
    total: int

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj['data'], 'name hash brawler1 brawler2 brawler3 winRate useRate wins losses draws total')

@dataclass
class EventMap(Map):
    stats: list[EventMapBrawlerStat]
    team_stats: list[EventMapTeamStat] | None

    @classmethod
    def from_json(cls, obj):
        return cls(
            **Map.from_json(obj).__dict__,
            stats=cls._unpack_list(EventMapBrawlerStat, obj['stats']),
            team_stats=cls._unpack_list(EventMapTeamStat, obj['teamStats']),
        )

@dataclass
class EventModifier(BaseModel):
    pass # ???

@dataclass
class Event(BaseModel):
    slot: EventSlot
    start_time: datetime
    end_time: datetime
    reward: int # tokens for pressing on the event
    map: EventMap
    modifier: EventModifier | None

    @classmethod
    def from_json(cls, obj):
        return cls(
            EventSlot.from_json(obj['slot']),
            dateutil.parser.isoparse(obj['startTime']),
            dateutil.parser.isoparse(obj['endTime']),
            obj['reward'],
            EventMap.from_json(obj['map']),
            EventModifier.from_json(obj['modifier']) if obj['modifier'] else None
        )

@dataclass
class EventData(BaseModel):
    active: list[Event]
    upcoming: list[Event]

    @classmethod
    def from_json(cls, obj):
        return cls(
            cls._unpack_list(Event, obj['active']),
            cls._unpack_list(Event, obj['upcoming']),
        )
