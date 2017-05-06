from django.shortcuts import render
from .stock import StockManager


def index(request):
    """개략적인 상황을 보여준다."""
    # TODO: 상황을 보여주기 위한 데이터를 생성한다
    result_list = []
    return render(request, 'stock/view.html', {'result': result_list})


def read_file(request):
    # 종목을 업데이트 한다
    pass


def collect(request):
    """데이터를 조회한다."""
    # 어떤 데이터를 조회하는가? 대상?
    result_list = []
    return render(request, 'stock/collect.html', {'result': result_list})


def view(request, code):
    # 오늘까지의 데이터가 있는가?
    # 데이터 조회는 언제 할 것인가
    # 전날 데이터는 오전 8시?
    # 데이터가 모두 있다고 가정한다면 데이터베이스에 데이터를 읽어서 보여준다
    data = []
    return render(request, 'stock/view.html', {'data': data})


# Create your views here.
def sell(request):
    pass


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
