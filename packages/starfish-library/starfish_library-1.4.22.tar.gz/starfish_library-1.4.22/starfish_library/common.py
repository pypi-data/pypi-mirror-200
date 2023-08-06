from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import json
import tweepy
import requests
from datetime import datetime, timedelta, timezone
from google.cloud import storage
import urllib.request
import urllib.parse
import time
from google.ads.googleads.client import GoogleAdsClient


def set_env_variables():
    if os.name == 'nt':
        local_secret_file_folder_path = 'E:/WorkSpace/Codes'
        env_variable_path = f'{local_secret_file_folder_path}/env.json'
    elif os.name == 'posix':
        env_variable_path = '/env/env'

    with open(env_variable_path, "r") as file:
        dict = json.load(file)
        for key, value in dict.items():
            os.environ[key] = value


def gcp_secret_manager():
    if os.name == 'nt':
        local_secret_file_folder_path = 'E:/WorkSpace/Codes'
        google_cloud_secret_path = f'{local_secret_file_folder_path}/service_account.json'
    elif os.name == 'posix':
        google_cloud_secret_path = '/secret/gcp_service_account'

    # GCP認証用のファイルパス
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_cloud_secret_path

    return google_cloud_secret_path


def google_ads_secret():
    if os.name == 'nt':
        local_secret_file_folder_path = 'E:/WorkSpace/Codes'
        google_ads_secret_path = f'{local_secret_file_folder_path}/oath.yaml'
    elif os.name == 'posix':
        google_ads_secret_path = '/google_ads/google_ads_oauth'

    return google_ads_secret_path


def test():
    print('hoge')


# Twitterで利用
# v1.1 に対応
def generate_twitter_api(CK, CKS, AT, ATS):
    gcp_secret_manager()
    auth = tweepy.OAuthHandler(CK, CKS)
    auth.set_access_token(AT, ATS)
    return tweepy.API(auth, wait_on_rate_limit=True)


# GCPの認証を戻す関数
def generate_google_service_auth(service):
    if service == "spreadsheet":
        a_api = 'https://spreadsheets.google.com/feeds'
        b_api = 'https://www.googleapis.com/auth/drive'
        SCOPES = [a_api, b_api]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            gcp_secret_manager(), SCOPES)

        google_service_auth = gspread.authorize(credentials)

    elif service == "googleads":
        google_ads_client = GoogleAdsClient.load_from_storage(
            google_ads_secret())
        google_service_auth = google_ads_client.get_service(
            "GoogleAdsService", version="v13")
    else:
        print("サービス未選択")
        return False

    return google_service_auth


# Feedly のアクセストークンを返す
def generate_feedly_token():
    gcp_secret_manager()
    url = 'https://cloud.feedly.com/v3/auth/token'
    params = {
        'client_id': 'feedlydev',
        'client_secret': 'feedlydev',
        'grant_type': 'refresh_token',
        'refresh_token': os.environ['FEEDLY_REFRESH_TOKEN'],
    }

    headers = {
        'Content-Type': 'application/json',
    }

    res = requests.post(url, headers=headers, params=params).json()
    return res['access_token']


# 現在日時情報の取得
# 引数のサンプル '%Y/%m/%d'
def make_date_info(format):
    JST = timezone(timedelta(hours=+9), 'JST')
    dt_now_name = datetime.now(JST).strftime(format)
    return dt_now_name


# クラウドストレージへのアップロード
# bucket > アップロードしたいストレージのバスケット名
# blob > バスケット名を除く､アップロード対象のパス
def uplaod_storage(bucket_name, blob_path, upload_file_path):
    gcp_secret_manager()
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(upload_file_path)
    return f'https://storage.cloud.google.com/{bucket_name}/{blob_path}?authuser=1'


# クラウドストレージからのダウンロード
# bucket > ストレージのバスケット名
# blob > バスケット名を除く､ダウンロード先のパス
def downlaod_storage(bucket_name, blob_path, download_file_path):
    gcp_secret_manager()
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.download_to_filename(download_file_path)
    return download_file_path


# YahooAPiに関して

# APIコールに必要なトークンの発行
def generate_yahoo_token():
    gcp_secret_manager()
    url = 'https://biz-oauth.yahoo.co.jp/oauth/v1/token?'
    param = {
        'grant_type': 'refresh_token',
        'client_id': os.environ['YAHOO_ADS_CLIENT_ID'],
        'client_secret': os.environ['YAHOO_ADS_CLIENT_SECRET'],
        'refresh_token': os.environ['YAHOO_ADS_REFRESH_TOKEN']
    }

    params = urllib.parse.urlencode(param)
    token_url = url + params

    with urllib.request.urlopen(token_url) as response:
        body = json.loads(response.read())
        token = body['access_token']

    return token


