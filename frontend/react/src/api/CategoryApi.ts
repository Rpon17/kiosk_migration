import axiosInstance from './axiosInstance';
import type { CategoryCreate, CategoryResponse } from '../types/category';

export const getCategories = async (storeId: number): Promise<CategoryResponse[]> => {
  const response = await axiosInstance.get<CategoryResponse[]>(`/categories/store/${storeId}`);
  return response.data;
};

export const createCategory = async (data: CategoryCreate): Promise<CategoryResponse> => {
  const response = await axiosInstance.post<CategoryResponse>('/categories', data);
  return response.data;
};