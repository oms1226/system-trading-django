import re
import sys
from pandas_datareader import data
import pandas as pd
from datetime import datetime, timedelta


def get_df_one(code):
    pattern = r'A(\d+)'
    if re.match(pattern, code):
        symbol = re.sub(pattern, r'\1.KS', code)
    else:
        return None

    today = datetime.today()
    start_day = today - timedelta(days=200)
    end_day = today

    try:
        df = data.DataReader(symbol, 'yahoo', start_day, end_day)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    df = df[df['Volume'] != 0]
    df_adj_close = df['Adj Close']
    df_volume = df['Volume']

    df['MA_5'] = pd.Series(df_adj_close).rolling(window=5).mean()
    df['MA_20'] = pd.Series(df_adj_close).rolling(window=20).mean()
    df['MA_60'] = pd.Series(df_adj_close).rolling(window=60).mean()
    df['MA_120'] = pd.Series(df_adj_close).rolling(window=120).mean()

    df['MV_5'] = pd.Series(df_volume).rolling(window=5).mean()
    df['MV_20'] = pd.Series(df_volume).rolling(window=20).mean()
    df['MV_60'] = pd.Series(df_volume).rolling(window=60).mean()
    df['MV_120'] = pd.Series(df_volume).rolling(window=120).mean()

    df['RA_5'] = df['MA_5'] / df['MA_20']
    df['RA_20'] = df['MA_20'] / df['MA_60']
    df['RA_60'] = df['MA_60'] / df['MA_120']

    return df
