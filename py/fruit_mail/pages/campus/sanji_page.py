from pages.base_page import BasePage


class SanjiPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        return await self.page.locator("#lead_tomorrow").is_visible()

    async def click_clear(self):
        button = self.page.locator("#clear")
        if await button.is_visible():
            await button.click()

    async def click_check(self):
        button = self.page.locator("#check")
        if await button.is_visible():
            await button.click()

    async def click_next(self):
        button = self.page.locator("#next")
        if await button.is_visible():
            await button.click()

    async def close_modal(self):
        modal = self.page.locator(".componentModal__body")
        if await modal.is_visible():
            close_button = modal.locator(".componentModal__close")
            if await close_button.is_visible():
                await close_button.click()

    async def click_restart(self):
        button = self.page.locator("#restart")
        if await button.is_visible():
            await button.click()

    async def close_ad(self):
        button = self.page.locator("#dismiss-button-element")
        if await button.is_visible():
            await button.click()
