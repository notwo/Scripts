from pages.base_page import BasePage

from lib.ad_killer import AdKiller


class SanjiPage(BasePage):

    def __init__(self, page):
        self.page = page
        self.ad_killer = AdKiller(page=page)

    async def is_finished(self) -> bool:
        return await self.page.locator("#lead_tomorrow").is_visible()

    async def click_clear(self):
        button = self.page.locator("#clear")
        if await button.is_visible():
            await button.click(timeout=500)

    async def click_check(self):
        button = self.page.locator("#check")
        if await button.is_visible():
            await button.click(timeout=500)

    async def click_next(self):
        button = self.page.locator("#next")
        if await button.is_visible():
            await button.click(timeout=500)

    async def close_modal(self):
        pass
        #close_button = self.page.locator(".componentModal__close")
        #if await close_button.is_visible():
        #    await close_button.click(timeout=500)

    async def click_restart(self):
        button = self.page.locator("#restart")
        if await button.is_visible():
            await button.click(timeout=1000)

    async def close_ad(self):
        await self.ad_killer.kill_ad()
