from pages.base_page import BasePage


class BingoPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def has_start_button(self):
        return await self.page.locator("#bingo_start").is_visible()

    async def click_start(self):
        await self.page.locator("#bingo_start").click()

    async def before_select_count(self):
        return await self.page.locator("input.before_select").count()

    async def click_first_before_select(self):
        await self.page.locator("input.before_select").first.click()