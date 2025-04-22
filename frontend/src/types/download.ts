export enum Platform {
  TIKTOK = 'TIKTOK',
  INSTAGRAM = 'INSTAGRAM',
  YOUTUBE = 'YOUTUBE'
}

export enum Quality {
  HIGH = 'HIGH',
  MEDIUM = 'MEDIUM',
  LOW = 'LOW'
}

export enum DownloadStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED'
}

export interface DownloadRequest {
  url: string;
  platform: Platform;
  quality: Quality;
}

export interface DownloadResponse {
  session_id: string;
  status: DownloadStatus;
  progress: number;
  url: string;
  file_path?: string;
  error_message?: string;
}

export interface BatchDownloadRequest {
  urls: string[];
  platform: Platform;
  quality: Quality;
}

export interface BatchDownloadResponse {
  session_id: string;
  total_urls: number;
  status: DownloadStatus;
  progress: number;
  completed_urls?: string[];
  failed_urls?: string[];
  error_message?: string;
} 