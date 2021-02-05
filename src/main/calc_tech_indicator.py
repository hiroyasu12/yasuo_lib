# 価格のリストを受け取ってpd.DataFrameを返す関数を定義する
# 必要なライブラリの読み込み
import pandas as pd

# ボリンジャーバンドの関数
from pyti.bollinger_bands import upper_bollinger_band as bb_up
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from pyti.bollinger_bands import lower_bollinger_band as bb_low

def calc_bolinger(period: int, sigma: float, p_list: list): #期間、マルチ、価格のn足リスト（データはperiod個以上であること）
    eth_df = pd.DataFrame(p_list, columns = ['price'])
    _bb_up = bb_up(p_list,period,sigma)
    _bb_mid = bb_mid(p_list,period,sigma)
    _bb_low = bb_low(p_list,period,sigma)
    eth_df['bb_up'] = _bb_up #上側
    eth_df['bb_mid'] = _bb_mid #移動平均
    eth_df['bb_low'] = _bb_low #下限
    return eth_df

def calc_rsi(period:int, p_list:list): #移動平均の期間と価格のn足リスト(データはperiod個以上であること)
    ##差分を計算する
    df = pd.DataFrame(p_list, columns=['price'])
    diff = df.diff()
    # 最初のレコードが欠損してしまうので落としてあげる
    diff = diff[1:]
    # 値上がり幅、値下がり幅をシリーズへ切り分け
    up, down = diff.copy(), diff.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    down
    # 値上がり幅/値下がり幅の単純移動平均（14)を処理
    up_sma_14 = up.rolling(window=14, center=False).mean()
    down_sma_14 = down.abs().rolling(window=14, center=False).mean()
    down_sma_14
    # RSIの計算
    RS = up_sma_14 / down_sma_14
    RSI = 100.0 - (100.0 / (1.0 + RS))
    ret = pd.concat([df, RSI.rename(columns={'price': 'rsi'})], axis=1)
    return ret

def calc_macd(sma_big: int, sma_small: int, signal: int, p_list: list):
    #それぞれの移動平均を計算する
    df = pd.DataFrame(p_list, columns=['price'])
    short_window = df.rolling(window=sma_big, center=False).mean()
    long_window = df.rolling(window=sma_small, center=False).mean()
    # macdの計算
    macd = short_window - long_window
    df_signal = macd.rolling(window=signal, center=False).mean()
    ret = pd.concat([df, long_window.rename(columns={'price':'sma_big'}), short_window.rename(columns={'price':'sma_small'}), macd.rename(columns={'price':'macd'}), df_signal.rename(columns={'price':'signal'})], axis=1)
    return ret

def calc_dmi(length: int, adx: int, p_list: list):
    return False