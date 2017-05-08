
class SellMAX_10:
    """10% 이상 손실이 발생하면 매도 한다."""
    def __init__(self, ):
        self.max_rate = 0.9
        self.max_close = 0
        self.datas = []
        self.data_list = []
        self.data_index_map = {}
        self.compare_close = False

    def set_datas(self, datas):
        self.datas = datas
        self.data_list = list(self.datas)
        for index, data in enumerate(self.data_list):
            self.data_index_map[data.date] = index

    def should_i_sell(self, date):
        close = self.datas.get(date=date).close
        if self.max_close * self.max_rate > close:
            self.compare_close = False
            self.max_close = 0
            return True
        else:
            return False

    def set_close(self, close):
        if self.compare_close and close > self.max_close:
            self.max_close = close

    def set_close_start(self):
        self.compare_close = True



