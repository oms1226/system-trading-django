from datetime import datetime
from ..models import StockData
from .AccountManager import AccountManager


def get_unix_time(date):
    # strftime('%s') 부분이 윈도우에서 동작하지 않는다.
    return int(datetime.strptime(date, '%Y-%m-%d').strftime('%s')) * 1000


class StockSimulator:
    """시뮬레이션 합니다."""
    def __init__(self, code, strategy_buy, strategy_sell, start_money):
        self.code = code
        self.strategy_buy = strategy_buy
        self.strategy_sell = strategy_sell
        self.start_money = int(start_money)

        # 데이터 조회
        self.stock_datas = StockData.objects.filter(code=code).order_by('date')
        self.strategy_buy.set_datas(self.stock_datas)
        self.strategy_sell.set_datas(self.stock_datas)

        self.balance_history = []
        self.buy_history = []
        self.sell_history = []

        self.simulate()

    def simulate(self):
        # holding_max_amount = 1000000
        account_manager = AccountManager(self.start_money, self.start_money)

        for data in self.stock_datas:
            # 보유주가 있는가?
            if account_manager.have_stocks():
                rst = self.strategy_sell.should_i_sell(data.date)
                if rst:
                    sell_count = account_manager.sell(data.close)
                    print('판매', self.code, data.date, data.close)
                    self.sell_history.append({'date': data.date, 'count': sell_count, 'code': self.code})
            # 살만한가?
            rst = self.strategy_buy.should_i_buy(data.date)
            if rst:
                buy_count = account_manager.buy(data.close)
                if buy_count > 0:
                    print('구매', self.code, data.date, data.close)
                    self.buy_history.append({'date': data.date, 'count': buy_count, 'code': self.code})
                    self.strategy_sell.set_close_start()

            self.strategy_sell.set_close(data.close)

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


