from datetime import datetime
from ..models import StockData
from .AccountManager import AccountManager


def get_unix_time(date):
    # strftime('%s') 부분이 윈도우에서 동작하지 않는다.
    return int(datetime.strptime(date, '%Y-%m-%d').strftime('%s')) * 1000


class StockSimulator:
    """시뮬레이션 합니다."""
    def __init__(self, strategy, code):
        self.strategy = strategy
        self.code = code

        # 데이터 조회
        self.stock_datas = StockData.objects.filter(code=code).order_by('date')
        self.strategy.set_datas(self.stock_datas)
        self.balance_history = []
        self.buy_history = []
        self.sell_history = []
        self.simulate()

    def simulate(self):
        # 데이터를 하나씩 읽는다.
        starting_amount = 1000000
        holding_max_amount = 1000000
        account_manager = AccountManager(starting_amount, holding_max_amount)

        for data in self.stock_datas:
            # 보유주가 있는가?
            if account_manager.have_stocks():
                max_adj_close = account_manager.get_max_adj_close()
                rst = self.strategy.should_i_sell(data.date, max_adj_close)
                if rst:
                    sell_count = account_manager.sell(data.adj_close)
                    print('판매', data.date, data.adj_close)
                    self.sell_history.append({'date': data.date, 'count': sell_count})
            # 살만한가?
            rst = self.strategy.should_i_buy(data.date)
            if rst:
                buy_count = account_manager.buy(data.adj_close)
                print('구매', data.date, data.adj_close)
                if buy_count > 0:
                    self.buy_history.append({'date': data.date, 'count': buy_count})

            account_manager.compare_adj_close(data.adj_close)
            balance_with_stock = account_manager.get_balance_with_stock(data.close)
            self.balance_history.append({'date': data.date, 'balance': balance_with_stock
                                        , 'adj_close': data.adj_close
                                        , 'ma_5': data.ma_5, 'ma_20': data.ma_20
                                        , 'open': data.open, 'high': data.high, 'low': data.low, 'close': data.close})

    def get_balance_history(self):
        return self.balance_history

    def get_buy_history(self):
        return self.buy_history

    def get_sell_history(self):
        return self.sell_history


