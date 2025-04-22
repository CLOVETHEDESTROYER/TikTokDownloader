'use client';

import React from 'react';
import Head from 'next/head';

interface SEOProps {
  title?: string;
  description?: string;
  canonical?: string;
  ogType?: 'website' | 'article';
  ogImage?: string;
  twitterCard?: 'summary' | 'summary_large_image';
}

const SEO: React.FC<SEOProps> = ({
  title = 'TikSave - Download TikTok Videos Without Watermark',
  description = 'Download TikTok videos without watermark in HD quality. Free, fast, and easy to use online tool.',
  canonical,
  ogType = 'website',
  ogImage = '/og-image.jpg',
  twitterCard = 'summary_large_image'
}) => {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://tiksave.com';
  const fullCanonicalUrl = canonical ? `${siteUrl}${canonical}` : siteUrl;
  const fullOgImageUrl = ogImage.startsWith('http') ? ogImage : `${siteUrl}${ogImage}`;

  return (
    <Head>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={fullCanonicalUrl} />
      
      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={fullCanonicalUrl} />
      <meta property="og:image" content={fullOgImageUrl} />
      <meta property="og:site_name" content="TikSave" />
      
      {/* Twitter */}
      <meta name="twitter:card" content={twitterCard} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullOgImageUrl} />
    </Head>
  );
};

export default SEO; 