from PySide6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QListWidget, 
    QPushButton, 
    QInputDialog
)
from PySide6.QtCore import Signal 
from api.stock_api import create_stock, get_stock, update_stock


class StockView(QWidget):
    stock_selected = Signal(int, int)  # stock_id, quantity

    def __init__(self):
        super().__init__()

        self.current_product_id = 1 
        self.stock_data = [] 

        self.title_label = QLabel(f"[상품 ID: {self.current_product_id}] 재고 관리 화면")
        self.list_widget = QListWidget()
        
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.refresh_button = QPushButton("재고 조회")
        self.add_button = QPushButton("재고 생성")
        self.update_button = QPushButton("재고 변경")

        self.refresh_button.clicked.connect(self.load_stock)
        self.add_button.clicked.connect(self.add_stock)
        self.update_button.clicked.connect(self.update_stock)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    # 🔄 1. 안전장치를 강화한 재고 조회 함수
    def load_stock(self):
        try:
            self.title_label.setText(f"[상품 ID: {self.current_product_id}] 재고 관리 화면")
            self.list_widget.clear()
            
            # API 호출
            response_data = get_stock(self.current_product_id)
            
            # 🚀 [안전장치 1] 데이터가 정상적인 리스트나 딕셔너리가 아닌 경우 예외 처리
            if not response_data:
                self.list_widget.addItem("등록된 재고가 없습니다. [재고 생성]을 눌러주세요.")
                self.stock_data = []
                return

            # API가 단일 딕셔너리(`{}`)로 줄 경우를 대비해 리스트(`[]`)로 통일
            if isinstance(response_data, dict):
                # 만약 에러 메시지가 담겨온 거라면 거르기
                if "detail" in response_data:
                    self.list_widget.addItem(f"서버 메시지: {response_data['detail']}")
                    return
                self.stock_data = [response_data]
            elif isinstance(response_data, list):
                self.stock_data = response_data
            else:
                self.list_widget.addItem("올바르지 않은 데이터 형식입니다.")
                return
            
            for stock in self.stock_data:
                # 🚀 [안전장치 2] string indices must be integers 에러 방지 안전 검사
                if not isinstance(stock, dict) or 'quantity' not in stock:
                    continue
                    
                # 시간 데이터 가공
                updated_at = stock.get('updated_at', '')
                time_str = updated_at.split("T")[0] if "T" in str(updated_at) else str(updated_at)
                if not time_str or time_str == "None":
                    time_str = "기록 없음"

                self.list_widget.addItem(f"현재 재고: {stock['quantity']}개 (최근 수정: {time_str})")
                
        except Exception as e:
            print(f"재고 화면 조회 처리 실패: {e}")

    # 🖱️ 2. 더블클릭 이벤트 함수
    def on_item_double_clicked(self, item):
        try:
            row = self.list_widget.row(item)
            if row < 0 or row >= len(self.stock_data):
                return
            selected_stock = self.stock_data[row]   
            self.stock_selected.emit(selected_stock['id'], selected_stock['quantity'])
        except Exception as e:
            print(f"아이템 더블클릭 실패: {e}")

    # ➕ 3. 재고 최초 생성 함수
    def add_stock(self):
        quantity, ok = QInputDialog.getInt(self, "재고 생성", "최초 입고할 수량을 입력하세요:", 0, 0)
        if ok:
            try:
                # API로 요청을 보낼 때 인자 값이 제대로 매칭되는지 확인
                create_stock(product_id=self.current_product_id, quantity=quantity)
                self.load_stock() 
            except Exception as e:
                print(f"재고 생성 실패: {e}\n💡 백엔드의 주소(URL)나 스키마 규격을 확인해 보세요.")

    # ✏️ 4. 재고 수량 변경 함수
    def update_stock(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            print("수정할 재고 항목을 목록에서 먼저 선택해 주세요.")
            return

        row = self.list_widget.row(current_item)
        if row < 0 or row >= len(self.stock_data):
            return
            
        selected_stock = self.stock_data[row]
        stock_id = selected_stock['id']
        current_qty = selected_stock['quantity']

        new_qty, ok = QInputDialog.getInt(
            self, 
            "재고 변경", 
            f"변경할 수량을 입력하세요 (현재: {current_qty}개):", 
            current_qty, 
            0
        )

        if ok:
            try:
                update_stock(stock_id=stock_id, quantity=new_qty)
                self.load_stock()
            except Exception as e:
                print(f"재고 변경 실패: {e}")