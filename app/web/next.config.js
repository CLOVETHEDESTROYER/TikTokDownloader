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
  // Add API route rewrites
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8001/api/:path*',
      },
      {
        source: '/health',
        destination: 'http://backend:8001/health',
      },
    ];
  },
  // Add other configurations as needed
  output: 'standalone',
  experimental: {
    // Enable CSS layer support
    layers: true,
  },
};

module.exports = nextConfig; 