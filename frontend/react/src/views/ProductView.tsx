import { useState, useEffect } from "react";

import { getProducts, createProduct } from "../api/ProductApi";
import { getStock, updateStock } from "../api/StockApi";

import type { ProductResponse } from "../types/product";

export default function ProductView({
  categoryId,
}: {
  categoryId: number;
}) {
  const [products, setProducts] = useState<ProductResponse[]>([]);
  const [stocks, setStocks] = useState<Record<number, number>>({});

  useEffect(() => {
    loadProducts();
  }, [categoryId]);

  const loadProducts = async () => {
    try {
      const productList = await getProducts(categoryId);

      setProducts(productList);

      const stockMap: Record<number, number> = {};

      for (const product of productList) {
        try {
          const stock = await getStock(product.id);
          stockMap[product.id] = stock.quantity;
        } catch {
          stockMap[product.id] = 0;
        }
      }

      setStocks(stockMap);
    } catch (error) {
      console.error("상품 조회 실패", error);
    }
  };

  const handleAddProduct = async () => {
    const name = prompt("상품명을 입력하세요.");
    if (!name?.trim()) return;

    const price = prompt("가격을 입력하세요.");
    if (!price) return;

    try {
      await createProduct({
        category_id: categoryId,
        name: name.trim(),
        price: Number(price),
      });

      alert("상품 등록 완료");
      loadProducts();
    } catch (error) {
      alert("상품 등록 실패");
    }
  };

  const handleUpdateStock = async (
    productId: number,
    currentQty: number
  ) => {
    const qty = prompt(
      "변경할 재고를 입력하세요.",
      String(currentQty)
    );

    if (qty === null) return;

    try {
      await updateStock(productId, {
        quantity: Number(qty),
      });

      setStocks((prev) => ({
        ...prev,
        [productId]: Number(qty),
      }));

      alert("재고 수정 완료");
    } catch (error) {
      alert("재고 수정 실패");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "25px",
        }}
      >
        <h2>📦 상품 관리</h2>

        <button
          onClick={handleAddProduct}
          style={{
            padding: "10px 20px",
            backgroundColor: "#ddd",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          ➕ 상품 등록
        </button>
      </div>

      {products.length === 0 ? (
        <div
          style={{
            padding: "30px",
            textAlign: "center",
            color: "#888",
          }}
        >
          등록된 상품이 없습니다.
        </div>
      ) : (
        products.map((p) => (
          <div
            key={p.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "15px",
              marginBottom: "10px",
            }}
          >
            <div>
              <div
                style={{
                  fontWeight: "bold",
                  fontSize: "18px",
                }}
              >
                {p.name}
              </div>

              <div
                style={{
                  marginTop: "5px",
                  color: "#666",
                }}
              >
                가격 : {p.price.toLocaleString()}원
              </div>

              <div
                style={{
                  marginTop: "5px",
                  color: "#ddd",
                  fontWeight: "bold",
                }}
              >
                재고 : {stocks[p.id] ?? 0}개
              </div>
            </div>

            <button
              onClick={() =>
                handleUpdateStock(
                  p.id,
                  stocks[p.id] ?? 0
                )
              }
              style={{
                padding: "10px 18px",
                backgroundColor: "#ddd",
                color: "white",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              재고 수정
            </button>
          </div>
        ))
      )}
    </div>
  );
}