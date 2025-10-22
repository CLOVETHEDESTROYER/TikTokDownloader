import { MetadataRoute } from "next"

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://tiktokwatermarkremover.com"
  const currentDate = new Date()
  
  return [
    { 
      url: baseUrl, 
      lastModified: currentDate, 
      changeFrequency: "daily", 
      priority: 1 
    },
    { 
      url: `${baseUrl}/about`, 
      lastModified: currentDate, 
      changeFrequency: "weekly", 
      priority: 0.9 
    },
    { 
      url: `${baseUrl}/privacy-policy`, 
      lastModified: currentDate, 
      changeFrequency: "monthly", 
      priority: 0.5 
    },
    { 
      url: `${baseUrl}/terms-of-service`, 
      lastModified: currentDate, 
      changeFrequency: "monthly", 
      priority: 0.5 
    },
    { 
      url: `${baseUrl}/dmca`, 
      lastModified: currentDate, 
      changeFrequency: "monthly", 
      priority: 0.3 
    },
  ]
}
