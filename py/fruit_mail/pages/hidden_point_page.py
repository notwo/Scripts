from pages.base_page import BasePage


class HiddenPointPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    async def hidden_point_link_count(self):
        return await self.page.locator("div.hidden_clickItem__winningResult > a").count()

    def hidden_point_link(self, index):
        return self.page.locator("div.hidden_clickItem__winningResult > a").nth(index)
