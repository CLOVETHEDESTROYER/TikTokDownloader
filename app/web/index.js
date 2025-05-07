// This file is just a simple entry point for Digital Ocean deployment
// It delegates to the Next.js start script

console.log('Starting Next.js app...');

// Import the Next.js CLI
try {
  require('next/dist/bin/next');
} catch (error) {
  console.error('Failed to start Next.js app', error);
  process.exit(1);
} 