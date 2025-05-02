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
    // In production with the combined app, we use a relative path
    // that will be handled by our Nginx configuration
    // In development, we use the absolute URL from env var
    const isProduction = process.env.NODE_ENV === 'production';
    
    // Default to localhost for development
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // In production, we want to use a relative URL that will be proxied
    const destination = isProduction 
      ? 'http://localhost:8000/api/v1/:path*'  // Internal to Docker network
      : `${apiUrl}/api/v1/:path*`;             // Development external URL
    
    return [
      {
        source: '/api/v1/:path*',
        destination: destination,
      },
      {
        source: '/health',
        destination: isProduction 
          ? 'http://localhost:8000/health'
          : `${apiUrl}/health`,
      }
    ];
  },
  // Add other configurations as needed
  output: 'standalone',
};

module.exports = nextConfig; 