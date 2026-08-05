import asyncio

from pages.login_page import LoginPage


class LoginService:

    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def login(self, login_id, password):

        if not await self.login_page.is_login_page():
            print("既にログイン済み")
            return

        await self.login_page.input_login_info(login_id, password)

        await self.login_page.click_login()

        await self.login_page.close_ad()

        await asyncio.sleep(1)

        await self.page.wait_for_load_state("domcontentloaded")

        await self.page.reload()

        await self.page.wait_for_load_state("domcontentloaded")