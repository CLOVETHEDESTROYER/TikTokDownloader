'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Download, Moon, Sun, Menu, X } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header 
      className={`sticky top-0 z-50 transition-all duration-300 ${
        isScrolled 
          ? 'bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm shadow-sm' 
          : 'bg-transparent'
      }`}
    >
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <Download className="w-8 h-8 text-teal-600 dark:text-teal-400" />
          <span className="text-xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
            TikSave
          </span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link 
            href="/" 
            className={`text-sm font-medium transition-colors duration-200 ${
              pathname === '/' 
                ? 'text-teal-600 dark:text-teal-400' 
                : 'text-gray-700 dark:text-gray-300 hover:text-teal-600 dark:hover:text-teal-400'
            }`}
          >
            Home
          </Link>
          <Link 
            href="/about" 
            className={`text-sm font-medium transition-colors duration-200 ${
              pathname === '/about' 
                ? 'text-teal-600 dark:text-teal-400' 
                : 'text-gray-700 dark:text-gray-300 hover:text-teal-600 dark:hover:text-teal-400'
            }`}
          >
            How It Works
          </Link>
          <Link 
            href="/privacy-policy" 
            className={`text-sm font-medium transition-colors duration-200 ${
              pathname === '/privacy-policy' 
                ? 'text-teal-600 dark:text-teal-400' 
                : 'text-gray-700 dark:text-gray-300 hover:text-teal-600 dark:hover:text-teal-400'
            }`}
          >
            Privacy
          </Link>
          <button 
            onClick={toggleTheme}
            className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors duration-200"
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </nav>

        {/* Mobile Menu Button */}
        <div className="md:hidden flex items-center">
          <button 
            onClick={toggleTheme}
            className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors duration-200 mr-2"
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          <button 
            onClick={toggleMobileMenu}
            className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors duration-200"
            aria-label="Open menu"
          >
            {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white dark:bg-gray-900 shadow-lg">
          <nav className="container mx-auto px-4 py-4 flex flex-col space-y-4">
            <Link 
              href="/" 
              className={`text-base font-medium transition-colors duration-200 ${
                pathname === '/' 
                  ? 'text-teal-600 dark:text-teal-400' 
                  : 'text-gray-700 dark:text-gray-300'
              }`}
              onClick={toggleMobileMenu}
            >
              Home
            </Link>
            <Link 
              href="/about" 
              className={`text-base font-medium transition-colors duration-200 ${
                pathname === '/about' 
                  ? 'text-teal-600 dark:text-teal-400' 
                  : 'text-gray-700 dark:text-gray-300'
              }`}
              onClick={toggleMobileMenu}
            >
              How It Works
            </Link>
            <Link 
              href="/privacy-policy" 
              className={`text-base font-medium transition-colors duration-200 ${
                pathname === '/privacy-policy' 
                  ? 'text-teal-600 dark:text-teal-400' 
                  : 'text-gray-700 dark:text-gray-300'
              }`}
              onClick={toggleMobileMenu}
            >
              Privacy
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header; 