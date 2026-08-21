"""
既知のことわざをあらかじめDBに登録するスクリプト。

使い方:
    python3 seed_proverbs.py

SEED_PROVERBS に登録したいことわざを "前の文字列|後ろの文字列" の形式で
追加してから実行してください（例: "念には|念を入れよ"）。
"""
from db.proverb_repository import ProverbRepository
from pathlib import Path


# ここに事前にわかっていることわざを追加してください（"前半|後半" の形式）
SEED_PROVERBS = [
]


def main() -> None:
    db_path = Path("./db/campus.db").resolve()

    valid_proverbs = [w for w in SEED_PROVERBS]
    if len(valid_proverbs) == 0:
        return

    with ProverbRepository(db_path) as repo:
        print(f"登録対象: {len(valid_proverbs)}件")

        # DBに既に存在することわざを確認
        existing = [w for w in valid_proverbs if repo.exists(*w.split('|'))]

        if existing:
            print(f"⚠ 既にDBに存在するため登録されないことわざ: {existing}")
        else:
            print("✓ DB上の重複なし")

        repo.register_many(valid_proverbs)
        print(f"{len(valid_proverbs)}件を登録しました（DB: {db_path}）")


if __name__ == "__main__":
    main()