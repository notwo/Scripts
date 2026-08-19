# -*- coding: utf-8 -*-
"""
ProverbRepository
==================

ことわざ（head → tail の2断片）をSQLiteに永続化するリポジトリ。
ProverbSolver / seed_proverbs.py からはこのクラス経由でのみDBにアクセスする。

テーブル定義
------------
proverbs(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    head TEXT,   -- ことわざの前半
    tail TEXT    -- ことわざの後半
)

ことわざは順不同ではない（例:「念には」→「念を入れよ」）ため、
register() で渡した head, tail の順番をそのまま保存する。

一方 exists() での検索は、ゲーム側の選択肢の並び（シャッフルされて
いる／ブルートフォースで試す順）に依存せずヒットさせたいため、
head/tail 双方向（a→b, b→a）をOR条件で照会する。
"""

import sqlite3
from pathlib import Path
from typing import Union


class ProverbRepository:
    """ことわざ（proverbs テーブル）に対する問い合わせ・登録を担当"""

    def __init__(self, db_path: Union[str, Path] = "proverb_solver.db"):
        self.db_path = str(db_path)
        self._init_db()

    def __enter__(self) -> "ProverbRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # 各メソッドが呼び出しの都度コネクションを開閉しているため
        # ここで特別な後始末は不要。with構文で使えるようにするための実装。
        return None

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS proverbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                head TEXT,
                tail TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def exists(self, a: str, b: str) -> bool:
        """
        a, b の組み合わせが既知のことわざとして登録済みか判定する。
        検索時は a→b と b→a の両方の並びを照会するため、
        引数の順番が前後していてもヒットする。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 1 FROM proverbs
            WHERE (head = ? AND tail = ?)
               OR (head = ? AND tail = ?)
            """,
            (a, b, b, a),
        )
        found = cur.fetchone() is not None
        conn.close()
        return found

    def find_pair(self, a: str, b: str):
        """
        a, b の組み合わせが既知のことわざとして登録済みであれば、
        DBに保存されている本来の順番 (head, tail) を返す。
        見つからなければ None。

        exists() と違い、引数の順番に関わらず「本当のhead, tail順」を
        取得できるため、find_proverb_combo() が返す結果を常に
        正しい語順にそろえたい場合に使う。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT head, tail FROM proverbs
            WHERE (head = ? AND tail = ?)
               OR (head = ? AND tail = ?)
            """,
            (a, b, b, a),
        )
        row = cur.fetchone()
        conn.close()
        return (row[0], row[1]) if row is not None else None

    def register(self, head: str, tail: str) -> None:
        """
        ことわざを1件登録する。head, tail の順番はそのままDBに保存されるため、
        呼び出し側が「前半, 後半」の正しい語順で渡すことを想定している。
        同じ head/tail の組が既に存在する場合は登録しない。
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM proverbs WHERE head = ? AND tail = ?",
            (head, tail),
        )
        if cur.fetchone() is None:
            conn.execute(
                "INSERT INTO proverbs (head, tail) VALUES (?, ?)",
                (head, tail),
            )
            conn.commit()
        conn.close()

    def register_many(self, entries: list) -> None:
        """
        "前の文字列|後の文字列" 形式の文字列リストをまとめて登録する。
        seed_proverbs.py からの一括登録用。
        """
        for entry in entries:
            head, tail = entry.split("|", 1)
            self.register(head, tail)