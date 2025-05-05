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
    const isDev = process.env.NODE_ENV !== 'production';
    return [
      {
        source: '/api/:path*',
        destination: isDev
          ? 'http://localhost:8000/api/:path*' // Proxy to backend in dev
          : '/api/:path*', // In production, let DO App Platform route
      },
      {
        source: '/health',
        destination: isDev
          ? 'http://localhost:8000/health'
          : '/health',
      },
    ];
  },
  // Add other configurations as needed
  output: 'standalone',
};

module.exports = nextConfig; 