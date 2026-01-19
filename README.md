<!--
SPDX-License-Identifier: MIT
Copyright (c) 2020 icecake0141
-->

<!--
This file was created or modified with the assistance of an AI (Large Language Model). Review for correctness and security.
-->

# Linguafrancatto

DeepLをバックエンドとして使用するSlack用言語翻訳ボットです。

## 概要

このボットは、特定のベースネームを持つチャネル間で翻訳されたメッセージを自動的に投稿する機能、または特定のキーワードでトリガーされた翻訳メッセージを投稿する機能を持っています。メッセージの監視メカニズムとしてSlackのEvent APIを使用しているため、エンドポイントWebサーバーとして動作し、Google App Engine上で実行するように設計されていますが、オンプレミス環境でも実行できます。このプロジェクトは、Slack Bolt SDK for Pythonを使用して作成されました。

## 必要なもの

* DeepL APIキー（DeepL APIプランの有効なサブスクリプション）
* Slack Bot TokenとSlack Signing Secret（Slackワークスペースへの管理者アクセス）
* Python 3.8以上

### 使用技術

* [Slack Bolt for Python](https://github.com/slackapi/bolt-python)
* [Flask](https://flask.palletsprojects.com/)
* [DeepL API](https://www.deepl.com/docs-api/introduction/)

## 環境変数

以下の環境変数を設定する必要があります（`env_variables.yaml`ファイルまたはシステム環境変数として）：

| 環境変数名 | 説明 | 必須 |
|-----------|------|------|
| `DEEPL_TOKEN` | DeepL APIの認証トークン | はい |
| `SLACK_SIGNING_SECRET` | Slack Appの署名シークレット | はい |
| `SLACK_BOT_TOKEN` | Slack Botのトークン | はい |
| `MULTI_CHANNEL` | 継続的な翻訳が必要なSlackチャネルベースネームのカンマ区切りリスト | はい |
| `DEBUG_MODE` | デバッグモード（`True` または `False`） | いいえ（デフォルト: False） |
| `PORT` | サーバーのポート番号 | いいえ（デフォルト: 3000） |
| `GUARDIAN_UID` | ボット管理者のSlack UID | いいえ |
| `PROJECT_ID` | Google Secret ManagerプロジェクトID | いいえ |
| `SECRET_NAME` | Google Secret Managerシークレット名 | いいえ |
| `SECRET_VERSION` | Google Secret Managerシークレットバージョン | いいえ |

## インストール

1. リポジトリをクローンします：
   ```sh
   git clone https://github.com/icecake0141/linguafrancatto.git
   cd linguafrancatto
   ```

2. 依存関係をインストールします：
   ```sh
   pip install -r requirements.txt
   ```

3. `env_variables.yaml.sample`を参考に`env_variables.yaml`を作成し、必要な環境変数を設定します。

## ローカルでの実行

1. 環境変数を設定します（`.env`ファイルまたはシステム環境変数として）。

2. アプリケーションを起動します：
   ```sh
   python main.py
   ```

3. デフォルトではポート3000でサーバーが起動します。`PORT`環境変数で変更可能です。

4. Slack Event APIのエンドポイント：`http://your-server:3000/slack/events`

## SlackとDeepLのセットアップ

### Slack App設定

1. [Slack API](https://api.slack.com/apps)で新しいアプリを作成します。
2. **OAuth & Permissions**で以下のBot Token Scopesを追加：
   - `channels:history` - チャネルメッセージの読み取り
   - `channels:read` - チャネル情報の読み取り
   - `chat:write` - メッセージの送信
   - `users:read` - ユーザー情報の読み取り
3. **Event Subscriptions**を有効にし、Request URLを設定：`https://your-server/slack/events`
4. **Subscribe to bot events**で`message.channels`を追加します。
5. アプリをワークスペースにインストールし、Bot User OAuth Tokenを取得します。

### DeepL API設定

1. [DeepL API](https://www.deepl.com/pro-api)でアカウントを作成します。
2. APIキーを取得し、`DEEPL_TOKEN`環境変数に設定します。

## 使用方法

### キーワードトリガー翻訳

メッセージ内に以下のキーワードを含めると、そのメッセージが指定された言語に翻訳されます：

- **Nyan** - 日本語に翻訳
- **Meow** - 英語に翻訳
- **Miaou** - フランス語に翻訳
- **Мяу** - ロシア語に翻訳

例：
```
Hello, how are you? Nyan
```
このメッセージは日本語に翻訳されます。

### マルチチャネル自動翻訳

`MULTI_CHANNEL`環境変数に設定されたベースネームを持つチャネルでは、メッセージが自動的に翻訳されます。

例：`MULTI_CHANNEL=general`の場合
- `general`（または`general-ja`） - 日本語チャネル
- `general-en` - 英語チャネル
- `general-fr` - フランス語チャネル

いずれかのチャネルに投稿されたメッセージは、他の言語チャネルに自動的に翻訳されて投稿されます。

### 使用状況の確認

チャネルに`Meousage`と投稿すると、DeepL APIの使用状況が表示されます。

## Google App Engineへのデプロイ

1. `app.yaml`ファイルを確認し、必要に応じて設定を調整します。

2. `env_variables.yaml`に環境変数を設定します（`env_variables.yaml.sample`を参考に）。

3. Google Cloud SDKがインストールされていることを確認します。

4. デプロイを実行：
   ```sh
   gcloud app deploy
   ```

5. ログを確認：
   ```sh
   gcloud app logs tail -s default
   ```

## 開発とテスト

### デバッグモード

`DEBUG_MODE=True`を設定すると、詳細なログ出力が有効になります。

### コードのフォーマット

```sh
black .
```

### リンティング

```sh
ruff check .
```

### テスト

このプロジェクトには自動化されたユニットテストが含まれています。

テストを実行するには：

```sh
# テスト依存関係がインストールされていることを確認
pip install -r requirements.txt

# すべてのテストを実行
pytest

# カバレッジレポート付きでテストを実行
pytest --cov=main --cov-report=html

# 特定のテストクラスを実行
pytest tests/test_main.py::TestMarkdownFunctions -v

# 特定のテストを実行
pytest tests/test_main.py::TestMarkdownFunctions::test_replace_markdown_bold -v
```

テストには以下が含まれます：
- マークダウン変換関数のテスト (`replace_markdown`、`revert_markdown`)
- DeepL API関数のテスト (モック付き)
- Flaskエンドポイントのテスト

手動でテストする場合は、Slackワークスペースで実際にメッセージを送信して動作を確認してください。

## セキュリティ

- **環境変数**: APIトークンやシークレットは環境変数として管理し、ソースコードにハードコーディングしないでください。
- **HTTPS**: 本番環境では必ずHTTPSを使用してください。Slack Event APIはHTTPSエンドポイントを要求します。
- **認証**: Slack Signing Secretを使用してリクエストの真正性を検証します（Slack Bolt SDKが自動的に処理）。
- **Google Secret Manager**: 機密情報の管理には、Google Secret Managerの使用を推奨します。

## ライセンス

このプロジェクトはMITライセンスの下で配布されています。詳細は`LICENSE`ファイルを参照してください。

## リンク

* Project Link: [https://github.com/icecake0141/linguafrancatto](https://github.com/icecake0141/linguafrancatto)

## 参考資料

* [DeepL API Documentation](https://www.deepl.com/docs-api/introduction/)
* [Slack API](https://api.slack.com/)
* [Slack Bolt for Python - Getting Started](https://slack.dev/bolt-python/tutorial/getting-started)
* [Slack Bolt with Google App Engine and Flask](https://github.com/slackapi/bolt-python/blob/main/examples/google_app_engine/flask/main.py)
* [Google App Engine Python 3 Runtime](https://cloud.google.com/appengine/docs/standard/python3/runtime)

## 謝辞

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/)
