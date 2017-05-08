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

        compare_days = 3

        # 3일동안 0 이하이며 마지막날 0.99 이상이면 True
        result = True
        for i in range(compare_days):
            sidx = index - compare_days + i
            if sidx < 0:
                return False
            if self.data_list[sidx].ra_5 > 1:
                return False

        if self.datas.get(date=date).ra_5 < 0.99:
            return False

        # 20일 평균선이 3일동안 상승추세에 있어야 함

        last_ma_20 = 0
        for i in range(compare_days):
            sidx = index - compare_days + i
            if sidx < 0:
                return False
            ma_20 = self.data_list[sidx].ma_20
            if ma_20 > last_ma_20:
                last_ma_20 = ma_20
            else:
                return False

        return True

    def should_i_sell(self, date, max_adj_close):
        adj_close = self.datas.get(date=date).adj_close
        if max_adj_close * 0.9 > adj_close:
            return True
        else:
            return False
