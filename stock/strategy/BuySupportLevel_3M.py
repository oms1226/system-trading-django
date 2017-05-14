from collections import Counter
from datetime import datetime, timedelta


class BuySupportLevel_3M():
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

        # 3개월 값들의 정수형을 얻는다.
        compare_days = 60
        if index < compare_days:
            return False

        start_index = index - compare_days

        data_range = self.data_list[start_index:index - 5]
        # To return a new list, use the sorted() built-in function...
        sort_list = sorted(data_range, key=lambda x: x.close)

        min_data = None
        last_date = None
        for data in sort_list:
            this_date = datetime.strptime(data.date, '%Y-%m-%d')

            if last_date is None:
                last_date = this_date
                continue

            if this_date > last_date + timedelta(days=5):
                min_data = data
                break
            else:
                last_date = this_date

        if min_data is not None:
            this_close = self.data_list[index].close
            if min_data.close < this_close < min_data.close * 1.05:
                return True

        return False
