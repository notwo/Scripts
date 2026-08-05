class BingoService:

    def __init__(self, page, setting):
        self.page = page
        self.setting = setting

    async def play(self):

        await self.click_start()

        count = await self.page.locator("input.before_select").count()

        click_count = min(
            self.setting.bingo.max_click,
            count,
        )

        for _ in range(click_count):

            await self.page.locator("input.before_select").first.click()

            await self.page.wait_for_function(
                "count => document.querySelectorAll('input.before_select').length < count",
                arg=count,
            )

            count -= 1

    async def click_start(self):

        start = self.page.locator("#bingo_start")

        if await start.is_visible():
            await start.click()