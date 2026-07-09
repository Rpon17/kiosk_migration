from PySide6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QListWidget, 
    QPushButton, 
    QInputDialog
)
from PySide6.QtCore import Signal 
from api.product_api import get_products_by_category, create_product


class ProductView(QWidget):
    
    product_selected = Signal(int, str)

    def __init__(self):
        super().__init__()

        self.current_category_id = 1 
        self.products_data = [] 


        self.title_label = QLabel(f"[카테고리 ID: {self.current_category_id}] 상품 관리 화면")
        self.list_widget = QListWidget()
        
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.refresh_button = QPushButton("상품 조회")
        self.add_button = QPushButton("상품 추가")

        self.refresh_button.clicked.connect(self.load_products)
        self.add_button.clicked.connect(self.add_product)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_products(self):
        try:
            self.title_label.setText(f"[카테고리 ID: {self.current_category_id}] 상품 관리 화면")
            
            self.products_data = get_products_by_category(self.current_category_id)
            
            self.list_widget.clear()
            for product in self.products_data:
                self.list_widget.addItem(f"{product['name']} ({product['price']}원)")
                
        except Exception as e:
            print(f"상품 조회 실패: {e}")

    def on_item_double_clicked(self, item):
        row = self.list_widget.row(item)            
        selected_product = self.products_data[row]   
        
        self.product_selected.emit(selected_product['id'], selected_product['name'])

    def add_product(self):
        name, ok1 = QInputDialog.getText(self, "상품 등록", "새로운 상품 이름을 입력하세요:")
        if not ok1 or not name.strip():
            return
        price, ok2 = QInputDialog.getInt(self, "상품 등록", "상품 가격을 입력하세요 (원):", 0, 0)
        if not ok2:
            return

        try:
            create_product(category_id=self.current_category_id, name=name.strip(), price=price)
            self.load_products() 
        except Exception as e:
            print(f"상품 등록 실패: {e}")