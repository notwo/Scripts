from dataclasses import dataclass


@dataclass(frozen=True)
class SiteSetting:
    login_url: str
    prize_everyday_url: str
    treasure_url: str
    bingo_url: str


@dataclass(frozen=True)
class BrowserSetting:
    headless: bool
    timeout: int


@dataclass(frozen=True)
class BingoSetting:
    max_click: int


@dataclass(frozen=True)
class RoutineSetting:
    prize_everyday: bool
    treasure: bool
    bingo: BingoSetting


@dataclass(frozen=True)
class Setting:
    site: SiteSetting
    browser: BrowserSetting
    routine: RoutineSetting
    bingo: BingoSetting
