import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        tiktok: {
          primary: '#8B5CF6',
          secondary: '#C4B5FD',
          accent: '#4C1D95',
          dark: '#1E1B4B',
          light: '#F5F3FF',
          gray: '#F3F4F6',
          'gray-dark': '#2D2B3F',
        },
      },
      backgroundImage: {
        'gradient-tiktok': 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
        'gradient-purple': 'linear-gradient(135deg, #C4B5FD 0%, #8B5CF6 50%, #4C1D95 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient-shift': 'gradient 8s linear infinite',
      },
      backdropBlur: {
        'xxl': '30px',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center',
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center',
          },
        },
      },
    },
  },
  plugins: [],
};

export default config; 