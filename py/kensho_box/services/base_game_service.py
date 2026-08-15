import asyncio
from abc import ABC, abstractmethod
from lib.ad_killer import AdKiller


class BaseGameService(ABC):

    def __init__(self, page, setting):
        self.page = page
        self.setting = setting
        self.ad_killer = AdKiller(page=page)

    @property
    @abstractmethod
    def url(self) -> str:
        """URL"""

    async def execute(self):
        """共通処理"""

        await self.page.goto(self.url, wait_until="domcontentloaded")

        # 広告が表示されていたら閉じる
        await self.ad_killer.kill_ad()

        await self.play()

    @abstractmethod
    async def play(self):
        """固有の処理"""