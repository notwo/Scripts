# -*- coding: utf-8 -*-
"""
ProverbRepository
==================

「ことわざの正解ペア」をSQLiteに永続化するリポジトリ。
IdiomRepository と同様、ProverbSolver からはこのクラス経由でのみ
DBにアクセスする。

テーブル定義
------------
proverbs(pattern TEXT PRIMARY KEY)

pattern は、正解ペアの2断片を sorted() で順序を揃えてから
"|||" で連結した文字列。選択順に依存せず同一パターンとして
照合できるようにするための正規化。
"""

import sqlite3
from pathlib import Path


class ProverbRepository:
    """ことわざの正解ペア（proverbs）に対する問い合わせ・登録を担当"""

    def __init__(self, db_path: str = "proverb_solver.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS proverbs (
                pattern TEXT PRIMARY KEY
            )
            """
        )
        self._conn.commit()

    @staticmethod
    def _pattern_key(a: str, b: str) -> str:
        """選択順に依存しないキーを作る（sortして連結）。"""
        return "|".join(sorted([a, b]))

    def exists(self, a: str, b: str) -> bool:
        """a, b の組み合わせが既知の正解パターンとして登録済みか判定する。"""
        cur = self._conn.cursor()
        cur.execute(
            "SELECT 1 FROM proverbs WHERE pattern = ?",
            (self._pattern_key(a, b),),
        )
        found = cur.fetchone() is not None
        return found

    def register(self, a: str, b: str) -> None:
        """ブルートフォースで判明した正解パターンを登録する。"""
        self._conn.execute(
            "INSERT OR IGNORE INTO proverbs (pattern) VALUES (?)",
            (self._pattern_key(a, b),),
        )
        self._conn.commit()
        self._conn.close()

    def register_many(self, patterns: list[str]) -> None:
        """ことわざを複数件まとめて登録"""
        self._conn.executemany(
            "INSERT OR IGNORE INTO proverbs (pattern) VALUES (?)",
            [(w,) for w in patterns],
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "ProverbRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()