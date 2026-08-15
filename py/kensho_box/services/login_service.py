import asyncio

from pages.login_page import LoginPage


class LoginService:

    def __init__(self, page, setting):
        self.page = page
        self.login_page = LoginPage(page)
        self.setting = setting

    async def login(self, login_mail_address, password):
        await self.page.goto(self.setting.site.login_url)

        if not await self.login_page.is_login_page():
            print("既にログイン済み")
            return

        await self.login_page.input_login_info(login_mail_address, password)

        await self.login_page.click_login()

        await asyncio.sleep(1)

        await self.page.wait_for_load_state("domcontentloaded")

        await self.page.reload(wait_until="domcontentloaded")
