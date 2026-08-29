#!/usr/bin/env python3
"""
バッチ処理スクリプト — 指定されたバッチ番号のキーワードペアを処理
使用例: python3 process_batch.py 2
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# キーワードリスト（全28個）
KEYWORDS = [
    "AI SEO記事作成 代行",                      # 1
    "AI ライティング代行 格安",                  # 2
    "SEO記事 作成代行 安い",                    # 3
    "AI SEO記事 ツール 会社",                   # 4
    "SEO記事 量産 代行 会社",                   # 5
    "AIライティング SaaS 比較",                # 6
    "記事作成 自動生成 サービス",                # 7
    "SEO記事 外注 安い おすすめ",               # 8
    "AI SEO対策記事 作成 業者",                # 9
    "SEO記事 丸投げ 代行",                     # 10
    "コンテンツSEO 記事作成 AI 業者",          # 11
    "SEO記事 作成し放題",                      # 12
    "AI記事作成 作成し放題",                   # 13
    "記事作成代行 無制限",                     # 14
    "AI ライティング 無制限",                  # 15
    "SEO記事 何記事でも",                      # 16
    "記事作成 月額固定 使い放題",               # 17
    "AI記事作成 定額 無制限",                  # 18
    "SEO記事 サブスク 使い放題",               # 19
    "コンテンツ制作 使い放題",                  # 20
    "記事作成代行 何本でも 定額",               # 21
    "AI記事作成 やり放題",                     # 22
    "SEO対策記事 発注し放題",                  # 23
    "記事作成 依頼し放題",                     # 24
    "ライティング 依頼無制限",                  # 25
    "SEO記事 いくらでも作れる",                # 26
    "AI記事作成 本数制限なし",                 # 27
    "記事作成代行 上限なし 月額",              # 28
]

WORK_DIR = Path("/Users/ty_macbookair/Downloads/SEOツール会社作業用")
RESULTS_JSON = WORK_DIR / "data" / "results.json"
BUILD_EXCEL_PY = WORK_DIR / "build_excel.py"

def get_keywords_for_batch(batch_num):
    """バッチ番号からキーワードペアを取得"""
    kw_idx1 = (batch_num - 1) * 2
    kw_idx2 = kw_idx1 + 1
    if kw_idx2 >= len(KEYWORDS):
        return None, None
    return KEYWORDS[kw_idx1], KEYWORDS[kw_idx2]

def log(msg):
    """ログ出力"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {msg}")

def load_results():
    """results.json を読み込む"""
    if RESULTS_JSON.exists():
        with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_results(data):
    """results.json に保存"""
    with open(RESULTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_keyword(keyword, batch_num, rank_offset):
    """キーワード1つを処理（WebSearch → WebFetch）"""
    log(f"バッチ{batch_num} キーワード処理開始: {keyword}")

    # WebSearch を実行
    result = subprocess.run(
        [
            "python3", "-c",
            f"""
import json
import subprocess
import sys

query = {json.dumps(keyword)}

# Claude Code の WebSearch 実行を Bash で実行（subprocess 経由）
result = subprocess.run(
    ['python3', '-m', 'claude_sdk', 'web-search', query],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"Error: {{result.stderr}}", file=sys.stderr)
    sys.exit(1)

# 結果を JSON として解析
try:
    data = json.loads(result.stdout)
    for item in data.get('results', []):
        print(json.dumps({{
            'title': item.get('title', ''),
            'url': item.get('url', '')
        }}))
except Exception as e:
    print(f"Parse error: {{e}}", file=sys.stderr)
    sys.exit(1)
"""
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        log(f"  ⚠ WebSearch 失敗: {result.stderr}")
        return []

    # 結果をパース
    rows = []
    for line in result.stdout.strip().split('\n'):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            rows.append({
                "検索キーワード": keyword,
                "リスティングorオーガニック": "オーガニック",
                "表示順位": rank_offset,
                "会社名": "取得不可",
                "サービス名": "取得不可",
                "URL": item.get('url', 'N/A'),
                "特徴": "取得不可",
                "費用": "取得不可"
            })
            rank_offset += 1
        except json.JSONDecodeError:
            pass

    if rows:
        log(f"  ✓ {len(rows)} 件取得")
    return rows

def process_batch(batch_num):
    """バッチを処理"""
    log(f"===== バッチ{batch_num} 開始 =====")

    kw1, kw2 = get_keywords_for_batch(batch_num)
    if kw1 is None:
        log(f"✗ バッチ{batch_num} は存在しません")
        return False

    log(f"処理キーワード: {kw1}, {kw2}")

    # 既存データを読み込む
    existing_data = load_results()
    new_rows = []

    # キーワード1を処理
    rows1 = process_keyword(kw1, batch_num, 1)
    new_rows.extend(rows1)

    # キーワード2を処理
    rows2 = process_keyword(kw2, batch_num, 1)
    new_rows.extend(rows2)

    # データを保存
    all_data = existing_data + new_rows
    save_results(all_data)
    log(f"✓ {len(new_rows)} 件のデータを追加（累計: {len(all_data)}件）")

    # Excel を再生成
    result = subprocess.run(['python3', str(BUILD_EXCEL_PY)], capture_output=True, text=True)
    if result.returncode == 0:
        log(result.stdout.strip())
    else:
        log(f"✗ Excel 生成エラー: {result.stderr}")
        return False

    log(f"===== バッチ{batch_num} 完了 =====\n")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"使用法: python3 {sys.argv[0]} <バッチ番号>")
        print(f"例: python3 {sys.argv[0]} 2")
        sys.exit(1)

    try:
        batch_num = int(sys.argv[1])
    except ValueError:
        print(f"バッチ番号は整数である必要があります")
        sys.exit(1)

    success = process_batch(batch_num)
    sys.exit(0 if success else 1)
