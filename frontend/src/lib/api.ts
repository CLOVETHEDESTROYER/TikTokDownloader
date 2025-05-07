import axios from 'axios';
import { 
  DownloadRequest, 
  DownloadResponse, 
  BatchDownloadRequest, 
  BatchDownloadResponse 
} from '@/types/download';
import { TikTokVideoData } from '@/services/downloadService';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const API_KEY = process.env.NEXT_PUBLIC_WEBSITE_API_KEY;

// Create an axios instance that we can use across the app
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

/**
 * Download a single video
 */
export const downloadVideo = async (request: DownloadRequest): Promise<TikTokVideoData> => {
  const response = await api.post<TikTokVideoData>('/download', request);
  return response.data;
};

/**
 * Batch download multiple videos at once
 */
export const batchDownload = async (request: BatchDownloadRequest): Promise<BatchDownloadResponse> => {
  const response = await api.post<BatchDownloadResponse>('/batch-download', request);
  return response.data;
};

/**
 * Check the status of a download in progress
 */
export const getDownloadStatus = async (sessionId: string): Promise<DownloadResponse> => {
  const response = await api.get<DownloadResponse>(`/status/${sessionId}`);
  return response.data;
};

/**
 * Get the remaining download quota for the user or IP
 */
export const getQuota = async (): Promise<{ remaining: number }> => {
  const response = await api.get<{ remaining: number }>('/quota');
  return response.data;
}; 