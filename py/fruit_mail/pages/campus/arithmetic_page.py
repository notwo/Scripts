import asyncio

from lib.ad_killer import AdKiller
from pages.base_page import BasePage


class ArithmeticPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.ad_killer = AdKiller(page=page)

    async def is_finished(self) -> bool:
        return await self.page.locator("#lead_tomorrow").is_visible()

    async def transfer_check(self) -> bool:
        # スタンプGET
        self._click_clear()
        # モーダルが出たら閉じる
        self._close_modal()
        # 「もう一度プレイする」があればクリック
        self._click_restart()

    async def click_check(self):
        button = self.page.locator("#check")
        if await button.is_visible():
            await button.click(timeout=1000)

    async def click_next(self):
        button = self.page.locator("#next")
        if await button.is_visible():
            await button.click(timeout=1000)

    async def close_ad(self):
        await self.ad_killer.kill_ad()

    async def _click_clear(self):
        button = self.page.locator("#clear")
        if await button.is_visible():
            await button.click(timeout=500)

    async def _close_modal(self):
        await asyncio.sleep(2)

        close_button = self.page.locator("#complete_modal .componentModal__close")
        
        if await close_button.is_visible():
            await close_button.click()

    async def _click_restart(self):
        await asyncio.sleep(2)

        link = self.page.get_by_role(
            "link",
            name="もう一度プレイする"
        )
        if await link.is_visible():
            await link.click(force=True)
