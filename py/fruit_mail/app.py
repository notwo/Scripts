import os

from config.config import setting
from playwright.async_api import async_playwright
from services.bingo_service import BingoService
from services.login_service import LoginService


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

        await login_service.login(
            os.getenv("LOGIN_ID"),
            os.getenv("PASSWORD")
        )

        await page.goto(setting.site.bingo_url)

        await bingo_service.play()

        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())