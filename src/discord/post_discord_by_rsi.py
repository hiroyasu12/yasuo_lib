# 必要なライブラリの読み込み
import pandas as pd
from datetime import datetime
import requests
import json
import numpy
import python_bitbankcc
import time
import setting_API_env as settingEnv
import os, sys
sys.path.append('../')
#print(os.getcwd())
from src.main import calc_tech_indicator

# インスタンスを定義する
pub = python_bitbankcc.public()

trading_coin = 'btc_jpy'
interval = 300
period = 16
sigma = 1.6
webhook_url = settingEnv.discordAPI

headers = {'Content-Type': 'application/json'}

# cryptowatchのAPIから5分単位のビットコインの価格を取得してデータフレームにする関数


def get_btcprice():
    url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=' + \
        str(interval)+'&after=' + str(int(time.time()-interval * period))
    r = requests.get(url)
    r2 = json.loads(r.text)
    pricedata = []
    for data in r2['result'][str(interval)]:
        dt = datetime.fromtimestamp(data[0])
        price = data[4]
        vol = data[5]
        pricedata.append([dt, price, vol])
    return pd.DataFrame(pricedata, columns=['date', 'price', 'vol'])
##############BOT本体#################


pastd = datetime.today()
eth_df = get_btcprice()
p_list = eth_df['price'].values.tolist()
a = 0
while True:
    # 時刻取得＆判定用に変換
    d = datetime.today()
    #d_hm = d.strptime(d.strftime("%H:%M"), "%H:%M")
    #pastd_hm = pastd.strptime(pastd.strftime("%H:%M"), "%H:%M")
    if True:  # d_hm > pastd_hm :
        # 関数を使ってビットコインの価格データを取得する
        #eth_df = get_btcprice()
        last_price = pub.get_ticker('btc_jpy')
        p_list.append(int(last_price['last']))
        #data = eth_df['price'].values.tolist()
        if len(p_list) > period:
            df_rsi = calc_tech_indicator.calc_rsi(14, p_list)
            last_rsi = float(df_rsi['rsi'][df_rsi['rsi'].size - 1])
            if last_rsi < 20 and a != 1:
                main_content = {
                    "allowed_mentions": {
                        "parse": ["users", "roles"],
                        "users": []
                    },
                    'content': '<@&806199768396595281> BTC/JPYのRSIが20を割りました！買い時かも！'
                }
                response = requests.post(
                    webhook_url, json.dumps(main_content), headers=headers)
                a = 1
            elif last_rsi > 70 and a != 2:
                main_content = {
                    "allowed_mentions": {
                        "parse": ["users", "roles"],
                        "users": []
                    },
                    'content': '<@&806199768396595281> BTC/JPYのRSIが70を超えました！売り時かも！'
                }
                response = requests.post(
                    webhook_url, json.dumps(main_content), headers=headers)
                a = 2
            elif last_rsi >= 40 and last_rsi <= 50:
                a = 0
            # 先頭を削除しメモリ節約
            p_list.pop(0)
            print(d.strftime("%Y-%m-%d %H:%M:%S"))
    pastd = d
    time.sleep(interval)
