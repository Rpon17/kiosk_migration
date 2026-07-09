export interface StoreCreate {
  name: string;
  location: string; 
}

export interface StoreResponse {
  id: number;
  name: string;
  location: string; 
  created_at: string;
}