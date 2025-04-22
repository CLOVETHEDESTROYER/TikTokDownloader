import axios from 'axios';
import { 
  DownloadRequest, 
  DownloadResponse, 
  BatchDownloadRequest, 
  BatchDownloadResponse 
} from '@/types/download';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const downloadVideo = async (request: DownloadRequest): Promise<DownloadResponse> => {
  const response = await api.post<DownloadResponse>('/download', request);
  return response.data;
};

export const batchDownload = async (request: BatchDownloadRequest): Promise<BatchDownloadResponse> => {
  const response = await api.post<BatchDownloadResponse>('/batch-download', request);
  return response.data;
};

export const getDownloadStatus = async (sessionId: string): Promise<DownloadResponse> => {
  const response = await api.get<DownloadResponse>(`/status/${sessionId}`);
  return response.data;
};

export const getQuota = async (): Promise<{ remaining: number }> => {
  const response = await api.get<{ remaining: number }>('/quota');
  return response.data;
}; 