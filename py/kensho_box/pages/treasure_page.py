import asyncio
from pages.base_page import BasePage


class TreasurePage(BasePage):

    def __init__(self, page):
        super().__init__(page=page)

    async def finished(self):
        """
        最初の「応募済み」かどうか
        """
        await asyncio.sleep(3)
        await self.close_ad()
        link = self.page.get_by_role(
            "link",
            name="応募済み"
        )
        return await link.is_visible()

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
        await asyncio.sleep(3)
        await self.close_ad()

        link = self.page.get_by_role(
            "link",
            name="応募する"
        )
        if await link.is_visible():
            await link.click()

    async def click_confirm_button(self):
        """
        「確認して次へ」
        """
        await asyncio.sleep(3)
        await self.close_ad()

        link = self.page.get_by_role(
            "link",
            name="確認して次へ"
        )
        if await link.is_visible():
            await link.click()

    async def click_second_apply_button(self):
        """
        2回目の「応募する」
        """
        await asyncio.sleep(3)
        await self.close_ad()

        button = self.page.get_by_role(
            "button",
            name="応募する"
        )
        if await button.is_visible():
            await button.click()

    async def click_final_apply_button(self):
        """
        最後の「応募する」
        """
        await asyncio.sleep(3)
        await self.close_ad()

        button = self.page.get_by_role(
            "button",
            name="承諾する"
        )
        if await button.is_visible():
            await button.click()

