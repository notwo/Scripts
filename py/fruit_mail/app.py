from playwright.async_api import async_playwright

from config.config import setting
from services.bingo_service import BingoService
from services.fruitmail_service import FruitmailService
from services.login_service import LoginService
from services.scratch_service import ScratchService


async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=setting.browser.headless
        )

        page = await browser.new_page()

        page.set_default_timeout(setting.browser.timeout)

        await page.goto(setting.site.bingo_url)

        login_service = LoginService(page)
        bingo_service = BingoService(page, setting)
        scratch_service = ScratchService(page)

        fruitmail = FruitmailService(
            page,
            login_service,
            bingo_service,
            scratch_service,
            setting,
        )

        await fruitmail.execute()

        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())