from pages.base_page import BasePage


class PrizeRoulettePage(BasePage):

    BUTTON_PRIORITY = [
        ("#retry", "もういちど回す"),
        ("#start", "START"),
        ("#stop", "STOP"),
    ]

    def __init__(self, page):
        super().__init__(page)

    async def is_applied(self) -> bool:
        return await self.page.get_by_role(
            "button",
            name="応募済み"
        ).is_visible()

    async def is_finished(self) -> bool:
        """
        ルーレット終了画面か判定
        """
        return await self.page.locator("#end").is_visible()

    async def get_visible_button(self) -> tuple[str, str] | None:
        for selector, name in self.BUTTON_PRIORITY:
            locator = self.page.locator(selector)

            if await locator.count() == 0:
                continue

            if await locator.first.is_visible():
                return selector, name

        return None

    async def click_button(self, selector: str):
        await self.page.locator(selector).first.click()

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
        await self.page.get_by_role(
            "button",
            name="応募する"
        ).click()
    
    async def click_confirm_button(self):
        """
        「確認して次へ」
        """
        await self.page.get_by_role(
            "button",
            name="確認して次へ"
        ).click()

    async def click_final_apply_button(self):
        """
        最後の「承諾する」
        """
        await self.page.get_by_role(
            "button",
            name="承諾する"
        ).click()