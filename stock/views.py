import json
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .manager import StockManager
from .strategy.BuyRA_5 import BuyRA_5
from .strategy.BuyGC_5 import BuyGC_5
from .strategy.SellDC_5 import SellDC_5
from .strategy.SellMAX_10 import SellMAX_10
from .manager.StockSimulator import StockSimulator
from .models import StockCode, StrategyBuy, StrategySell


def index(request):
    # 대상들
    codes = StockCode.objects.all()
    # 매수전략
    buys = StrategyBuy.objects.filter(use_yn='Y')
    # 매도전략
    sells = StrategySell.objects.filter(use_yn='Y')
    # 초기금
    money = 1000000
    return render(request, 'stock/simulate.html'
                  , {'codes': codes, 'buys': buys, 'sells': sells
                      , 'money': money
                     })


def add_stock(request):
    # name, yahoo_code,
    # 파일읽기
    file = os.path.join(settings.SITE_ROOT, '../manager/data/kospi_yahoo.csv')
    f = open(file, 'rt')
    lines = f.readlines()
    for line in lines:
        datas = line.split(',')
        yahoo_code = datas[0]
        name = datas[1]
        obj, created = StockCode.objects.get_or_create(
            yahoo_code=yahoo_code, name=name
        )
    f.close()


def update_stock(request):
    # 종목을 업데이트 한다
    # 코스피 : http://finance.daum.net/quote/all.daum?type=U&stype=P
    # 코스닥 : http://finance.daum.net/quote/all.daum?type=U&stype=Q
    pass


def send_to_slack(msg):
    channel = 'bot_stock'
    settings.SLACK.chat.post_message(channel, msg)


def collect(request):
    """데이터를 조회한다."""
    # 어떤 데이터를 조회하는가? 대상?
    targets = ['A001525', 'A023350', 'A018670']
    for target in targets:
        # 데이터를 가져와서 저장한다.
        rst = StockManager.save_recent_data(target)
        if rst:
            send_to_slack('[데이터저장] : {}'.format(target))

    return render(request, 'stock/collect.html', {'msg': '데이터 저장 완료'})


# def view(request, strategy, code):
#     """시물레이션을 보여준다."""
#     # return render(request, 'manager/view.html', {'strategy': strategy, 'code': code})
#     # 대상들
#     codes = StockCode.objects.all()
#     # 매수전략
#     buys = StrategyBuy.objects.filter(use_yn='Y')
#     # 매도전략
#     sells = StrategySell.objects.filter(use_yn='Y')
#     # 초기금
#     return render(request, 'manager/simulate.html', {'codes': codes
#         , 'buys': buys
#         , 'sells': sells})


def simulate(request, code, buy_code, sell_code, start_money):
    #최근 데이터를 조회한다
    print('최근 데이터 저장 시작', code)
    rst = StockManager.save_recent_data(code)
    print('최근 데이터 저장 결과', rst)
    if rst is None:
        send_to_slack('[데이터저장 실패] : {}'.format(code))

    if buy_code == 'RA_5':
        buy_func = BuyRA_5()
    elif buy_code == 'GC_5':
        buy_func = BuyGC_5()

    if sell_code == 'MAX_10':
        sell_func = SellMAX_10()
    elif sell_code == 'DC_5':
        sell_func = SellDC_5()

    print('시뮬레이션 시작', code, buy_code, sell_code, start_money)
    simulator = StockSimulator(code, buy_func, sell_func, start_money)
    print('시뮬레이션 종료', code, buy_code, sell_code, start_money)

    balance_history = simulator.get_balance_history()
    buy_history = simulator.get_buy_history()
    sell_history = simulator.get_sell_history()

    return HttpResponse(json.dumps([balance_history, buy_history, sell_history]), content_type='text/json')




B20_T05 = 'B20_T05'
B05_T20 = 'B05_T20'
MA_5 = 'MA_5'
MA_20 = 'MA_20'


def analyze(request):
    """살 종목을 추천한다."""
    # 30일간의 데이터를 가져온다. 5일 평균, 20일 평균 포함
    df = StockManager.get_df_one('A001525')

    before = None
    result = []

    for index, row in df.iterrows():
        if row[MA_5] and row[MA_20]:
            ma5 = row[MA_5]
            ma20 = row[MA_20]
            if ma20 > ma5:
                current = B05_T20
            else:
                current = B20_T05
            if before:
                if before == B05_T20 and current == B20_T05:
                    # found
                    result.append({
                        'date': index.strftime('%Y-%m-%d'),
                        'adjclose': row['Adj Close']
                    })
            before = current
    return render(request, 'stock/analyze.html', {'result': result})
