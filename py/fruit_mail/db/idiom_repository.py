"""三字熟語データを管理するSQLite3リポジトリ"""
import sqlite3
from pathlib import Path


class IdiomRepository:
    """
    三字熟語(idioms)テーブルへのアクセスを担当する。

    スキーマ:
        idioms(word TEXT PRIMARY KEY)  -- word は3文字の熟語（例: "熱帯魚"）
    """

    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idioms (
                word TEXT PRIMARY KEY
            )
            """
        )
        self._conn.commit()

    def exists(self, word: str) -> bool:
        """3文字完全一致で熟語が存在するか"""
        cur = self._conn.execute(
            "SELECT 1 FROM idioms WHERE word = ? LIMIT 1", (word,)
        )
        return cur.fetchone() is not None

    def has_prefix(self, prefix: str) -> bool:
        """指定した文字列で始まる熟語が存在するか（枝刈り用の前方一致検索）"""
        cur = self._conn.execute(
            "SELECT 1 FROM idioms WHERE word LIKE ? LIMIT 1", (f"{prefix}%",)
        )
        return cur.fetchone() is not None

    def add(self, word: str) -> None:
        """熟語を1件登録（既存なら無視）"""
        self._conn.execute("INSERT OR IGNORE INTO idioms (word) VALUES (?)", (word,))
        self._conn.commit()

    def add_many(self, words: list[str]) -> None:
        """熟語を複数件まとめて登録"""
        self._conn.executemany(
            "INSERT OR IGNORE INTO idioms (word) VALUES (?)",
            [(w,) for w in words],
        )
        self._conn.commit()

    def exists(self, word: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM idioms WHERE word = ? LIMIT 1",
            (word,),
        ).fetchone()
        return row is not None

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "IdiomRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()