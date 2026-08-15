from playwright.async_api import async_playwright

from config.config import setting
from services.bingo_service import BingoService
from services.kensho_box_service import KenshoBoxService
from services.login_service import LoginService
from services.prize_everyday_service import PrizeEverydayService
from services.treasure_service import TreasureService


def routine_services(page):
    services = []

    if setting.routine.prize_everyday:
        services.append(PrizeEverydayService(page, setting))
    if setting.routine.treasure:
        services.append(TreasureService(page, setting))
    if setting.bingo:
        services.append(BingoService(page, setting))

    return services


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=setting.browser.headless
        )

        page = await browser.new_page()

        page.set_default_timeout(setting.browser.timeout)

        kensho_box = KenshoBoxService(
            login_service=LoginService(page, setting),
            routine_services=routine_services(page)
        )
        await kensho_box.execute()

        await browser.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())