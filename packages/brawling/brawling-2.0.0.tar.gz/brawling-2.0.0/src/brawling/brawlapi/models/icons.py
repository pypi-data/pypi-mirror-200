from ...models.base import BaseModel, dataclass

__all__ = [
    "Icons",
    "PlayerIcon",
    "ClubIcon",
]

@dataclass
class ClubIcon(BaseModel):
    id: int
    image_url: str

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, 'id image_url')

@dataclass
class PlayerIcon(BaseModel):
    id: int
    name: str
    name2: str
    image_url: str
    image_url2: str
    brawler: int | None
    required_total_trophies: int
    sort_order: int

    is_reward: bool
    is_available_for_offers: bool

    @classmethod
    def from_json(cls, obj):
        return cls._from_props(cls, obj, 'id name name2 imageUrl imageUrl2 brawler requiredTotalTrophies sortOrder isReward isAvailableForOffers')

@dataclass
class Icons(BaseModel):
    player: list[PlayerIcon]
    club: list[ClubIcon]

    @classmethod
    def from_json(cls, obj):
        player_icons = list(obj['player'].values())
        club_icons = list(obj['club'].values())

        return cls(
            cls._unpack_list(PlayerIcon, player_icons),
            cls._unpack_list(ClubIcon, club_icons),
        )
