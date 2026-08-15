class LoginPage:

    def __init__(self, page):
        self.page = page

    async def is_login_page(self):
        return await self.page.locator("#login_mail_address").count() > 0

    async def input_login_info(self, login_id, password):
        await self.page.fill("#login_mail_address", login_id)
        await self.page.fill("#login_pass", password)

    async def click_login(self):
        await self.page.locator('#btn_login').click()
