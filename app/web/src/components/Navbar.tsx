'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';

const Navbar: React.FC = () => {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  const isActive = (path: string) => {
    return pathname === path;
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };
  
  return (
    <nav className="bg-white/80 backdrop-blur-lg border-b border-tiktok-secondary/20 shadow-sm py-4 relative z-10">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="flex items-center">
            <span className="text-2xl font-bold bg-gradient-purple text-transparent bg-clip-text">
              TikSave
            </span>
          </Link>
          
          <div className="hidden md:flex space-x-8">
            <NavLink href="/" active={isActive('/')}>
              Home
            </NavLink>
            <NavLink href="/about" active={isActive('/about')}>
              About
            </NavLink>
          </div>
          
          <div className="md:hidden">
            <button
              onClick={toggleMobileMenu}
              className="text-tiktok-dark focus:outline-none"
              aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
            >
              {mobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-white/95 backdrop-blur-lg border-b border-tiktok-secondary/20 shadow-md">
          <div className="px-4 py-4 space-y-4">
            <MobileNavLink href="/" active={isActive('/')} onClick={toggleMobileMenu}>
              Home
            </MobileNavLink>
            <MobileNavLink href="/about" active={isActive('/about')} onClick={toggleMobileMenu}>
              About
            </MobileNavLink>
          </div>
        </div>
      )}
    </nav>
  );
};

interface NavLinkProps {
  href: string;
  active: boolean;
  children: React.ReactNode;
}

const NavLink: React.FC<NavLinkProps> = ({ href, active, children }) => {
  return (
    <Link 
      href={href}
      className={`${
        active 
          ? 'text-tiktok-primary font-medium' 
          : 'text-gray-600 hover:text-tiktok-primary'
      } transition-colors duration-200`}
    >
      {children}
    </Link>
  );
};

interface MobileNavLinkProps extends NavLinkProps {
  onClick: () => void;
}

const MobileNavLink: React.FC<MobileNavLinkProps> = ({ href, active, onClick, children }) => {
  return (
    <Link 
      href={href}
      onClick={onClick}
      className={`${
        active 
          ? 'text-tiktok-primary font-medium' 
          : 'text-gray-600'
      } block py-2 transition-colors duration-200`}
    >
      {children}
    </Link>
  );
};

export default Navbar; 