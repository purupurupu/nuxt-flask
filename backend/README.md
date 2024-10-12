# README

## セットアップ

1. 仮想環境を作成し、アクティベートします：
   ```
   python -m venv venv
   source venv/bin/activate  # Linuxの場合
   venv\Scripts\activate  # Windowsの場合
   ```

2. 依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```

3. アプリケーションを実行します：
   ```
   python app.py
   ```

## 開発

- `app.py`: メインアプリケーションファイル
- `requirements.txt`: 依存関係リスト
- `GoogleCloud`: 認証はjsonを.envに書く。