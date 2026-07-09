from PySide6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QListWidget, 
    QPushButton, 
    QInputDialog
)
from PySide6.QtCore import Signal
from api.category_api import get_categories_by_store, create_category


class CategoryView(QWidget):
    category_selected = Signal(int, str)

    def __init__(self):
        super().__init__()

        self.current_store_id = 1 
        self.categories_data = [] 

        self.title_label = QLabel(f"[매장 ID: {self.current_store_id}] 카테고리 관리 화면")
        self.list_widget = QListWidget()
        
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.refresh_button = QPushButton("카테고리 조회")
        self.add_button = QPushButton("카테고리 추가")

        self.refresh_button.clicked.connect(self.load_categories)
        self.add_button.clicked.connect(self.add_category)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_categories(self):
        try:
            self.categories_data = get_categories_by_store(self.current_store_id)
            
            self.list_widget.clear()
            for category in self.categories_data:
                self.list_widget.addItem(f"{category['name']}")
                
        except Exception as e:
            print(f"카테고리 조회 실패: {e}")

    def on_item_double_clicked(self, item):
        row = self.list_widget.row(item)            
        selected_category = self.categories_data[row]   
        

        self.category_selected.emit(selected_category['id'], selected_category['name'])

    def add_category(self):
        name, ok = QInputDialog.getText(self, "카테고리 등록", "새로운 카테고리 이름을 입력하세요:")
        
        if ok and name.strip():
            try:
                create_category(self.current_store_id, name.strip())
                self.load_categories()
            except Exception as e:
                print(f"카테고리 등록 실패: {e}")