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
  title: "TikTok Video Downloader - Remove Watermark Free | TikSave",
  description: "Download TikTok videos without watermark instantly. Free, fast, and secure. No registration required. Works on all devices. Download in HD quality.",
  keywords: "tiktok downloader, remove watermark, tiktok video download, free download, no watermark, tiktok saver",
  openGraph: {
    title: "TikTok Video Downloader - Remove Watermark Free",
    description: "Download TikTok videos without watermark instantly. Free, fast, and secure.",
    url: "https://tiktokwatermarkremover.com",
    siteName: "TikSave",
    images: [
      {
        url: "https://tiktokwatermarkremover.com/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "TikTok Video Downloader",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "TikTok Video Downloader - Remove Watermark Free",
    description: "Download TikTok videos without watermark instantly. Free, fast, and secure.",
    images: ["https://tiktokwatermarkremover.com/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "YOUR_GOOGLE_VERIFICATION_CODE",
  },
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
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
          `}
        </Script>
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
