/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable TypeScript checking during build
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  },
  // Disable ESLint during build
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  // Add API route rewrites for local development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'production' 
          ? 'http://backend:8001/api/:path*'
          : 'http://localhost:8000/api/:path*',
      },
      {
        source: '/health',
        destination: process.env.NODE_ENV === 'production' 
          ? 'http://backend:8001/health'
          : 'http://localhost:8000/health',
      },
    ];
  },
  // Add other configurations as needed
  output: 'standalone',
  // Remove the problematic experimental config
  experimental: {
    // Remove outputFileTracingRoot to fix the warning
  },
};

module.exports = nextConfig;