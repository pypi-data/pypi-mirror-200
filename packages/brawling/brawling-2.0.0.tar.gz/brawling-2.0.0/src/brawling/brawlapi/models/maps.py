from ...models.base import BaseModel, dataclass
from datetime import datetime
from .modes import PartialGameMode

__all__ = [
    "MapEnvironment",
    "Map"
]

@dataclass
class MapEnvironment(BaseModel):
    id: int
    name: str
    hash: str
    path: str
    version: int
    image_url: str

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, "id name hash path version imageUrl")

@dataclass
class Map(BaseModel):
    # this is so unholy.
    id: int
    new: bool
    disabled: bool
    name: str
    hash: str
    version: int

    link: str
    image_url: str
    credit: str

    environment: MapEnvironment
    game_mode: PartialGameMode

    last_active: datetime
    data_updated: datetime

    @classmethod
    def from_json(cls, obj):
        return cls(
            *cls._unpack_props(obj, 'id new disabled name hash version link imageUrl credit'),
            MapEnvironment.from_json(obj['environment']),
            PartialGameMode.from_json(obj['gameMode']),
            cls._datetime(obj['lastActive']),
            cls._datetime(obj['dataUpdated']),
        )
