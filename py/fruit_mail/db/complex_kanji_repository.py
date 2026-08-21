# -*- coding: utf-8 -*-
"""
ComplexKanjiRepository
==================

難読漢字（kanji ←→ hiragana の2断片）をSQLiteに永続化するリポジトリ。
KanjiSolver / seed_kanji.py からはこのクラス経由でのみDBにアクセスする。

テーブル定義
------------
kanjis(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji TEXT,   -- 難読漢字の漢字
    hiragana TEXT    -- 難読漢字の読み
)

難読漢字は順不同（例:「無病息災」←→「むびょうそくさい」）ため、
register() で渡した kanji, hiragana の順番をそのまま保存する。

一方 find() での検索は、ゲーム側の選択肢の並び（シャッフルされて
いる／ブルートフォースで試す順）に依存せずヒットさせたいため、
kanji/hiragana 一方向（a→b）を照会する。
"""

import sqlite3
from pathlib import Path
from typing import Union


class ComplexKanjiRepository:
    """難読漢字（kanjis テーブル）に対する問い合わせ・登録を担当"""

    def __init__(self, db_path: Union[str, Path] = "campus.db"):
        self.db_path = str(db_path)
        self._init_db()

    def __enter__(self) -> "ComplexKanjiRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # 各メソッドが呼び出しの都度コネクションを開閉しているため
        # ここで特別な後始末は不要。with構文で使えるようにするための実装。
        return None

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kanjis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kanji TEXT,
                hiragana TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def find(self, a: str, b: str) -> str:
        """
        a, b の組み合わせが既知の難読漢字として登録済みか判定する。
        検索時は a→b と b→a の両方の並びを照会するため、
        引数の順番が前後していてもヒットする。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT kanji, hiragana FROM kanjis
            WHERE (kanji = ? AND hiragana = ?)
            """,
            (a, b),
        )
        found = cur.fetchone()
        conn.close()
        return found

    def find_pair(self, a: str, b: str):
        """
        a, b の組み合わせが既知の難読漢字として登録済みであれば、
        DBに保存されている本来の順番 (kanji, hiragana) を返す。
        見つからなければ None。

        find() と違い、引数の順番に関わらず「本当のkanji, hiragana順」を
        取得できるため、find_kanji_combo() が返す結果を常に
        正しい語順にそろえたい場合に使う。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT kanji, hiragana FROM kanjis
            WHERE (kanji = ? AND hiragana = ?)
               OR (kanji = ? AND hiragana = ?)
            """,
            (a, b, b, a),
        )
        row = cur.fetchone()
        conn.close()
        return (row[0], row[1]) if row is not None else None

    def register(self, kanji: str, hiragana: str) -> None:
        """
        難読漢字を1件登録する。kanji, hiragana の順番はそのままDBに保存されるため、
        呼び出し側が「前半, 後半」の正しい語順で渡すことを想定している。
        同じ kanji/hiragana の組が既に存在する場合は登録しない。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM kanjis WHERE kanji = ? AND hiragana = ?",
            (kanji, hiragana),
        )
        if cur.fetchone() is None:
            conn.execute(
                "INSERT INTO kanjis (kanji, hiragana) VALUES (?, ?)",
                (kanji, hiragana),
            )
            conn.commit()
        conn.close()

    def register_many(self, entries: list) -> None:
        """
        "前の文字列|後の文字列" 形式の文字列リストをまとめて登録する。
        seed_kanjis.py からの一括登録用。
        """
        for kanji, hiragana in entries:
            self.register(kanji, hiragana)