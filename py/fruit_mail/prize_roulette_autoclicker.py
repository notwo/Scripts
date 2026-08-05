import os
import asyncio
from playwright.async_api import async_playwright

password = os.getenv("PASSWORD", "")
login_id = os.getenv("LOGIN_ID", "")


async def login(page):
    # ログインページ表示
    await page.goto("https://www.fruitmail.net/login?go_html=https://www.fruitmail.net/prize/roulette/")

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
            #close_ad = page.locator("#btn-close-ad-interstitial")
            #if await close_ad.is_visible():
            #    print("広告を閉じます")
            #    await close_ad.click()
            #
            #    # 広告が閉じるのを少し待つ
            #    await asyncio.sleep(1)
            #
            #    # 次のループへ
            #    continue

            # 各ボタンをチェック
            while True:
                await asyncio.sleep(3)

                retry = page.locator("#retry")
                start = page.locator("#start")

                if await retry.is_visible():
                    print("retry")
                    await retry.click()

                    # retryが消えるまで待つ
                    await retry.wait_for(state="hidden")
                    continue
                elif await start.is_visible():
                    print("start")
                    await start.click()

                    # retryが出るまで待つ
                    await retry.wait_for(state="visible")
                    continue
                else:
                    print("どちらのボタンも表示されません。画面を確認して操作してください。")
                    input("操作が終わったら Enter を押してください...")
                    print("全処理を終了します。")
                    exit(0)

        except Exception as e:
            print(f"エラー: {e}")

        # 5秒待機
        await asyncio.sleep(5)



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        # 直でスロットページを開こうとするとトップページに飛ばされてログイン画面に行かないので、先に直接ログイン画面にアクセスする
        # ログイン
        await login(page)

        # スロットページへアクセス
        await page.goto("https://www.fruitmail.net/prize/roulette/")

        # その場で数秒待つ。遷移が速すぎて画面表示が間に合わず、スタートをクリックできないことが多々ある
        await asyncio.sleep(3)
        # スタートボタンクリック
        await page.locator('button[type="submit"]').click()

        # ボタン監視
        await monitor_buttons(page, browser)


asyncio.run(main())
