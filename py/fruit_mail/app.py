from playwright.async_api import async_playwright

from config.config import setting
from services.bingo_service import BingoService
from services.fruitmail_service import FruitmailService
from services.login_service import LoginService
from services.chirashi_service import ChirashiService
from services.prize_everyday_service import PrizeEverydayService
from services.prize_point_service import PrizePointService
from services.prize_gorgeous_service import PrizeGorgeousService
from services.daily_ad_click_service import DailyAdClickService
from services.rank_gacha_service import RankGachaService
from services.prize_present_slot_service import PrizePresentSlotService
from services.scratch_service import ScratchService
from services.prize_roulette_service import PrizeRouletteService
from services.game_top_service import GameTopService
from services.hidden_point_service import HiddenPointService


def game_services(page, context):
    services = []

    if setting.game.bingo:
        services.append(BingoService(page, setting))
    if setting.game.scratch:
        services.append(ScratchService(page, setting))
    if setting.game.chirashi:
        services.append(ChirashiService(page, setting))
    if setting.game.rank_gacha:
        services.append(RankGachaService(page, setting))
    if setting.game.prize_present_slot:
        services.append(PrizePresentSlotService(page, setting))
    if setting.game.prize_roulette:
        services.append(PrizeRouletteService(page, setting))
    if setting.game.top:
        services.append(GameTopService(page, setting, context))

    return services


def routine_services(page):
    services = []

    if setting.routine.prize_everyday:
        services.append(PrizeEverydayService(page, setting))
    if setting.routine.prize_point:
        services.append(PrizePointService(page, setting))
    if setting.routine.prize_gorgeous:
        services.append(PrizeGorgeousService(page, setting))
    if setting.routine.daily_ad_click:
        services.append(DailyAdClickService(page, setting))
    if setting.routine.hidden_point:
        services.append(HiddenPointService(page, setting))

    return services


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=setting.browser.headless
        )

        context = await browser.new_context()

        page = await context.new_page()

        page.set_default_timeout(setting.browser.timeout)

        fruitmail = FruitmailService(
            login_service=LoginService(page, setting),
            game_services=game_services(page, context),
            routine_services=routine_services(page)
        )
        await fruitmail.execute()

        await context.close()

        await browser.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())