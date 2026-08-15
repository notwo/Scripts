import os


class KenshoBoxService:

    def __init__(
        self,
        login_service,
        routine_services,
    ):
        self.login_service = login_service
        self.routine_services = routine_services

    async def execute(self):
        login_mail_address = os.getenv("KB_LOGIN_MAIL_ADDRESS")
        password = os.getenv("KB_PASSWORD")
        if not login_mail_address or not password:
            print("login_mail_address,passwordを設定してください")
            return

        await self.login_service.login(login_mail_address, password)

        for routine in self.routine_services:
            await routine.execute()
