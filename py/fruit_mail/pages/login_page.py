class LoginPage:

    def __init__(self, page):
        self.page = page

    async def is_login_page(self):
        return await self.page.locator("#user_identifier").count() > 0

    async def input_login_info(self, login_id, password):
        await self.page.fill("#user_identifier", login_id)
        await self.page.fill("#password", password)

    async def click_login(self):
        await self.page.locator('button[type="submit"]').click()

    async def close_ad(self):
        ad = self.page.locator("#btn-close-ad-interstitial")
        if await ad.is_visible():
            await ad.click()