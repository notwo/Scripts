from pages.base_page import BasePage


class PrizePresentSlotPage(BasePage):

    BUTTONS = {
        "#start": "START",
        "#stop": "STOP",
        "#retry": "もういちど回す",
    }

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        return await self.page.locator("#end").is_visible()

    async def visible_button(self):
        """
        表示されているボタンを返す
        Returns:
            tuple[str, str] | None
            (selector, name)
        """
        for selector, name in self.BUTTONS.items():
            locator = self.page.locator(selector)

            if await locator.is_visible():
                return selector, name

        return None

    async def click_button(self, selector: str):
        await self.page.locator(selector).click()