class StrategyRa5:
    def __init__(self):
        self.datas = None
        self.data_list = []
        self.data_index_map = {}

    def set_datas(self, datas):
        self.datas = datas
        self.data_list = list(self.datas)
        for index, data in enumerate(self.data_list):
            self.data_index_map[data.date] = index

    def should_i_buy(self, date):
        # 인덱스 얻기
        index = self.data_index_map[date]

        # 3일동안 0 이하이며 마지막날 0.99 이상이면 True
        result = True
        for i in range(4):
            sidx = index - (i + 1)
            if sidx < 0:
                result = False
                break
            if self.data_list[sidx].ra_5 > 1:
                result = False
                break

        if result and self.datas.get(date=date).ra_5 > 0.99:
            return True
        else:
            return False

    def should_i_sell(self, date, max_adj_close):
        adj_close = self.datas.get(date=date).adj_close
        if max_adj_close * 0.9 > adj_close:
            return True
        else:
            return False
