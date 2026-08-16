import asyncio

from pages.campus.sanji_page import SanjiPage
from services.campus.medal_service import MedalService
from lib.sanji_solver import SanjiSolver


class SanjiService():
    """
    三字熟語ゲームを解く。

    方針:
      1. まずDBに問い合わせ（前方一致で枝刈り）て候補を探す
      2. DBヒットすればそれを試す（誤ヒットだった場合の保険としてブルートフォースへ）
      3. DBに無ければ全順列を実際に試すブルートフォースへフォールバック
      4. ブルートフォースで正解した熟語はDBに保存し、次回以降はDB検索でヒットさせる

    流れ:
      (2)(3) 漢字取得 → DB検索 → (無ければ)ブルートフォース
      (4)    3個選んで check をクリック
      (5)    正解なら next。不正解なら retry で選択を戻して次を試す
      (6)    これを max_combo_attempts 回繰り返す
      (7)    clear をクリック
    """

    def __init__(self, page, repo, setting):
        self.page = page
        self.sanji_page = SanjiPage(page)
        self.solver = SanjiSolver()
        self.medal_service = MedalService(page=page,setting=setting)
        self._repo = repo
        self.setting = setting
        self._max_combo_attempts = self.setting.campus.sanji["max_combo_attempts"]

    async def game_start(self):
        print("======== 三字熟語ゲーム開始 ========")

        while True:
            try:
                if await self.sanji_page.is_finished():
                    await self.medal_service.run()
                    break

                await self._run()

                await self.sanji_page.transfer_check()

            except Exception as e:
                print(f"Sanji Game Error: {e}")
                # タイムアウトするときは大概広告のせい
                await self.sanji_page.close_ad()

            await asyncio.sleep(5)

        print("======== 三字熟語ゲーム終了 ========")

    async def _run(self):
        await self.sanji_page.click_restart_again()

        """3組の三字熟語を完了させ、最後に clear をクリックする"""
        for attempt in range(1, self._max_combo_attempts + 1):
            print(f"--- 三字熟語 {attempt}/{self._max_combo_attempts} 組目 ---")
            await self._solve_one_combo()

    # ------------------------------------------------------------------
    # 1組分の処理
    # ------------------------------------------------------------------ 
    async def _solve_one_combo(self) -> None:
        available = await self._get_available_kanji()

        # 1. DB検索（枝刈りあり）
        db_combo = self.solver.find_sanji_combo(available, self._repo)
        excluded: set[tuple[str, str, str]] = set()

        if db_combo is not None:
            print(f"  DBヒット: {''.join(db_combo)}")
            excluded.add(db_combo)
            if await self._try_combo(db_combo):
                print(f"  → 正解！（DB検索）")
                return
            print("  → DBのデータと実際の正解が一致しませんでした。ブルートフォースに切り替えます。")

        # 2. ブルートフォース フォールバック
        tried = 0
        for candidate in self.solver.generate_candidates(available=available, shuffle=True):
            if candidate in excluded:
                continue

            tried += 1
            print(f"  試行{tried}: {''.join(candidate)}")

            if await self._try_combo(candidate):
                word = "".join(candidate)
                self._repo.add(word)
                print(f"  → 正解！（ブルートフォース {tried}回目）DBに登録: {word}")
                return

    async def _retry(self) -> bool:
        retry_locator = self.page.locator("#retry")
        if await retry_locator.is_visible():
            # 不正解 → retryで選択をリセットして次の候補へ
            ## あまりに連発して攻撃と判断されないための措置
            await asyncio.sleep(3)
            await retry_locator.click()
            await self._wait_for_selection_cleared()
            return False

        # 正解 → next クリック
        await self.sanji_page.click_next()
        await self._wait_for_selection_cleared()
        return True

    async def _try_combo(self, combo: tuple[str, str, str]) -> bool:
        """1つの組み合わせをクリック→checkで試す。正解ならTrue"""
        await self._click_kanji_combo(combo)
        await self.sanji_page.click_check()

        try:
            return await self._retry()

        except Exception as e:
            await self.sanji_page.close_ad()

    # ------------------------------------------------------------------
    # DOM操作の共通処理
    # ------------------------------------------------------------------
    async def _get_available_kanji(self) -> list[str]:
        # すぐに読み込もうとすると空になる謎現象対策
        await asyncio.sleep(3)

        """未選択（isSelected及びisUsedが付いていない）漢字要素のテキストを取得"""
        items = self.page.locator(".sanjiSelect")
        count = await items.count()

        kanji: list[str] = []
        for i in range(count):
            item = items.nth(i)
            css_class = await item.get_attribute("class") or ""
            classes = css_class.split()
            if "isSelected" in classes or "isUsed" in classes:
                continue
            text = (await item.inner_text()).strip()
            kanji.append(text)
        return kanji

    async def _wait_for_selection_cleared(self) -> None:
        """選択済み(isSelected)の漢字が無くなり、かつ retry が非表示になるまで待つ"""
        await self.page.wait_for_function(
            """
            ({ kanjiSelector, retrySelector, selectedClass }) => {
                const retry = document.querySelector(retrySelector);
                const retryVisible = retry && retry.offsetParent !== null;
                if (retryVisible) return false;
 
                const selectedItems = document.querySelectorAll(
                    kanjiSelector + '.' + selectedClass
                );
                return selectedItems.length === 0;
            }
            """,
            arg={
                "kanjiSelector": "sanjiSelect",
                "retrySelector": "#retry",
                "selectedClass": "isSelected",
            },
        )

    async def _click_kanji_combo(self, combo: tuple[str, str, str]) -> None:
        """漢字を順にクリックして選択する（画面上での選択順序＝熟語の並び）"""
        for kanji in combo:
            locator = (
                self.page.locator('.sanjiSelect:not(.isSelected):not(.isUsed)')
                .filter(has_text=kanji)
                .first
            )
            if await locator.is_visible():
                await locator.click()
