import os


class FruitmailService:

    def __init__(
        self,
        login_service,
        game_services,
        routine_services,
    ):
        self.login_service = login_service
        self.game_services = game_services
        self.routine_services = routine_services

    async def execute(self):
        login_id = os.getenv("LOGIN_ID")
        password = os.getenv("FR_PASSWORD")
        if not login_id or not password:
            print("login_id,passwordを設定してください")
            return

        await self.login_service.login(login_id, password)

        for routine in self.routine_services:
            await routine.execute()
        for game in self.game_services:
            await game.execute()
