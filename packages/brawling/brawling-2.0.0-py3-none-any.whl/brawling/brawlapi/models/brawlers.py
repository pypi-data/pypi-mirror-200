from ...models.base import BaseModel, dataclass

__all__ = [
    "Brawler",
    "BrawlerClass",
    "BrawlerRarity",
    "StarPower",
    "Gadget",
    "EquipmentItem"
]

@dataclass
class BrawlerClass(BaseModel):
    id: int
    name: str

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, 'id name')

@dataclass
class BrawlerRarity(BaseModel):
    id: int
    name: str
    color: str

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, 'id name color')

@dataclass
class EquipmentItem(BaseModel):
    id: int
    name: str
    path: str
    version: int
    description: str
    description_html: str
    image_url: str
    released: bool

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, 'id name path version description descriptionHtml imageUrl released')

@dataclass
class StarPower(EquipmentItem):
    pass

@dataclass
class Gadget(EquipmentItem):
    pass

@dataclass
class Brawler(BaseModel):
    id: int
    avatar_id: int
    name: str
    hash: str
    path: str
    released: bool
    version: int
    link: str
    image_url: str
    image_url2: str
    image_url3: str

    class_: BrawlerClass
    rarity: BrawlerRarity
    unlock: None # ??

    description: str
    description_html: str

    star_powers: list[StarPower]
    gadgets: list[Gadget]

    @classmethod
    def from_json(cls, obj):
        return cls(
            *cls._unpack_props(obj, 'id avatarId name hash path released version link imageUrl imageUrl2 imageUrl3'),
            BrawlerClass.from_json(obj['class']),
            BrawlerRarity.from_json(obj['rarity']),
            *cls._unpack_props(obj, 'unlock description descriptionHtml'),
            cls._unpack_list(StarPower, obj['starPowers']),
            cls._unpack_list(Gadget, obj['gadgets']),
        )
