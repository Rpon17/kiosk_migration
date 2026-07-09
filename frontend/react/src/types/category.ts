export interface CategoryCreate {
  name: string;
  store_id: number;
}

export interface CategoryResponse {
  id: number;
  name: string;
  store_id: number;
  created_at: string;
}