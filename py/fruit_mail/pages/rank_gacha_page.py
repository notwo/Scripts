from pages.base_page import BasePage


class RankGachaPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    async def is_finished(self) -> bool:
        text = self.page.locator("div").get_by_text(
            "プレイ可能数：0",
            exact=True
        )
        return await text.is_visible()

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
        link = self.page.locator("a.rankgacha_result__backToLink")
        if await link.is_visible():
          await link.click()

    async def click_button(self):
        """
        ガチャを回す
        """
        await self.ok_button()

        button = self.page.get_by_role(
            "button",
            name="ガチャを回す"
        )
        if await button.is_visible():
            await button.click()