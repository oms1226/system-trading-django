
class SellMomentum:
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
        # 인덱스 얻기
        index = self.data_index_map[date]

        compare_days = 20

        if index < compare_days:
            return False

        prev_index = index - compare_days
        prev_data = self.data_list[prev_index]
        next_data = self.data_list[index]

        if next_data.close < prev_data.close:
            return True

        return False

    def set_close(self, close):
        if self.compare_close and close > self.max_close:
            self.max_close = close

    def set_close_start(self):
        self.compare_close = True



