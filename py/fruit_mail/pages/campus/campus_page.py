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
        # リロード
        await self.page.reload(wait_until="domcontentloaded")
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
            await button.click(timeout=1000)

    async def _close_modal(self):
        await asyncio.sleep(3)

        close_button = self.page.locator("#complete_modal .componentModal__close")
        
        if await close_button.is_visible():
            await close_button.click()

    async def _click_restart(self):
        # ゲーム実施中であれば何もしない
        check = self.page.locator("#check")
        next = self.page.locator("#next")
        clear = self.page.locator("#clear")
        if await check.is_visible() or await next.is_visible() or await clear.is_visible():
            return

        await asyncio.sleep(5)

        link = self.page.get_by_role(
            "link",
            name="もう一度プレイする"
        )
        # 広告が邪魔で消せないとループするので強制クリックとする
        await link.click(force=True)

    async def click_restart_again(self):
        link = self.page.get_by_role(
            "link",
            name="もう一度プレイする"
        )
        if await link.is_visible():
            await link.click(force=True)
