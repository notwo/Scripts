import asyncio
import re
from datetime import datetime, timedelta

from pages.prize_present_slot_page import PrizePresentSlotPage
from services.base_game_service import BaseGameService


class PrizePresentSlotService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.page = page
        self.slot_page = PrizePresentSlotPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_present_slot_url

    async def play(self):
        print("======== プレゼントスロット開始 ========")

        await self.page.reload(wait_until="domcontentloaded")

        while True:
            try:
                if await self.slot_page.is_finished():
                    print("======== プレゼントトップへボタンを検出 ========")
                    countdown = self.page.locator("span.countdown")

                    h = await countdown.locator("#h").inner_text()
                    m = await countdown.locator("#m").inner_text()
                    s = await countdown.locator("#s").inner_text()

                    text = f"{h}:{m}:{s}"

                    match = re.search(r'(\d{2}):(\d{2}):(\d{2})', text)

                    hours, minutes, seconds = map(int, match.groups())

                    now = datetime.now()

                    target_time = now + timedelta(
                        hours=hours,
                        minutes=minutes,
                        seconds=seconds
                    )

                    print(f'次回実行可能時刻: {target_time.strftime("%H:%M:%S")}')
                    break

                if await self.slot_page.close_ad():
                    await asyncio.sleep(1)
                    continue

                button = await self.slot_page.visible_button()

                if button:
                    selector, name = button

                    print(f"{name} をクリック")

                    await self.slot_page.click_button(selector)
                else:
                    # 謎に実行中に画面が読み込み切れず止まることがあるのでリロードで対策
                    self.page.reload()

            except Exception as e:
                await self.slot_page.close_ad()

            await asyncio.sleep(5)

        print("======== プレゼントスロット終了 ========")