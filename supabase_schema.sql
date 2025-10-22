-- Content Pipeline Database Schema for Supabase
-- Run these commands in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Social Accounts Table
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT,
    platform TEXT NOT NULL CHECK (platform IN ('instagram', 'tiktok', 'facebook')),
    account_id TEXT NOT NULL,
    username TEXT NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB,
    UNIQUE(platform, account_id)
);

-- Content Items Table
CREATE TABLE content_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_account_id UUID REFERENCES social_accounts(id),
    original_url TEXT NOT NULL,
    platform TEXT NOT NULL CHECK (platform IN ('instagram', 'tiktok', 'facebook')),
    content_type TEXT NOT NULL CHECK (content_type IN ('video', 'post', 'reel', 'story', 'igtv')),
    title TEXT,
    description TEXT,
    author TEXT,
    thumbnail_url TEXT,
    duration FLOAT,
    view_count INTEGER,
    like_count INTEGER,
    metadata JSONB,
    status TEXT DEFAULT 'collected' CHECK (status IN ('collected', 'downloading', 'downloaded', 'processing', 'scheduled', 'posted', 'failed', 'deleted')),
    download_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(original_url)
);

-- Download Queue Table
CREATE TABLE download_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID REFERENCES content_items(id),
    priority INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'downloading', 'completed', 'failed')),
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- Scheduled Posts Table
CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_item_id UUID REFERENCES content_items(id),
    target_platforms TEXT[] NOT NULL,
    scheduled_time TIMESTAMPTZ NOT NULL,
    caption TEXT,
    hashtags TEXT[],
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'posting', 'posted', 'failed')),
    post_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    posted_at TIMESTAMPTZ
);

-- Create indexes for better performance
CREATE INDEX idx_content_items_status ON content_items(status);
CREATE INDEX idx_content_items_platform ON content_items(platform);
CREATE INDEX idx_content_items_created_at ON content_items(created_at);
CREATE INDEX idx_download_queue_status ON download_queue(status);
CREATE INDEX idx_download_queue_priority ON download_queue(priority);
CREATE INDEX idx_scheduled_posts_scheduled_time ON scheduled_posts(scheduled_time);
CREATE INDEX idx_scheduled_posts_status ON scheduled_posts(status);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_content_items_updated_at 
    BEFORE UPDATE ON content_items 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data for testing
INSERT INTO social_accounts (platform, account_id, username, access_token) VALUES
('instagram', 'sample_instagram_id', 'your_instagram', 'sample_token_instagram'),
('tiktok', 'sample_tiktok_id', 'your_tiktok', 'sample_token_tiktok');

-- Insert sample content items
INSERT INTO content_items (source_account_id, original_url, platform, content_type, title, author, status) VALUES
((SELECT id FROM social_accounts WHERE platform = 'instagram' LIMIT 1), 'https://www.instagram.com/p/C1234567890/', 'instagram', 'reel', 'Amazing Dance Reel', '@user123', 'collected'),
((SELECT id FROM social_accounts WHERE platform = 'tiktok' LIMIT 1), 'https://www.tiktok.com/@chef_mike/video/1234567890', 'tiktok', 'video', 'Cooking Tutorial', '@chef_mike', 'downloading'),
((SELECT id FROM social_accounts WHERE platform = 'instagram' LIMIT 1), 'https://www.instagram.com/p/B0CDEF12345/', 'instagram', 'post', 'Travel Vlog', '@wanderer_x', 'downloaded');

-- Insert sample download queue items
INSERT INTO download_queue (content_item_id, priority, status) VALUES
((SELECT id FROM content_items WHERE title = 'Amazing Dance Reel' LIMIT 1), 1, 'pending'),
((SELECT id FROM content_items WHERE title = 'Cooking Tutorial' LIMIT 1), 2, 'downloading');
