import axiosInstance from './axiosInstance';
import type { StoreCreate, StoreResponse } from '../types/store';

// 매장 전체 조회
export const getStores = async (): Promise<StoreResponse[]> => {
  const response = await axiosInstance.get<StoreResponse[]>('/stores');
  return response.data;
};

// 매장 생성
export const createStore = async (data: StoreCreate): Promise<StoreResponse> => {
  const response = await axiosInstance.post<StoreResponse>('/stores', data);
  return response.data;
};