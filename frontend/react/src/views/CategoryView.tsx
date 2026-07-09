import { useState, useEffect } from "react";
import { getCategories, createCategory } from "../api/CategoryApi";
import type { CategoryResponse } from "../types/category";

interface Props {
  storeId: number;
  storeName: string;
  onCategorySelect: (categoryId: number, categoryName: string) => void;
}

export default function CategoryView({
  storeId,
  storeName,
  onCategorySelect,
}: Props) {
  const [categories, setCategories] = useState<CategoryResponse[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(
    null
  );

  useEffect(() => {
    loadCategories();
    setSelectedCategoryId(null);
  }, [storeId]);

  const loadCategories = async () => {
    try {
      const data = await getCategories(storeId);
      setCategories(data || []);
    } catch (error) {
      console.error("카테고리 로드 실패", error);
    }
  };

  const handleAddCategory = async () => {
    const name = prompt(`${storeName}에 추가할 카테고리 이름을 입력하세요.`);
    if (!name?.trim()) return;

    try {
      await createCategory({
        name,
        store_id: storeId,
      });

      loadCategories();
    } catch (error) {
      alert("카테고리 등록 실패");
    }
  };

  const handleSelectCategory = () => {
    if (selectedCategoryId === null) {
      alert("카테고리를 선택해주세요.");
      return;
    }

    const selectedCategory = categories.find(
      (c) => c.id === selectedCategoryId
    );

    if (!selectedCategory) return;

    onCategorySelect(selectedCategory.id, selectedCategory.name);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>📂 {storeName} 카테고리 관리</h2>

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "6px",
          minHeight: "200px",
          marginTop: "20px",
        }}
      >
        {categories.length === 0 ? (
          <div style={{ padding: "20px", color: "#888" }}>
            등록된 카테고리가 없습니다.
          </div>
        ) : (
          categories.map((cat) => (
            <div
              key={cat.id}
              onClick={() => setSelectedCategoryId(cat.id)}
              style={{
                padding: "12px",
                cursor: "pointer",
                borderBottom: "1px solid #eee",
                backgroundColor:
                  selectedCategoryId === cat.id
                    ? "#d6f5ff"
                    : "transparent",
                fontWeight:
                  selectedCategoryId === cat.id ? "bold" : "normal",
              }}
            >
              {cat.name}
            </div>
          ))
        )}
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: "20px",
        }}
      >
        <div style={{ display: "flex", gap: "10px" }}>
                  <button
          onClick={handleSelectCategory}
          disabled={selectedCategoryId === null}
        >
          조회
        </button>

          <button onClick={handleAddCategory}>추가</button>
        </div>
      </div>
    </div>
  );
}