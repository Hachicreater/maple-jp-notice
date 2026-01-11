import os
import json
import requests
from playwright.sync_api import sync_playwright

# --- 設定 ---
TARGET_URL = "https://maplestory.nexon.co.jp/notice/list/"
LAST_ID_FILE = "last_id.txt"
WEBHOOK_URLS_JSON = os.environ.get("DISCORD_WEBHOOK_JSON", "[]")
HISTORY_LIMIT = 50 # 保持する履歴の数

def get_latest_notices():
    """ブラウザを起動し、カテゴリとタイトルを抽出する"""
    notices = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print(f"【ログ】アクセス中: {TARGET_URL}")
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            page.wait_for_selector("table.notice-list", timeout=30000)
            
            rows = page.query_selector_all("table.notice-list tr")
            for row in rows:
                cat_elem = row.query_selector("td.category")
                link_elem = row.query_selector("td.ttl a")
                
                if cat_elem and link_elem:
                    category = cat_elem.inner_text().strip()
                    title = link_elem.inner_text().strip()
                    href = link_elem.get_attribute("href")
                    
                    if "alias=" in href:
                        # URLからID(alias)を抽出
                        import urllib.parse
                        query = urllib.parse.urlparse(href).query
                        params = urllib.parse.parse_qs(query)
                        alias = params.get('alias', [None])[0]
                        
                        if alias:
                            notices.append({
                                "id": alias,
                                "title": title,
                                "url": f"https://maplestory.nexon.co.jp{href}",
                                "category": category
                            })
        except Exception as e:
            print(f"【エラー】取得失敗: {e}")
        finally:
            browser.close()
    return notices

def main():
    # Webhook設定確認
    try:
        webhook_urls = json.loads(WEBHOOK_URLS_JSON)
    except:
        print("【エラー】Webhook設定が読み込めません。")
        return

    # 記事取得
    notices = get_latest_notices()
    if not notices:
        return

    # 取得結果をログに表示（カテゴリ確認用）
    print(f"【ログ】取得成功: {len(notices)}件")
    for i, n in enumerate(notices[:5]): # 最初の5件を詳細表示
        print(f"  [{i+1}] 【{n['category']}】 {n['title']}")

    # 履歴（過去50件のID）の読み込み
    history_ids = []
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            history_ids = [line.strip() for line in f.readlines() if line.strip()]

    # 通知対象の抽出（履歴に存在しないIDのみ）
    new_notices = [n for n in notices if n["id"] not in history_ids]

    # 初回実行時（履歴が空またはreset時）は保存のみ
    if not history_ids or history_ids[0] == "reset":
        # 現在取得した全IDを履歴として保存して終了
        new_history = [n["id"] for n in notices][:HISTORY_LIMIT]
        with open(LAST_ID_FILE, "w") as f:
            f.write("\n".join(new_history))
        print("【ログ】初期化完了。現在の記事を履歴に登録しました。")
        return

    if not new_notices:
        print("【ログ】新着記事はありません。")
    else:
        print(f"【ログ】新着通知: {len(new_notices)}件")
        for n in reversed(new_notices):
            payload = {
                "content": f"**【{n['category']}】**\n{n['title']}\n{n['url']}"
            }
            for url in webhook_urls:
                try:
                    requests.post(url, json=payload, timeout=10)
                except: pass

        # 履歴の更新（新しいIDを先頭に追加し、最大50件に絞る）
        current_ids = [n["id"] for n in notices]
        # 現在のIDリスト + 過去のIDリスト を合体させて重複削除
        updated_history = list(dict.fromkeys(current_ids + history_ids))[:HISTORY_LIMIT]
        
        with open(LAST_ID_FILE, "w") as f:
            f.write("\n".join(updated_history))

if __name__ == "__main__":
    main()
