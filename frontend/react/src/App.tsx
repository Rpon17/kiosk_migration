import { useState } from "react";
import StoreView from "./views/StoreView";
import CategoryView from "./views/CategoryView";
import ProductView from "./views/ProductView";

type ViewType = "store" | "category" | "product";

export default function App() {
  const [currentView, setCurrentView] = useState<ViewType>("store");
  const [currentStore, setCurrentStore] = useState({ id: 0, name: "" });
  const [currentCategory, setCurrentCategory] = useState({ id: 0, name: "" });

  // 매장 선택 시 하위 모든 상태 초기화
  const handleStoreSelection = (storeId: number, storeName: string) => {
    setCurrentStore({ id: storeId, name: storeName });
    setCurrentCategory({ id: 0, name: "" });
    setCurrentView("category");
  };

  // 카테고리 선택 시 상품 화면으로
  const handleCategorySelection = (categoryId: number, categoryName: string) => {
    setCurrentCategory({ id: categoryId, name: categoryName });
    setCurrentView("product");
  };

  // 안전한 페이지 이동을 위한 래퍼 함수
  const navigateTo = (view: ViewType) => {
    if (view !== "store" && currentStore.id === 0) {
      alert("⚠️ 먼저 매장을 선택해 주세요.");
      setCurrentView("store");
    } else {
      setCurrentView(view);
    }
  };

  return (
    <div style={{ display: "flex", fontFamily: "sans-serif", minHeight: "100vh" }}>
      {/* 사이드바 */}
      <div style={{ width: "200px", backgroundColor: "#f4f5f7", padding: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>
        <h3 style={{ marginTop: 0 }}>POS 관리자</h3>
        <button onClick={() => navigateTo("store")} style={navButtonStyle(currentView === "store")}>🏢 매장 관리</button>
        <button onClick={() => navigateTo("category")} style={navButtonStyle(currentView === "category")}>📁 카테고리 관리</button>
        <button onClick={() => navigateTo("product")} style={navButtonStyle(currentView === "product")}>🎁 상품 관리</button>
      </div>

      {/* 메인 콘텐츠 */}
      <div style={{ flex: 1, padding: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: "2px solid #333", paddingBottom: "20px" }}>
          <h1>POS 관리 시스템</h1>
          {currentStore.id !== 0 && (
            <button onClick={() => setCurrentView("store")} style={{ padding: '8px 12px' }}>매장 변경</button>
          )}
        </div>
        
        {/* 상태 표시줄 */}
        <div style={{ padding: "10px", backgroundColor: "#e6f7ff", margin: "20px 0", borderRadius: "4px" }}>
          현재 위치: <strong>{currentStore.name || "매장 미선택"}</strong> 
          {currentCategory.id !== 0 && ` > ${currentCategory.name}`}
        </div>
        
        {/* 뷰 분기 */}
        <div style={{ marginTop: "20px" }}>
          {currentView === "store" && <StoreView onStoreSelect={handleStoreSelection} />}
          {currentView === "category" && currentStore.id !== 0 && (
            <CategoryView storeId={currentStore.id} storeName={currentStore.name} onCategorySelect={handleCategorySelection} />
          )}
          {currentView === "product" && currentCategory.id !== 0 && (
            <ProductView categoryId={currentCategory.id} />
          )}
        </div>
      </div>
    </div>
  );
}

function navButtonStyle(isActive: boolean) {
  return {
    padding: "10px", textAlign: "left" as const, cursor: "pointer",
    backgroundColor: isActive ? "#1890ff" : "transparent",
    color: isActive ? "#fff" : "#333",
    border: "none", borderRadius: "4px"
  };
}