from pages.base_page import BasePage


class GameTopPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def goto_campus(self, url):
        await self.page.goto(url, wait_until="domcontentloaded")

    async def click_game_link(self, gamename):
        await self.page.get_by_role(
            "link",
            name=gamename
        ).click()

    async def click_game_start_dialog(self):
        await self.page.get_by_role(
            "link",
            name="ゲームを開始する"
        ).click()
