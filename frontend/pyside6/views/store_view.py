from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QInputDialog  
)
from PySide6.QtCore import Signal 
from api.store_api import get_stores, create_store 


class StoreView(QWidget):
    
    # 매장이 더블 클릭되면 매장ID, 매장명을 실어서 보냄
    store_selected = Signal(int, str)

    def __init__(self):
        super().__init__()
        
        # 받아온 매장 정보를 저장할 바구니
        self.stores_data = [] 

        self.list_widget = QListWidget()
        
        # 위젯만들기
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        # 버튼을 2개 만듬
        self.refresh_button = QPushButton("매장 조회")
        self.add_button = QPushButton("매장 추가")

        # 각 버튼을 눌렀을때 실행할 함수를 매칭함
        self.refresh_button.clicked.connect(self.load_store)
        self.add_button.clicked.connect(self.add_store) 

        # 위에서 만든 리스트 상자와 버튼들을 위에서 아래로 정렬함
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    # 매장 목록을 가져와서 띄우기
    def load_store(self):
        # API파일을 통해서 백엔드 db에 있는 매장 원본 데이터를 싹다 가져옴
        self.stores_data = get_stores()
        
        # 새로운 내용을 보여주기 전에 화면에 위젯을 지움
        self.list_widget.clear()
        
        # 바구니에서 매장을 하나씩 꺼내서 글자로 가공함
        for store in self.stores_data:
            self.list_widget.addItem(f"{store['name']} / {store['location']}")

    # 더블클릭 시 작동할 함수
    def on_item_double_clicked(self, item):
        row = self.list_widget.row(item)       # 몇 번째 줄인지 index 확인
        selected_store = self.stores_data[row] # 원본 데이터에서 해당 매장 딕셔너리 추출
        
        # MainWindow 들으라고 신호를 빵 쏩니다 (id와 name 전달)
        self.store_selected.emit(selected_store['id'], selected_store['name'])

    # 매장 추가하는 알림바
    def add_store(self):
        name, ok1 = QInputDialog.getText(self, "매장 등록", "매장 이름을 입력하세요:")
        if not ok1 or not name.strip():
            return

        location, ok2 = QInputDialog.getText(self, "매장 등록", "매장 위치를 입력하세요:")
        if not ok2 or not location.strip():
            return

        try:
            create_store(name, location)
            self.load_store()
        except Exception as e:
            print(f"매장 등록 실패: {e}")