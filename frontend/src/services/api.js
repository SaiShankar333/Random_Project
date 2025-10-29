/**
 * API Service Layer
 * Handles all HTTP requests to the Flask backend
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add response interceptor for debugging
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.config.url, response.data);
    return response;
  },
  error => {
    console.error('API Error:', error.config?.url, error.message);
    return Promise.reject(error);
  }
);

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Prediction APIs
export const predictReview = async (reviewData) => {
  const response = await api.post('/predict', reviewData);
  return response.data;
};

export const predictBatchReviews = async (reviews) => {
  const response = await api.post('/predict/batch', { reviews });
  return response.data;
};

// Analytics APIs
export const getSummary = async () => {
  const response = await api.get('/analytics/summary');
  return response.data;
};

export const getCategoryStats = async () => {
  const response = await api.get('/analytics/category');
  return response.data;
};

export const getTimingStats = async () => {
  const response = await api.get('/analytics/timing');
  return response.data;
};

export const getReviews = async (page = 1, perPage = 50, filter = 'all') => {
  const response = await api.get('/analytics/reviews', {
    params: { page, per_page: perPage, filter }
  });
  return response.data;
};

export const getModelPerformance = async () => {
  const response = await api.get('/analytics/model-performance');
  return response.data;
};

export const getVerificationStatus = async () => {
  const response = await api.get('/analytics/verification-status');
  return response.data;
};

// Bulk Processing APIs
export const uploadBulkFile = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/bulk/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  });
  return response.data;
};

export const downloadResults = (downloadId) => {
  return `${API_BASE_URL}/bulk/download/${downloadId}`;
};

export const downloadTemplate = () => {
  return `${API_BASE_URL}/bulk/template`;
};

export default api;

