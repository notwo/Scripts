import asyncio
from pages.base_page import BasePage


class CampusPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def transfer_check(self):
        # スタンプGET
        await self._click_clear()
        # モーダルが出たら閉じる
        await self._close_modal()
        # 「もう一度プレイする」があればクリック
        await self._click_restart()

    async def is_finished(self) -> bool:
        await asyncio.sleep(2)
        return await self.page.locator("#lead_tomorrow").is_visible()

    async def click_check(self):
        button = self.page.locator("#check")
        if await button.is_visible():
            await button.click(timeout=1000)

    async def click_next(self):
        button = self.page.locator("#next")
        if await button.is_visible():
            await button.click(timeout=1000)

    async def _click_clear(self):
        await asyncio.sleep(3)

        button = self.page.locator("#clear")
        if await button.is_visible():
            await button.click(timeout=500)

    async def _close_modal(self):
        await asyncio.sleep(3)

        close_button = self.page.locator("#complete_modal .componentModal__close")
        
        if await close_button.is_visible():
            await close_button.click()

    async def _click_restart(self):
        await asyncio.sleep(3)

        link = self.page.get_by_role(
            "link",
            name="もう一度プレイする"
        )
        if await link.is_visible():
            await link.click()
