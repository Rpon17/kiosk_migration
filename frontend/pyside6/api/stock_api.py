import requests

BASE_URL = "http://127.0.0.1:8000"

# 🔍 1. 재고 조회 API
def get_stock(product_id: int):
    """특정 상품의 재고 정보를 조회합니다."""
    url = f"{BASE_URL}/stocks/{product_id}"
    response = requests.get(url)
    
    # 500 에러 등이 나면 에러를 일으키지 않고 디버깅 로그를 찍은 후 빈 결과를 줍니다.
    if response.status_code != 200:
        print(f"[-] 백엔드 재고 조회 실패 ({response.status_code}): {response.text}")
        return None
        
    return response.json()


# ➕ 2. 재고 생성 API (수정됨)
def create_stock(product_id: int, quantity: int):
    """새로운 재고 데이터를 생성합니다."""
    url = f"{BASE_URL}/stocks"
    
    # 🚀 백엔드(FastAPI) Pydantic 스키마가 기대하는 정확한 JSON 바디 구조로 매핑
    payload = {
        "product_id": product_id,
        "quantity": quantity
    }
    
    # ⚠️ data=payload가 아니라 json=payload로 보내야 백엔드가 500 에러 없이 파싱합니다.
    response = requests.post(url, json=payload)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        # 백엔드에서 왜 터졌는지 터미널에 에러 원인 상세 출력
        print(f"[-] 백엔드 재고 생성 실패 ({response.status_code}): {response.text}")
        response.raise_for_status()


# ✏️ 3. 재고 변경 API (인자명 매칭 완료)
def update_stock(stock_id: int, quantity: int):
    """기존 재고 수량을 변경합니다."""
    # 🚀 화면단(StockView)과 매개변수 이름을 'stock_id'로 완벽하게 일치시켰습니다.
    url = f"{BASE_URL}/stocks/{stock_id}"
    
    payload = {
        "quantity": quantity
    }
    
    # 수정(Update)이므로 보통 PUT 또는 PATCH를 사용합니다. 
    # 만약 백엔드가 PUT이 아닌 다른 메서드를 쓴다면 requests.put을 requests.patch나 post로 바꿔주세요.
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[-] 백엔드 재고 변경 실패 ({response.status_code}): {response.text}")
        response.raise_for_status()