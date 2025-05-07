'use client';

import React from 'react';
import Link from 'next/link';
import { Download, Heart } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <Download className="w-6 h-6 text-teal-600 dark:text-teal-400" />
              <span className="text-lg font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
                TikSave
              </span>
            </Link>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              The simplest way to download TikTok videos without watermarks. Our free service lets you save and share your favorite content easily.
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
              Made with <Heart className="w-4 h-4 text-red-500 mx-1" /> for TikTok content creators and fans
            </p>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link href="/privacy-policy" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">Legal</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/privacy-policy" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/privacy-policy" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  DMCA
                </Link>
              </li>
              <li>
                <Link href="/privacy-policy" className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  Contact Us
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-200 dark:border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-4 md:mb-0">
            © {currentYear} TikSave. All rights reserved.
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            TikSave is not affiliated with TikTok or ByteDance Ltd.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 