from collections import Counter
from datetime import datetime, timedelta


class BuyMomentum:
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

        compare_days = 20

        if index < compare_days:
            return False

        prev_index = index - compare_days
        prev_data = self.data_list[prev_index]
        next_data = self.data_list[index]

        if next_data.close > prev_data.close:
            return True

        return False
