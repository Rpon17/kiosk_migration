export interface StockResponse {
  id: number;
  product_id: number;
  quantity: number;
  updated_at: string;
}

export interface StockUpdate {
  quantity: number;
}