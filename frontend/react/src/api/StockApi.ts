import axiosInstance from './axiosInstance';
import type { StockResponse, StockUpdate } from '../types/stock';

export const getStock = async (productId: number): Promise<StockResponse> => {
  const response = await axiosInstance.get(`/stocks/${productId}`);
  return response.data;
};

export const updateStock = async (productId: number, data: StockUpdate): Promise<StockResponse> => {
  const response = await axiosInstance.put(`/stocks/${productId}`, data);
  return response.data;
};