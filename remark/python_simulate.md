name: inverse
layout: true
class: underscore

---
class: center, middle, hero

.title[
  # 시스템 트레이딩
  ## with python

  https://github.com/jacegem/system-trading-python
]

???

스피커 노트

Speaker notes go after ???

Toggle speaker view by pressing P

Pressing C clones the slideshow view,
which is the view to put on the projector
if you're using speaker view.

Press ? to toggle keyboard commands help.

---

# 차례

1. 전략을 세웁니다.

2. PyQt 를 이용해서 GUI로 구성합니다.

3. 데이터를 조회합니다. (야후 파이넨스)

4. 시뮬레이션을 합니다.

5. 앞으로 할 일

---

# 전략

단순하게 해 보았습니다.

Adj Close 값을 기준으로 전략을 세웠습니다

- 전날보다 오르면 `구매`
- 전날보다 내리면 `판매`

물론, `실패`하는 전략입니다


---

# PyQt

```
import sys
from PyQt5.QtWidgets import *

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.statusBar().showMessage('Ready')

    def changeStatusBar(self, msg):
        self.statusBar().showMessage(msg)

class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

if __name__ == "__main__":
    app = QApplication([])
    dialog = MyMainWindow()
    dialog.show()
    sys.exit(app.exec_())
```

---

# PyQt

실행 결과

