from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from views.store_view import StoreView
from views.category_view import CategoryView
from views.product_view import ProductView
from views.stock_view import StockView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("POS 관리자")
        self.resize(1000, 600)

        # ==========================================
        # 1. 왼쪽 사이드 메뉴 바 생성
        # ==========================================
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()

        self.store_button = QPushButton("매장 관리")
        self.category_button = QPushButton("카테고리 관리")
        self.product_button = QPushButton("상품 관리")
        self.stock_button = QPushButton("재고 관리")

        menu_layout.addWidget(self.store_button)
        menu_layout.addWidget(self.category_button)
        menu_layout.addWidget(self.product_button)
        menu_layout.addWidget(self.stock_button)

        menu_widget.setLayout(menu_layout)

        # ==========================================
        # 2. 오른쪽 메인 화면 스택 생성 및 위젯 등록
        # ==========================================
        self.stack = QStackedWidget()

        self.store_view = StoreView()
        self.category_view = CategoryView()
        self.product_view = ProductView()
        self.stock_view = StockView()

        self.stack.addWidget(self.store_view)
        self.stack.addWidget(self.category_view)
        self.stack.addWidget(self.product_view)
        self.stack.addWidget(self.stock_view)

        # ==========================================
        # 3. 🔌 각 화면에서 올라오는 더블클릭 신호(Signal) 릴레이 연결
        # ==========================================
        # ① 매장 더블클릭 ➡️ 카테고리 화면으로 이동
        self.store_view.store_selected.connect(self.handle_store_selection)
        
        # ② 카테고리 더블클릭 ➡️ 상품 화면으로 이동
        self.category_view.category_selected.connect(self.handle_category_selection)

        # 🔥 ③ [새로 추가] 상품 더블클릭 ➡️ 재고 화면으로 이동하도록 전선 납땜!
        self.product_view.product_selected.connect(self.handle_product_selection)

        # ==========================================
        # 4. 좌측 메뉴 버튼 직접 클릭 시 화면 전환 이벤트
        # ==========================================
        self.store_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.store_view))
        self.category_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.category_view))
        self.product_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.product_view))
        self.stock_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_view))

        # ==========================================
        # 5. 전체 레이아웃 조립 및 중앙 배치
        # ==========================================
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        main_layout.addWidget(menu_widget, 1)  # 가로 비율 1
        main_layout.addWidget(self.stack, 4)   # 가로 비율 4 (넓게 배치)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ==========================================
    # 🎯 신호(Signal)를 받아서 처리하는 전용 조종 함수들
    # ==========================================

    # 🚀 1. 매장 선택 시: 카테고리로 데이터 토스
    def handle_store_selection(self, store_id, store_name):
        self.category_view.current_store_id = store_id
        if hasattr(self.category_view, 'title_label'):
            self.category_view.title_label.setText(f"[{store_name}] 카테고리 관리 화면")
            
        self.category_view.load_categories()
        self.stack.setCurrentWidget(self.category_view)

    # 🚀 2. 카테고리 선택 시: 상품으로 데이터 토스
    def handle_category_selection(self, category_id, category_name):
        self.product_view.current_category_id = category_id
        if hasattr(self.product_view, 'title_label'):
            self.product_view.title_label.setText(f"[{category_name}] 상품 관리 화면")
            
        self.product_view.load_products()
        self.stack.setCurrentWidget(self.product_view)

    # 🚀 3. [새로 추가] 상품 선택 시: 재고로 데이터 토스
    def handle_product_selection(self, product_id, product_name):
        # 재고 뷰가 물고 있을 상품 ID를 유저가 선택한 진짜 ID로 덮어씌웁니다.
        self.stock_view.current_product_id = product_id
        if hasattr(self.stock_view, 'title_label'):
            self.stock_view.title_label.setText(f"[{product_name}] 재고 관리 화면")
            
        # 변경된 상품 ID를 가지고 DB 금고에서 재고 정보를 새로 뽑아옵니다.
        self.stock_view.load_stock()
        
        # 화면을 즉시 재고 관리 화면으로 휙 돌려줍니다.
        self.stack.setCurrentWidget(self.stock_view)