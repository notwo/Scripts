from dataclasses import dataclass


@dataclass(frozen=True)
class SiteSetting:
    login_url: str
    bingo_url: str
    scratch_url: str
    prize_everyday_url: str
    prize_point_url: str
    daily_ad_click_url: str
    rank_gacha_url: str
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
    bingo: bool
    scratch: bool
    prize_present_slot: bool
    prize_roulette: bool


@dataclass(frozen=True)
class OtherRoutineSetting:
    prize_everyday: bool
    prize_point: bool
    daily_ad_click: bool
    rank_gacha: bool


@dataclass(frozen=True)
class Setting:
    site: SiteSetting
    browser: BrowserSetting
    bingo: BingoSetting
    game: GameSetting
    routine: OtherRoutineSetting