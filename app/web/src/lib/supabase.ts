import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://vbbwydfwcegxxhiwdadu.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZiYnd5ZGZ3Y2VneHhoaXdkYWR1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5OTg3OTksImV4cCI6MjA3MzU3NDc5OX0.9VFSrZneI0dpg4uS3lmIUPNKb2Dq8Qg_w1HhxwXtC5s'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types for TypeScript
export interface SocialAccount {
  id: string
  user_id?: string
  platform: 'instagram' | 'tiktok' | 'facebook'
  account_id: string
  username: string
  access_token: string
  refresh_token?: string
  expires_at?: string
  is_active: boolean
  created_at: string
  metadata?: any
}

export interface ContentItem {
  id: string
  source_account_id: string
  original_url: string
  platform: 'instagram' | 'tiktok' | 'facebook'
  content_type: 'video' | 'post' | 'reel' | 'story' | 'igtv'
  title?: string
  description?: string
  author?: string
  thumbnail_url?: string
  duration?: number
  view_count?: number
  like_count?: number
  metadata?: any
  status: 'collected' | 'downloading' | 'downloaded' | 'processing' | 'scheduled' | 'posted' | 'failed' | 'deleted'
  download_path?: string
  created_at: string
  updated_at?: string
}

export interface DownloadQueue {
  id: string
  content_item_id: string
  priority: number
  status: 'pending' | 'downloading' | 'completed' | 'failed'
  retry_count: number
  error_message?: string
  created_at: string
  started_at?: string
  completed_at?: string
}

export interface ScheduledPost {
  id: string
  content_item_id: string
  target_platforms: string[]
  scheduled_time: string
  caption?: string
  hashtags?: string[]
  status: 'scheduled' | 'posting' | 'posted' | 'failed'
  post_data?: any
  created_at: string
  posted_at?: string
}
