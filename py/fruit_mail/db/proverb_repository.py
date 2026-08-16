# -*- coding: utf-8 -*-
"""
ProverbRepository
==================

「ことわざの正解ペア」をSQLiteに永続化するリポジトリ。
IdiomRepository と同様、ProverbSolver からはこのクラス経由でのみ
DBにアクセスする。

テーブル定義
------------
known_combos(pattern TEXT PRIMARY KEY)

pattern は、正解ペアの2断片を sorted() で順序を揃えてから
"|||" で連結した文字列。選択順に依存せず同一パターンとして
照合できるようにするための正規化。
"""

import sqlite3


class ProverbRepository:
    """ことわざの正解ペア（known_combos）に対する問い合わせ・登録を担当"""

    def __init__(self, db_path: str = "proverb_solver.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS known_combos (
                pattern TEXT PRIMARY KEY
            )
            """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def _pattern_key(a: str, b: str) -> str:
        """選択順に依存しないキーを作る（sortして連結）。"""
        return "|||".join(sorted([a, b]))

    def exists(self, a: str, b: str) -> bool:
        """a, b の組み合わせが既知の正解パターンとして登録済みか判定する。"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM known_combos WHERE pattern = ?",
            (self._pattern_key(a, b),),
        )
        found = cur.fetchone() is not None
        conn.close()
        return found

    def register(self, a: str, b: str) -> None:
        """ブルートフォースで判明した正解パターンを登録する。"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR IGNORE INTO known_combos (pattern) VALUES (?)",
            (self._pattern_key(a, b),),
        )
        conn.commit()
        conn.close()