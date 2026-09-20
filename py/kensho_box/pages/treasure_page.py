from urllib.parse import urlparse
import asyncio
from pages.base_page import BasePage


class TreasurePage(BasePage):

    def __init__(self, page, setting):
        super().__init__(page=page)
        self.setting = setting

    def _invalid_domain(self) -> bool:
        current_url = self.page.url
        domain = urlparse(current_url).netloc
        return domain != self.setting.site.allowed_domain

    async def finished(self):
        """
        最初の「応募する」があるかどうか
        """
        await asyncio.sleep(3)
        await self.close_ad()
        link = self.page.get_by_role(
            "link",
            name="応募する"
        )
        return not await link.is_visible()

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
        # 全然違う画面に遷移していたら画面を戻る
        if self._invalid_domain():
            await self.page.go_back()

        await asyncio.sleep(3)

        if self._invalid_domain():
            await self.page.go_back()

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
        # 全然違う画面に遷移していたら画面を戻る
        if self._invalid_domain():
            await self.page.go_back()

        await asyncio.sleep(3)

        if self._invalid_domain():
            await self.page.go_back()

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
        if self._invalid_domain():
            await self.page.go_back()

        await asyncio.sleep(3)

        if self._invalid_domain():
            await self.page.go_back()

        button = self.page.get_by_role(
            "button",
            name="応募する"
        )
        if await button.is_visible():
            await button.click()

    async def click_final_apply_button(self):
        """
        最後の「承諾する」
        """
        if self._invalid_domain():
            await self.page.go_back()

        await self.close_ad()

        if self._invalid_domain():
            await self.page.go_back()

        button = self.page.get_by_role(
            "button",
            name="承諾する"
        )
        if await button.is_visible():
            await button.click(force=True)
