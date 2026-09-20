from urllib.parse import urlparse
import asyncio
from pages.base_page import BasePage


class PrizeEverydayPage(BasePage):

    def __init__(self, page, setting):
        super().__init__(page=page)
        self.setting = setting

    async def finished(self):
        """
        最初の「応募する」があるかどうか
        """
        await asyncio.sleep(3)

        link = self.page.get_by_role(
            "link",
            name="応募する"
        )
        return not await link.is_visible()

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
        await asyncio.sleep(3)

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

        link = self.page.get_by_role(
            "link",
            name="確認して次へ"
        )
        if await link.is_visible():
            await link.click()

    async def click_final_apply_button(self):
        """
        最後の「応募する」
        """
        await asyncio.sleep(3)

        button = self.page.get_by_role(
            "button",
            name="応募する"
        )
        if await button.is_visible():
            await button.click()
