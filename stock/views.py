from django.shortcuts import render
from .stock import StockManager


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