# MCCに紐づくアカウントIDの取得
# token = generate_yahoo_token()
def get_yahoo_account_ids(token):
    serviceType = 'AccountLinkService/get'
    url = 'https://ads-search.yahooapis.jp/api/v6/' + serviceType

    request_header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    request_data = json.dumps({
        'managerAccountId': os.environ['YAHOO_ADS_MCC_ID']
    })

    request = urllib.request.Request(
        url, data=request_data.encode(),
        method='POST',
        headers=request_header
    )

    try:
        with urllib.request.urlopen(request) as response:
            status = response.getcode()
            if status == 200:
                body = json.loads(response.read())

                if body['errors'] is not None:
                    return False

                infos = body['rval']['values']
                account_ids = []
                for info in infos:
                    account_ids.append(info['accountLink']['accountId'])
                return account_ids

    except urllib.error.URLError as e:
        print(e.reason)


# レポートを作成キューに追加
def add_rerort(token, date, account_id, report_type, fields):
    serviceType = 'ReportDefinitionService/add'
    base_url = 'https://ads-search.yahooapis.jp/api/v6/'
    request_url = base_url + serviceType

    request_data = json.dumps(
        {
            'accountId': account_id,
            "operand": [{
                "dateRange": {
                    "endDate": date,
                    "startDate": date
                },
                "fields": fields,
                "reportDateRangeType": "CUSTOM_DATE",
                "reportLanguage": "EN",
                "reportName": account_id,
                "reportType": report_type
            }]
        }
    )

    # Template
    request_header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    request_url = base_url + serviceType

    request = urllib.request.Request(
        request_url,
        data=request_data.encode(),
        method='POST',
        headers=request_header
    )
    # Template

    with urllib.request.urlopen(request) as response:
        body = json.loads(response.read())
        report_job_id = body['rval']['values'][0]['reportDefinition']['reportJobId']
        return report_job_id


# レポート作成キューに追加されているサポートの作成状況の確認
def check_rerort_status(token, account_id, report_job_id):
    serviceType = 'ReportDefinitionService/get'
    base_url = 'https://ads-search.yahooapis.jp/api/v6/'
    request_url = base_url + serviceType

    request_data = json.dumps({
        'accountId': account_id,
        'reportJobIds': [report_job_id],
    })

    # Template
    request_header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    request_url = base_url + serviceType

    request = urllib.request.Request(
        request_url,
        data=request_data.encode(),
        method='POST',
        headers=request_header
    )
    # Template

    while True:
        time.sleep(1)
        try:
            with urllib.request.urlopen(request) as response:
                body = json.loads(response.read())
                reportJobStatas = body['rval']['values'][0]
                reportJobStatas = reportJobStatas['reportDefinition']['reportJobStatus']

                print(f'{reportJobStatas} > {account_id}')
                if reportJobStatas == 'COMPLETED':
                    return True

        except Exception as e:
            print(e)


# レポート作成キューで完了になったレポート情報をダウンロード
def download_rerort(token, account_id, report_job_id, fields):
    serviceType = 'ReportDefinitionService/download'
    base_url = 'https://ads-search.yahooapis.jp/api/v6/'
    request_url = base_url + serviceType

    request_data = json.dumps({
        'accountId': account_id,
        'reportJobId': report_job_id
    })

    # Template
    request_header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    request_url = base_url + serviceType

    request = urllib.request.Request(
        request_url,
        data=request_data.encode(),
        method='POST',
        headers=request_header
    )
    # Template

    with urllib.request.urlopen(request) as response:
        csv_body = response.read().decode("utf-8")
        rows = csv_body.split("\n")
        concat_dict_array = []
        for j in range(1, len(rows) - 2):
            row = rows[j].split(',')
            array = {}
            for i, value in enumerate(row):
                key = fields[i]
                array[f'{key}'] = value

            concat_dict_array.append(array)

        if concat_dict_array:
            return concat_dict_array


# 作成したレポートはもう使わないので削除する関数

def remove_rerort(token, account_id, report_job_id):
    serviceType = 'ReportDefinitionService/remove'
    base_url = 'https://ads-search.yahooapis.jp/api/v6/'
    request_url = base_url + serviceType

    request_data = json.dumps({
        'accountId': account_id,
        "operand": [{
            'reportJobId': report_job_id
        }]
    })

    # Template
    request_header = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    request_url = base_url + serviceType

    request = urllib.request.Request(
        request_url,
        data=request_data.encode(),
        method='POST',
        headers=request_header
    )
    # Template

    with urllib.request.urlopen(request) as response:
        body = json.loads(response.read())
        remove_status = body['rval']['values'][0]['operationSucceeded']
        print(f'レポート削除 : {remove_status} > {account_id}')


# Google MCC から アカウントIDを一括で取得する
def get_google_account_ids(client):
    set_env_variables()
    customer_id = os.environ['GOOGLE_ADS_MCC']
    query = """
        SELECT
            customer_client.currency_code,
            customer_client.descriptive_name,
            customer_client.hidden,
            customer_client.id,
            customer_client.time_zone
        FROM customer_client
        WHERE customer_client.level = 1
            AND customer_client.status = 'ENABLED'"""

    response = client.search(
        customer_id=str(customer_id), query=query)

    accounts = []
    for google_ads_row in response:
        customer_client = google_ads_row.customer_client

        account = {}
        account["account_id"] = customer_client.id
        account["account_name"] = customer_client.descriptive_name

        accounts.append(account)

    return accounts
