class RankGachaPage:

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        text = self.page.locator("div").get_by_text(
            "プレイ可能数：0",
            exact=True
        )
        return await text.is_visible()

    async def back_to_gacha(self):
        """
        プレイ画面へ戻る
        """
        button = self.page.get_by_role(
            "button",
            name="プレイ画面へ戻る"
        )
        if await button.is_visible():
          await button.click()

    async def click_button(self):
        """
        ガチャを回す
        """
        await self.page.get_by_role(
            "button",
            name="ガチャを回す"
        ).click()