from playwright.async_api import async_playwright

from config.config import setting
from services.bingo_service import BingoService
from services.fruitmail_service import FruitmailService
from services.login_service import LoginService
from services.prize_present_slot_service import PrizePresentSlotService
from services.scratch_service import ScratchService


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=setting.browser.headless
        )

        page = await browser.new_page()

        page.set_default_timeout(setting.browser.timeout)

        login_service = LoginService(page, setting)

        game_services = [
#            BingoService(page, setting),
#            ScratchService(page, setting),
            PrizePresentSlotService(page, setting),
        ]

        fruitmail = FruitmailService(
            login_service=login_service,
            game_services=game_services
        )

        await fruitmail.execute()

        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())