![](https://content.screencast.com/users/beneapp/folders/Snagit/media/2bf4c83a-067a-44f3-9b31-36b2fe1291ba/2017-04-02_22-26-48.png)

---

# PyQt

이 곳에 필요한 내용 요소들을 입력합니다.

- 조회하려는 코드
- 보유 최대 금액
- 시작날짜
- 종료날짜

--

```
class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
```

위 코드 안에 필요한 요소들을 넣어서 생성합니다.


---

# PyQt

```
def __init__(self, parent):
    super(FormWidget, self).__init__(parent)

    self.gridLayout = QGridLayout(self)

    # 대상 (코드)
    # 시작날짜
    # 종료날짜
    # 종목 최대 보유금액

    self.gridRow = 0
    self.gridCol = 0

    # 대상 (코드)
    self.editCode = QLineEdit()
    self.gridLayout.addWidget(self.editCode, self.add_row(), 0)
    self.editCode.setText('A023350')

    # 투자 최대 금액
    self.editMoneyMax = QLineEdit()
    self.gridLayout.addWidget(self.editMoneyMax, self.add_row(), 0)
    self.editMoneyMax.setText('1000000')
```

---


```
    # 시작날짜
    self.dateStart = QDateEdit()
    self.gridLayout.addWidget(self.dateStart, self.add_row(), 0)
    self.startDate = QDate(2017,1,1)
    self.dateStart.setDate(self.startDate)

    # 종료날짜
    self.dateEnd = QDateEdit()
    self.gridLayout.addWidget(self.dateEnd, self.add_row(), 0)
    self.endDate = QDate(QDate.currentDate())
    self.dateEnd.setDate(self.endDate)

    # 시작 버튼
    self.btnStart = QPushButton("데이터 가져오기")
    self.btnStart.clicked.connect(self.get_stock_data)
    self.gridLayout.addWidget(self.btnStart, self.add_row(), 0)

    # 분석 버튼
    self.btnStart = QPushButton("분석")
    self.btnStart.clicked.connect(self.start_simulator)
    self.gridLayout.addWidget(self.btnStart, self.add_row(), 0)

    # 결과 창
    self.logOutput = QTextEdit(parent)
    self.logOutput.setReadOnly(True)
    self.logOutput.setFixedWidth(800)
    self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
    self.gridLayout.addWidget(self.logOutput, self.init_row(), self.add_col(), 6, 1)
```

---

# PyQt

![](https://content.screencast.com/users/beneapp/folders/Snagit/media/18b3bdf8-b44c-49ed-aee4-2cc7ad6b11c6/2017-04-02_22-33-22.png)

추가적으로 버튼과 출력창을 넣었습니다.


---

# PyQt

최초에 GUI가 보이게 되면 데이터를 조회하도록 하였습니다.


앞 장에서 보았던 FormWidget 클래스 안에 정의하였습니다.


```
class FormWidget(QWidget):
...
    def showEvent(self, QShowEvent):
        """시작하면 데이터를 가져온다."""
        self.get_stock_data()
...
```

---

# PyQt

입력된 데이터를 읽어와서 조회를 합니다.


```
def get_stock_data(self):
    self.code = self.editCode.text()
    money_max = self.editMoneyMax.text()
    self.start_datetime = self.get_datetime(self.dateStart.date())
    self.end_datetime = self.get_datetime(self.dateEnd.date())

    # 데이터 가져오기
    item_list = []
    item_list.append({'code': self.code, 'name': '테스트대상'})
    self.data_manager = DataManager(self.start_datetime, self.end_datetime)
    self.data_manager.set_item_list(item_list)

    # 계정 관리자
    self.account_manager = AccountManager(money_max, self.data_manager)
```

---

# PyQt

데이터 관리를 위한 클래스입니다

```
class DataManager:
    # 시작일, 종료일,
    def __init__(self, start_date, end_date):
        self.item_list = {}     # 아이템 목록
        self.data_source = 'yahoo'
        self.start_date = start_date - timedelta(days=200)
        self.end_date = end_date
        self.item_datas = {}    # 아이템 결과 데이터
        self.stock_datas = {}

    def set_item_list(self, item_list):
        """가져올 대상 아이템(주식코드)들을 지정한다."""
        # itemList
        # item['code'], item['name']
        task = Tasks(item_list, self.start_date, self.end_date)
        self.stock_datas = task.start()
```

---

# QRunnable

병렬로 데이터 조회를 합니다.

콘솔 기반에서는 `multiprocessing` 로 가능했는데

PyQt에서는 사용이 안되어서 `QRunnable` 를 사용하였습니다

--

처리하기 위해서 여러 클래스들을 만들었습니다.

```
class Tasks(QObject):
    ...
class WorkerSignals(QObject):
    ...
class Worker(QRunnable):
    ...
```

지금은 필요없지만.... 만들어 보았습니다.

---

# Pandas

Pandas로 야후 파이낸스를 조회합니다. wikidocs 에서 본 내용대로 하였습니다.

--

```
try:
    df = data.DataReader(symbol, self.data_source, self.start_date, self.end_date)
except:
    print("Unexpected error:", sys.exc_info()[0])
    return None
```

--

- symbol 에는 코드 `023350.KR`
- data_source 에는 `yahoo`
- start_date 에는 `2017-01-01`
- end_date 에는 `2017-04-03`

---

# 시뮬레이션

조회된 데이터를 이용해서 시뮬레이션 합니다.

타입이 처음보는 `dataframe` 이라서 사용하기 어려웠습니다.

어쩔 수 없이 방법은 무한 구글링...

--

## 적용해야 할 것

--

- 주문 전략
- 판매 전략

---

# 전략

```
class AnalyzeBasic():
    ADJ_CLOSE = 'Adj Close'

    def __init__(self, stock_data):
        """예제 전략"""
        self.stock_data = stock_data
        self.df = self.stock_data.get_df()
        self.idx = 0
```

AnalyzeBasic 클래스를 만들어서 전략을 담당하게 하였습니다.

---

# 메소드들


- 데이터 (주가정보) 가 있는지
- 살 대상인지
- 판매 대상인지

```
def has_data(self, target_date):
def is_worth_buying(self, target_date):
def should_i_sell(self, target_date):
```

--

이제 앞서 정의했던 전략을 적용합니다.

- 전날보다 오르면 `구매`
- 전날보다 내리면 `판매`

---

# 데이터 확인

먼저 데이터가 있는지 확인합니다.

공휴일에는 거래가 없어서, 비교할 대상이 없습니다.

```
def has_data(self, target_date):
    date_str = target_date.strftime('%Y-%m-%d')
    if date_str in self.df.index:
        return True
    else:
        return False
```

---

# 살 가치가 있을까?

```
def is_worth_buying(self, target_date):
    """사도 되는 것인지 판단"""
    # 대상 날짜의 인덱스를 얻는다.
    date_str = target_date.strftime('%Y-%m-%d')
    self.idx = self.df.index.get_loc(date_str)

    # 전날 보다 올랐으면 산다
    adj_close_today = self.df.ix[self.idx][AnalyzeBasic.ADJ_CLOSE]
    adj_close_last = self.df.ix[self.idx - 1][AnalyzeBasic.ADJ_CLOSE]

    if adj_close_today > adj_close_last:
        return True
    else:
        return False
```

---

# 팔아야 할까?

```
def should_i_sell(self, target_date):
    """팔아야 하는가"""
    # 대상 날짜의 인덱스를 얻는다.
    date_str = target_date.strftime('%Y-%m-%d')
    self.idx = self.df.index.get_loc(date_str)

    # 전날 보다 떨어졌으면 판다.
    adj_close_today = self.df.ix[self.idx][AnalyzeBasic.ADJ_CLOSE]
    adj_close_last = self.df.ix[self.idx - 1][AnalyzeBasic.ADJ_CLOSE]

    if adj_close_today < adj_close_last:
        return True
    else:
        return False
```

---

# 시뮬레이션

2017-01-01 부터 2017-04-02 까지 시뮬레이션 하였습니다.



> 판매시에 `0.99` 를 곱하도록 하였습니다.


---

# 결론은 손해

![](https://content.screencast.com/users/beneapp/folders/Snagit/media/42526651-cc9d-4303-9b76-d305ec2f3eae/2017-04-02_23-24-56.png)

시작은 `1000000` 으로 시작했지만, 마지막엔 `869152` 가 되었습니다.


---

# 앞으로 할 일

- 전략 만들기 (수익성 높은, 그리고 여러개)
- 데이터베이스 구축 (firebase)
- 정보 제공 (slack, app)
- 웹으로 구현하기 (django)

---
class: center, middle, hero

.title[
  # Thank You

  모든 소스는 `https://github.com/jacegem/system-trading-python` 에서 확인가능합니다.

    이 발표 자료도 포함되어 있습니다.
]