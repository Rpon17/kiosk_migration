export interface ProductCreate {
  category_id: number;
  name: string;
  price: number;
  image_url?: string;
}

export interface ProductResponse {
  id: number;
  category_id: number;
  name: string;
  price: number;
  image_url?: string;
}