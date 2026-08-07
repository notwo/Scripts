from playwright.async_api import async_playwright

from config.config import setting
from services.bingo_service import BingoService
from services.fruitmail_service import FruitmailService
from services.login_service import LoginService
from services.prize_everyday_service import PrizeEverydayService
from services.prize_point_service import PrizePointService
from services.daily_ad_click_service import DailyAdClickService
from services.rank_gacha_service import RankGachaService
from services.prize_present_slot_service import PrizePresentSlotService
from services.scratch_service import ScratchService
from services.prize_roulette_service import PrizeRouletteService


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=setting.browser.headless
        )

        page = await browser.new_page()

        page.set_default_timeout(setting.browser.timeout)

        login_service = LoginService(page, setting)

        game_services = []
        if setting.game.bingo:
            game_services.append(BingoService(page, setting))
        if setting.game.scratch:
            game_services.append(ScratchService(page, setting))
        if setting.routine.prize_everyday:
            game_services.append(PrizeEverydayService(page, setting))
        if setting.routine.prize_point:
            game_services.append(PrizePointService(page, setting))
        if setting.routine.daily_ad_click:
            game_services.append(DailyAdClickService(page, setting))
        if setting.routine.rank_gacha:
            game_services.append(RankGachaService(page, setting))
        if setting.game.prize_present_slot:
            game_services.append(PrizePresentSlotService(page, setting))
        if setting.game.prize_roulette:
            game_services.append(PrizeRouletteService(page, setting))

        fruitmail = FruitmailService(
            login_service=login_service,
            game_services=game_services
        )

        await fruitmail.execute()

        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())