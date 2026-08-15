from pages.base_page import BasePage


class TreasurePage(BasePage):

    def __init__(self, page):
        self.page = page

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
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
        button = self.page.get_by_role(
            "button",
            name="承諾する"
        )
        if await button.is_visible():
            await button.click()

