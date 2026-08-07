from pages.prize_everyday_page import PrizeEverydayPage
from services.base_game_service import BaseGameService


class PrizeEverydayService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.prize_page = PrizeEverydayPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_everyday_url

    async def play(self):

        options = await self.prize_page.get_apply_numbers()

        numeric_options = [
            option
            for option in options
            if option["value"].isdigit()
        ]

        if not numeric_options:
            print("応募できる口数がありません")
            return

        max_option = max(
            numeric_options,
            key=lambda x: int(x["value"])
        )

        print(f"応募口数: {max_option['value']}")

        await self.prize_page.select_apply_number(
            max_option["value"]
        )

        await self.prize_page.click_apply_button()

        await self.prize_page.click_confirm_button()

        await self.prize_page.click_confirm_button()

        await self.prize_page.click_final_apply_button()

        print("応募完了")