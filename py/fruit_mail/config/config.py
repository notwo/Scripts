from pathlib import Path

import yaml

from models.setting import BingoSetting, BrowserSetting, Setting, SiteSetting, GameSetting, OtherRoutineSetting, CampusSetting

BASE_DIR = Path(__file__).resolve().parent.parent


def load_setting() -> Setting:

    with open(BASE_DIR / "config" / "setting.yml", encoding="utf-8") as f:
        yml = yaml.safe_load(f)

    return Setting(
        site=SiteSetting(**yml["site"]),
        browser=BrowserSetting(**yml["browser"]),
        bingo=BingoSetting(**yml["bingo"]),
        game=GameSetting(**yml["game"]),
        routine=OtherRoutineSetting(**yml["routine"]),
        campus=CampusSetting(**yml["campus"]),
    )


setting = load_setting()