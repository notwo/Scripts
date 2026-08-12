class RankGachaPage:

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        text = self.page.locator("div").get_by_text(
            "プレイ可能数：0",
            exact=True
        )
        return await text.is_visible(timeout=500)

    async def close_ad(self):
        text = self.page.locator("div.continue-prompt-text")
        if await text.is_visible(timeout=500):
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
          await button.click(timeout=500)

    async def back_to_gacha(self):
        """
        プレイ画面へ戻る
        """
        link = self.page.locator("a.rankgacha_result__backToLink")
        if await link.is_visible(timeout=500):
          await link.click()

    async def click_button(self):
        """
        ガチャを回す
        """
        await self.page.get_by_role(
            "button",
            name="ガチャを回す"
        ).click()