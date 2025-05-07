import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    domains: [
      'placehold.co',
      'via.placeholder.com',
      'placekitten.com',
      'picsum.photos',
      'i.ytimg.com',          // YouTube thumbnails
      'i.vimeocdn.com',       // Vimeo thumbnails
      'graph.facebook.com',   // Facebook/Instagram thumbnails
      'scontent.cdninstagram.com', // Instagram
      'cdninstagram.com',     // Instagram
      'pbs.twimg.com',        // Twitter
      'p16-sign-va.tiktokcdn.com', // TikTok
      'p16-sign-sg.tiktokcdn.com', // TikTok
      'p16-sign-useast2a.tiktokcdn.com', // TikTok
      'p77-sign-va.tiktokcdn.com', // TikTok
      'p77-sign-sg.tiktokcdn.com', // TikTok
    ],
  },
};

export default nextConfig;
