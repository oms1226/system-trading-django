import re
import sys
from pandas_datareader import data
import pandas as pd
from datetime import datetime, timedelta
from ..models import StockData
import numpy as np


def get_from_yahoo(code, start_day, end_day, stock_type):
    # yahoo_code = get_yahoo_code(code, stock_type)
    yahoo_code = code

    try:
        df = data.DataReader(yahoo_code, 'yahoo', start_day, end_day)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    df = df[df['Volume'] != 0]
    df_adj_close = df['Adj Close']
    df_volume = df['Volume']

    df['MA_5'] = pd.Series(df_adj_close).rolling(window=5).mean()
    df['MA_20'] = pd.Series(df_adj_close).rolling(window=20).mean()
    df['MA_60'] = pd.Series(df_adj_close).rolling(window=60).mean()

    df['MV_5'] = pd.Series(df_volume).rolling(window=5).mean()
    df['MV_20'] = pd.Series(df_volume).rolling(window=20).mean()
    df['MV_60'] = pd.Series(df_volume).rolling(window=60).mean()

    df['RA_5'] = df['MA_5'] / df['MA_20']
    df['RA_20'] = df['MA_20'] / df['MA_60']

    return df


def get_yahoo_code(code, type):
    # A001525
    m = re.match(r'A(\d+)', code)
    if m:
        code = m.group(1)
    if type == 'kospi':
        return code + '.KS'
    else:
        return None


def get_date_format(time):
    return time.strftime('%Y-%m-%d')


def get_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')


def save_recent_data(code, stock_type="kospi"):
    today = datetime.today()
    today_str = get_date_format(today)
    last_date = today - timedelta(days=1000)

    # 저장된 가장 최근 날짜를 구한다.
    try:
        stock_data = StockData.objects.filter(code=code).order_by('-date').first()
        last_date = stock_data.date
        if last_date == today_str:
            return True
        last_date = get_date(last_date) - timedelta(days=150)
    except StockData.DoesNotExist:
        last_date = today - timedelta(days=1000)

    df = get_from_yahoo(code, last_date, today, stock_type)
    if df is None:
        print("[조회 실패]", code)
        return None
    df = df.replace(np.nan, 0, regex=True)

    for index, row in df.iterrows():
        if last_date > index:
            continue
        # 데이터를 저장한다
        date = get_date_format(index)
        # 키는 날짜와 코드
        obj, created = StockData.objects.get_or_create(
            code=code, date=date,
            defaults={
                'open': row['Open'], 'high': row['High'], 'low': row['Low'],
                'close': row['Close'], 'volume': row['Volume'], 'adj_close': row['Adj Close'],
                'ma_5': row['MA_5'], 'ma_20': row['MA_20'], 'ma_60': row['MA_60'],
                'mv_5': row['MV_5'], 'mv_20': row['MV_20'], 'mv_60': row['MV_60'],
                'ra_5': row['RA_5'], 'ra_20': row['RA_20']
            },
        )
        if created:
            print("[저장완료]", code, date)

    return True

