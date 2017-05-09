from .HoldingStock import HoldingStock


class AccountManager:
    def __init__(self, starting_amount, holding_max_amount):
        self.balance = starting_amount
        self.holding_max_amount = holding_max_amount
        self.holding_stocks = []
        self.max_adj_close = 0
        self.sell_rate = 0.99
        pass

    def have_stocks(self):
        if len(self.holding_stocks) > 0:
            return True
        else:
            return False

    def get_max_adj_close(self):
        return self.max_adj_close

    def sell(self, adj_close):
        # 보유금액 += 오늘자 가격 * 수량
        sellable_count = self.get_sellable_count()
        self.balance += adj_close * sellable_count * self.sell_rate
        self.holding_stocks = []
        self.max_adj_close = 0
        return sellable_count

    def buy(self, adj_close):
        buyable_count = self.get_buyable_count(adj_close)
        if buyable_count > 0:
            self.balance -= adj_close * buyable_count
            self.holding_stocks.append(HoldingStock(adj_close, buyable_count))
        if adj_close > self.max_adj_close:
            self.max_adj_close = adj_close
        return buyable_count

    def get_sellable_count(self):
        sum_of_count = 0
        for holding_stock in self.holding_stocks:
            count = holding_stock.get_count()
            sum_of_count += count
        return sum_of_count

    def get_buyable_count(self, adj_close):
        sum_of_holding = 0
        for holding_stock in self.holding_stocks:
            count = holding_stock.get_count()
            price = holding_stock.get_price()
            sum_of_holding += count * price

        buyable_amount = self.holding_max_amount - sum_of_holding
        return int(buyable_amount / adj_close)

    def compare_adj_close(self, adj_close):
        # 보유주가 있다면, 최고값을 비교한다.
        if self.have_stocks():
            if adj_close > self.max_adj_close:
                self.max_adj_close = adj_close

    def get_balance_with_stock(self, close):
        sum_of_stock_price = 0
        for stock in self.holding_stocks:
            # sum_of_stock_price += manager.get_price() * manager.get_count() * self.sell_rate
            sum_of_stock_price += close * stock.get_count() * self.sell_rate
        return self.balance + sum_of_stock_price


