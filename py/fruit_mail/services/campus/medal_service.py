"""メダルクリック（未クリックのメダルを開いてタブを閉じる）サービス"""
from playwright.async_api import Page

from lib.ad_killer import AdKiller


class MedalService:
    """
    (1) medal_icon_off.png を含む未クリックのメダル画像を取得
    (2) クリック
    (3) 開いた別タブを閉じる
    (4) 未クリックのメダルがなくなるまで繰り返す
    """

    def __init__(self, page: Page, setting):
        self.page = page
        self.ad_killer = AdKiller(page=page)
        self._off_marker = setting.campus.medal["medal_off_marker"]
        self._active = setting.campus.medal["active"]

    async def run(self) -> None:
        if not self._active:
            return

        while True:
            try:
                target = await self._find_next_off_medal()
                if target is None:
                    print("開くメダルがなくなりました。メダルクリック終了。")
                    break

                async with self.page.context.expect_page() as popup_info:
                    if await target.is_visible():
                        await target.click(timeout=500)
                popup = await popup_info.value
                await popup.close()
            except Exception as e:
                # タイムアウトするときは大概広告のせい
                print('広告焼却')
                await self.ad_killer.kill_ad()

    async def _find_next_off_medal(self):
        """medal_icon_off.png を含む最初の要素を返す（なければ None）"""
        items = self.page.locator(".click_medal_item")
        count = await items.count()

        for i in range(count):
            item = items.nth(i)
            src = await item.locator("img").get_attribute("src") or ""
            if self._off_marker in src:
                return item

        return None