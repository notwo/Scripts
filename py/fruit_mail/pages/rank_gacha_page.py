class RankGachaPage:

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        text = self.page.locator("div").get_by_text(
            "プレイ可能数：0",
            exact=True
        )
        return await text.is_visible()

    async def close_ad(self):
        text = self.page.locator("div.continue-prompt-text")
        if await text.is_visible():
            text.click()

    async def ok_button(self):
        """
        動画の読み込みに失敗しました
        """
        button = self.page.get_by_role(
            "button",
            name="OK"
        )
        if await button.is_visible():
          await button.click()

    async def back_to_gacha(self):
        """
        プレイ画面へ戻る
        """
        link = self.page.get_by_role(
            "link",
            name="プレイ画面へ戻る"
        )
        if await link.is_visible():
          await link.click()

    async def click_button(self):
        """
        ガチャを回す
        """
        await self.page.get_by_role(
            "button",
            name="ガチャを回す"
        ).click()