from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    async def is_login_page(self):
        return await self.page.locator("#user_identifier").count() > 0

    async def input_login_info(self, login_id, password):
        await self.page.fill("#user_identifier", login_id)
        await self.page.fill("#password", password)

    async def click_login(self):
        await self.page.locator('button[type="submit"]').click()
