import asyncio
from abc import ABC, abstractmethod


class BaseGameService(ABC):

    def __init__(self, page, setting):
        self.page = page
        self.setting = setting

    @property
    @abstractmethod
    def url(self) -> str:
        """URL"""

    async def execute(self):
        """共通処理"""

        await self.page.goto(self.url, wait_until="domcontentloaded",)

        # 広告が表示されていたら閉じる
        await self._close_interstitial_ad()

        await self.play()

    async def _close_interstitial_ad(self):
        close_ad = self.page.locator("#btn-close-ad-interstitial")

        if await close_ad.is_visible():
            await close_ad.click()
            await asyncio.sleep(1)

    @abstractmethod
    async def play(self):
        """固有の処理"""