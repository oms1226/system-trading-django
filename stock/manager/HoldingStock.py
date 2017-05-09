class HoldingStock:
    """보유주에 대한 정보를 관리합니다."""
    def __init__(self, adj_close, count):
        self.adj_close = adj_close
        self.count = count

    def get_price(self):
        return self.adj_close

    def get_count(self):
        return self.count
