import os
import asyncio
from playwright.async_api import async_playwright

password = os.getenv("PASSWORD", "")
login_id = os.getenv("LOGIN_ID", "")


BUTTONS = {
    "#start": "START",
    "#stop": "STOP",
    "#retry": "もういちど回す",
}


async def login(page):
    if await page.locator("#user_identifier").count() == 0:
        print("既にログイン済み")
        return

    # ID・パスワード入力
    await page.fill("#user_identifier", login_id)
    await page.fill("#password", password)

    # ログインボタン押下
    await page.locator('button[type="submit"]').click()

    # ② 広告が表示されていたら閉じる
    close_ad = page.locator("#btn-close-ad-interstitial")
    if await close_ad.is_visible():
        print("広告を閉じます")
        await close_ad.click()

        # 広告が閉じるのを少し待つ
        await asyncio.sleep(1)

    # ログイン後の画面が読み込まれるまで待機
    await page.wait_for_load_state("domcontentloaded")

    print("ログイン完了。リロードします。")

    # 一度リロード
    await page.reload()

    # ログイン完了を待機
    await page.wait_for_load_state("domcontentloaded")


async def monitor_buttons(page, browser):
    while True:
        try:
            # 終了画面チェック（最優先）
            end = page.locator("#end")
            if await end.is_visible():
                print("プレゼントトップへボタンを検出。ブラウザを終了します。")
                await browser.close()
                return

            # 広告が表示されていたら閉じる
            close_ad = page.locator("#btn-close-ad-interstitial")
            if await close_ad.is_visible():
                print("広告を閉じます")
                await close_ad.click()
        
                # 広告が閉じるのを少し待つ
                await asyncio.sleep(1)

                # 次のループへ
                continue

            # 各ボタンをチェック
            for selector, name in BUTTONS.items():
                locator = page.locator(selector)

                if await locator.is_visible():
                    print(f"{name} をクリック")
                    await locator.click()

        except Exception as e:
            print(f"エラー: {e}")

        # 5秒待機
        await asyncio.sleep(5)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        # スロットページへアクセス
        await page.goto("https://slot.fruitmail.net/present_slot/")

        # ログイン
        await login(page)

        # ボタン監視
        await monitor_buttons(page, browser)


asyncio.run(main())
