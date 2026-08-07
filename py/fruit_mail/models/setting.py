from dataclasses import dataclass


@dataclass(frozen=True)
class SiteSetting:
    login_url: str
    bingo_url: str
    scratch_url: str
    prize_everyday_url: str
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
    prize_everyday: bool
    prize_present_slot: bool
    prize_roulette: bool


@dataclass(frozen=True)
class Setting:
    site: SiteSetting
    browser: BrowserSetting
    bingo: BingoSetting
    game: GameSetting