import os


class FruitmailService:

    def __init__(
        self,
        page,
        login_service,
        bingo_service,
        scratch_service,
        setting,
    ):
        self.page = page
        self.setting = setting
        self.login_service = login_service
        self.bingo_service = bingo_service
        self.scratch_service = scratch_service

    async def execute(self):
        login_id = os.getenv("LOGIN_ID")
        password = os.getenv("FR_PASSWORD")
        if not login_id or not password:
            print("login_id,passwordを設定してください")
            return

        await self.login_service.login(login_id, password)

        await self.page.goto(self.setting.site.bingo_url)
        await self.bingo_service.play()

        await self.page.goto(self.setting.site.scratch_url)
        await self.scratch_service.play()
