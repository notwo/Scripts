from pages.bingo_page import BingoPage
from services.base_game_service import BaseGameService


class BingoService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.bingo_page = BingoPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.bingo_url

    async def play(self):
        await self.click_start()

        count = await self.bingo_page.before_select_count()

        click_count = min(
            self.setting.bingo.max_click,
            count,
        )

        for _ in range(click_count):
            await self.bingo_page.click_first_before_select()

            await self.page.wait_for_function(
                """
                count => document.querySelectorAll(
                    'input.before_select'
                ).length < count
                """,
                arg=count,
            )

            count -= 1

    async def click_start(self):
        if await self.bingo_page.has_start_button():
            await self.bingo_page.click_start()