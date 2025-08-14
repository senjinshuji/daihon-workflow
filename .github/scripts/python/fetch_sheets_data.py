#!/usr/bin/env python3
"""
Google Sheetsからデータを取得するスクリプト
サービスアカウント認証を使用
"""

import json
import os
import sys
import csv
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def setup_credentials():
    """サービスアカウント認証をセットアップ"""
    # 環境変数からJSONを取得
    service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
    
    if service_account_json:
        # JSON文字列から認証情報を作成
        service_account_info = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    elif os.path.exists('service-account.json'):
        # ファイルから認証情報を作成
        credentials = service_account.Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    else:
        raise ValueError("サービスアカウント認証情報が見つかりません")
    
    return credentials

def fetch_sheet_data(spreadsheet_id, range_name, credentials):
    """Google Sheetsからデータを取得"""
    try:
        service = build('sheets', 'v4', credentials=credentials)
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print(f"No data found in range: {range_name}", file=sys.stderr)
            return []
        
        return values
        
    except HttpError as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        return []

def save_to_csv(data, output_path, sheet_name):
    """データをCSVファイルとして保存"""
    if not data:
        print(f"No data to save for {sheet_name}", file=sys.stderr)
        return False
    
    output_file = Path(output_path) / f"{sheet_name}.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
    print(f"Saved {len(data)} rows to {output_file}", file=sys.stderr)
    return True

def main():
    """メイン処理"""
    # コマンドライン引数から商品名を取得
    if len(sys.argv) < 2:
        print("Usage: python fetch_sheets_data.py <product_name>", file=sys.stderr)
        sys.exit(1)
    
    product_name = sys.argv[1]
    
    # Google Sheets IDを環境変数から取得（デフォルト値あり）
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID', '1Bm8xgoAeocPhiPoisVt1uMc0MTEuH70SDME4N1bg6mo')
    
    # 認証セットアップ
    try:
        credentials = setup_credentials()
        print("Authentication successful", file=sys.stderr)
    except Exception as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 取得するシートと範囲の定義
    # スプレッドシートの実際のシート名 → 出力CSVファイル名のマッピング
    sheets_to_fetch = {
        'market_bestsellers': 'レジェンド台本!A:Z',  # 市場ベストセラー
        'internal_top_group': '【配信結果】上位!A:Z',  # 高パフォーマンス台本
        'internal_middle_group': '【配信結果】中位!A:Z',  # 中パフォーマンス台本
        'internal_bottom_group': '【配信結果】下位!A:Z'  # 低パフォーマンス台本
    }
    
    # 出力ディレクトリ
    output_dir = f"{product_name}/data"
    
    # 各シートからデータを取得して保存
    success_count = 0
    for sheet_name, range_name in sheets_to_fetch.items():
        print(f"Fetching {sheet_name}...", file=sys.stderr)
        data = fetch_sheet_data(spreadsheet_id, range_name, credentials)
        
        if save_to_csv(data, output_dir, sheet_name):
            success_count += 1
    
    # GitHub Actions出力（標準出力のみ、key=value形式）
    print(f"Successfully fetched {success_count}/{len(sheets_to_fetch)} sheets", file=sys.stderr)
    print(f"completed=true")
    print(f"sheets_fetched={success_count}")
    
    return 0 if success_count == len(sheets_to_fetch) else 1

if __name__ == "__main__":
    sys.exit(main())