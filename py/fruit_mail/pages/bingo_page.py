class BingoPage:

    def __init__(self, page):
        self.page = page

    async def click_start(self):
        start = self.page.locator("#bingo_start")
        if await start.is_visible():
            await start.click()

    async def before_select_count(self):
        return await self.page.locator("input.before_select").count()

    async def click_first_before_select(self):
        await self.page.locator("input.before_select").first.click()