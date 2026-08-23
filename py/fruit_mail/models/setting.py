from dataclasses import dataclass


@dataclass(frozen=True)
class SiteSetting:
    login_url: str
    game_top_url: str
    campus_url: str
    bingo_url: str
    scratch_url: str
    hidden_point_url: str
    rank_gacha_url: str
    chirashi_url: str
    prize_everyday_url: str
    prize_point_url: str
    prize_gorgeous_url: str
    daily_ad_click_url: str
    prize_present_slot_url: str
    prize_roulette_url: str


@dataclass(frozen=True)
class BrowserSetting:
    headless: bool
    timeout: int


@dataclass(frozen=True)
class BingoSetting:
    max_click: int


@dataclass(frozen=True)
class GameSetting:
    top: bool
    bingo: bool
    scratch: bool
    rank_gacha: bool
    chirashi: bool
    prize_present_slot: bool
    prize_roulette: bool


@dataclass(frozen=True)
class OtherRoutineSetting:
    prize_everyday: bool
    prize_point: bool
    prize_gorgeous: bool
    daily_ad_click: bool
    hidden_point: bool


@dataclass(frozen=True)
class CampusSetting:
    calculate: dict
    arithmetic: dict
    balance: dict
    proverb: dict
    complex_kanji: dict
    sanji: dict
    medal: dict


@dataclass(frozen=True)
class Setting:
    site: SiteSetting
    browser: BrowserSetting
    bingo: BingoSetting
    game: GameSetting
    routine: OtherRoutineSetting
    campus: CampusSetting