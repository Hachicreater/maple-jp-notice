<h2 align="center">
  🍁 MapleStory Notice Monitor
</h2>
メイプルストーリー公式サイトの「お知らせ」を24時間監視し、更新があればDiscordへ即座に通知するシステムです。 </p>
JavaScriptで動的に生成される公式サイトの構造を突破するため、Playwright (ヘッドレスブラウザ) を採用しています。</p>
</p>
<h2>🚀 主な機能</h2>
<ul>
    <li><b>JavaScript レンダリング対応</b>:<br>Playwright により、ブラウザ上で読み込まれた後のお知らせ一覧を確実に取得します。</li>
    <li><b>カテゴリ判別機能</b>:<br>【お知らせ】【イベント】【ショップ】【メンテナンス】などのカテゴリを自動で取得し、通知に含めます。</li>
    <li><b>重複通知の防止</b>:<br>過去 50 件分の通知履歴を <code>last_id.txt</code> に保持し、同じ記事が何度も通知されるのを防ぎます。</li>
    <li><b>柔軟な通知先管理</b>:<br>GitHub の変数（Variables）にリスト形式で Webhook を登録することで、複数の Discord チャンネルへ同時に通知できます。</li>
</ul>

<h2>🛠 セットアップ方法</h2>
<h3>1. リポジトリの権限設定</h3>
<p>GitHub Actions が通知履歴（<code>last_id.txt</code>）を保存できるように設定を変更する必要があります。</p>
<ol>
  <li>リポジトリの <b>[Settings]</b> &gt; <b>[Actions]</b> &gt; <b>[General]</b> を開きます。</li>
  <li>最下部の <b>[Workflow permissions]</b> で <b>「Read and write permissions」</b> を選択して保存します。</li>
</ol>
<h3>2. Webhook URL の登録</h3>
  <p>通知を飛ばしたい Discord の Webhook URL を登録します。</p>
  <ol>
    <li>リポジトリの <b>[Settings]</b> &gt; <b>[Secrets and variables]</b> &gt; <b>[Actions]</b> を開きます。</li>
    <li><b>[Variables]</b> タブ（Secrets の隣）を選択し、<b>[New repository variable]</b> をクリックします。</li>
    <li>以下の内容で作成します。
    <ul>
      <li><b>Name</b>: <code>DISCORD_WEBHOOK_LIST</code></li>
      <li><b>Value</b>: <code>["ここにWebhook URLを記入"]</code></li>
      <li>※ URLが複数ある場合は <code>["URL1", "URL2"]</code> のようにカンマで区切って記述してください。</li>
    </ul>
  </li>
  </ol>
<h2>📂 ファイル構成</h2>
<ul>
  <li><code>maple_notice.py</code>: 監視プログラム本体。Playwright を使用してページを解析します。</li>
  <li><code>.github/workflows/check_news.yml</code>: 自動実行スケジュール設定。10分おきに自動巡回します。</li>
  <li><code>last_id.txt</code>: 通知済み記事の ID 履歴（最大50件保持）。</li>
</ul>
<h2>⚠️ 運用上の注意</h2>
<ul>
  <li><b>初回実行時</b>: 履歴がない状態で実行すると、現在の最新 20 件を履歴として登録（初期化）し、通知は行いません。</li>
  <li><b>通知テスト</b>: <code>last_id.txt</code> の内容を消去して <b>[Actions]</b> タブから <b>「Run workflow」</b> を手動実行すると、最新記事が新着として通知されます。</li>
  <li><b>エラー対応</b>: ログに「Webhook設定が読み込めません」と出る場合は、<code>Variables</code> の入力形式が <code>["URL"]</code> になっているか確認してください。</li>
</ul>
