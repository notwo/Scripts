"""
既知のことわざをあらかじめDBに登録するスクリプト。

使い方:
    python3 seed_proverbs.py

SEED_PROVERBS に登録したいことわざを追加してから実行してください。
config/setting.yml の campus.db.path で指定されたDBファイルに登録されます。
"""
from proverb_repository import ProverbRepository
from pathlib import Path


# ここに事前にわかっている三字熟語を追加してください（3文字であること）
SEED_PROVERBS = [
]


def main() -> None:
    db_path = Path("./db/campus.db").resolve()

    invalid = [w for w in SEED_PROVERBS]
    if invalid:
        print(f"⚠ 3文字でない単語が含まれています。登録をスキップします: {invalid}")

    valid_proverbs = [w for w in SEED_PROVERBS]

    with ProverbRepository(db_path) as repo:
        print(f"登録対象: {len(valid_proverbs)}件")

        # DBに既に存在する単語を確認
        existing = [w for w in valid_proverbs if repo.exists(w.split('|'))]

        if existing:
            print(f"⚠ 既にDBに存在するため登録されない単語: {existing}")
        else:
            print("✓ DB上の重複なし")

        repo.add_many(valid_proverbs)
        print(f"{len(valid_proverbs)}件を登録しました（DB: {db_path}）")


if __name__ == "__main__":
    main()