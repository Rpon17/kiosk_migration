import axiosInstance from './axiosInstance';
import type { ProductCreate, ProductResponse } from '../types/product';

export const getProducts = async (categoryId: number): Promise<ProductResponse[]> => {
  const response = await axiosInstance.get(`/products/category/${categoryId}`);
  return response.data;
};

export const createProduct = async (data: ProductCreate): Promise<ProductResponse> => {
  const response = await axiosInstance.post('/products', data);
  return response.data;
};