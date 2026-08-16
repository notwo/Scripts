from lib.ad_killer import AdKiller


class BasePage:

    def __init__(self, page):
        self.page = page
        self.ad_killer = AdKiller(page=page)

    def wait_for_debug(self):
        self.page.wait_for_timeout(10000)

    async def close_ad(self):
        """
        広告の閉じるボタンを探してクリックする
        """
        await self.ad_killer.kill_ad()