from ...models.base import BaseModel, dataclass
from datetime import datetime

__all__ = [
    "PartialGameMode",
    "GameMode"
]

@dataclass
class PartialGameMode(BaseModel):
    id: int
    name: str
    hash: str
    version: int
    color: str
    link: str
    image_url: str

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, "id name hash version color link imageUrl")

@dataclass
class GameMode(BaseModel):
    id: int
    sc_id: int
    name: str
    hash: str
    sc_hash: str
    disabled: bool
    color: str
    bg_color: str
    version: int
    title: str
    tutorial: str
    description: str
    short_description: str

    sort1: int # ??
    sort2: int # ??

    link: str
    image_url: str
    image_url2: str
    last_active: datetime

    @classmethod
    def from_json(cls, obj):
        return cls(
            *cls._unpack_props(obj, 'id scId name hash scHash disabled color bgColor version title tutorial description shortDescription sort1 sort2 link imageUrl imageUrl2'),
            cls._datetime(obj['lastActive'])
        )
