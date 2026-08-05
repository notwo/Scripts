from abc import ABC, abstractmethod


class BaseGameService(ABC):

    def __init__(self, page, setting):
        self.page = page
        self.setting = setting

    @property
    @abstractmethod
    def url(self) -> str:
        """ゲームのURL"""

    async def execute(self):
        """共通処理"""

        await self.page.goto(self.url)
        await self.page.wait_for_load_state("domcontentloaded")

        await self.play()

    @abstractmethod
    async def play(self):
        """各ゲーム固有の処理"""