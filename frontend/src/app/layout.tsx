import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Footer from "@/components/Footer";
import { ThemeProvider } from "@/context/ThemeContext";
import { DownloadsProvider } from "@/context/DownloadsContext";
import Header from "@/components/Header";
import Script from 'next/script';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TikSave - Download TikTok Videos Without Watermark",
  description: "Download TikTok, Instagram, and YouTube videos with high quality and no watermark.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {process.env.NEXT_PUBLIC_ADSENSE_ID && (
          <Script
            async
            src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${process.env.NEXT_PUBLIC_ADSENSE_ID}`}
            crossOrigin="anonymous"
            strategy="afterInteractive"
          />
        )}
      </head>
      <body className={`${inter.className} flex flex-col min-h-screen bg-gradient-to-br from-tiktok-light via-white to-tiktok-secondary/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900`}>
        <ThemeProvider>
          <DownloadsProvider>
            <Header />
            <div className="flex-grow">
              {children}
            </div>
            <Footer />
          </DownloadsProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
