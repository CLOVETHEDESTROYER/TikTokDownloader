# Video Downloader API - iOS Integration Guide

Complete Swift integration documentation for the TikTok/Instagram/Facebook/YouTube Downloader API.

## Table of Contents

1. [Overview](#overview)
2. [Base Configuration](#base-configuration)
3. [Authentication](#authentication)
4. [Platforms](#platforms)
   - [TikTok](#tiktok-api)
   - [Instagram](#instagram-api)
   - [Facebook](#facebook-api)
   - [YouTube](#youtube-api)
   - [Audio Extraction](#audio-extraction-api)
5. [Swift Implementation](#swift-implementation)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

---

## Overview

### Supported Platforms

| Platform | Content Types | URL Patterns |
|----------|---------------|--------------|
| **TikTok** | Videos | `tiktok.com`, `vm.tiktok.com`, `vt.tiktok.com` |
| **Instagram** | Posts, Reels, Stories | `instagram.com/p/`, `instagram.com/reel/` |
| **Facebook** | Videos, Reels, Live, Stories | `facebook.com`, `fb.watch` |
| **YouTube** | Videos, Shorts, Live | `youtube.com`, `youtu.be` |
| **Audio** | Extract audio from any platform | All above URLs |

### Quality Options

All platforms support these quality levels:
- `high` - Up to 1080p
- `medium` - Up to 720p  
- `low` - Up to 480p

---

## Base Configuration

### API Base URLs

```swift
// Development (local)
let API_BASE_URL = "http://localhost:8001"

// Production
let API_BASE_URL = "https://tiktokwatermarkremover.com"
// or
let API_BASE_URL = "http://YOUR_SERVER_IP:8001"
```

### Endpoint Structure

```
{BASE_URL}/api/v1/{platform}/{action}
```

Examples:
- `POST /api/v1/tiktok/download`
- `POST /api/v1/instagram/download`
- `POST /api/v1/facebook/download`
- `POST /api/v1/youtube/download`
- `POST /api/v1/audio/extract`

---

## Authentication

All endpoints require an API key passed in the `X-API-Key` header.

```swift
let headers: [String: String] = [
    "Content-Type": "application/json",
    "X-API-Key": "YOUR_API_KEY"
]
```

---

## Platforms

### TikTok API

#### Download Single Video
**Endpoint:** `POST /api/v1/tiktok/download?url={URL}`

**Request:**
```swift
// URL parameter (query string)
let url = "https://www.tiktok.com/@user/video/123456789"
```

**Response:**
```json
{
  "status": "success",
  "filename": "tiktok_abc123.mp4",
  "title": "Video Title",
  "url": "/downloads/tiktok_abc123.mp4"
}
```

#### Batch Download
**Endpoint:** `POST /api/v1/tiktok/batch`

**Request Body:**
```json
["https://tiktok.com/...", "https://tiktok.com/..."]
```

#### Get Status
**Endpoint:** `GET /api/v1/tiktok/status/{session_id}`

---

### Instagram API

#### Download Content
**Endpoint:** `POST /api/v1/instagram/download`

**Request Body:**
```json
{
  "url": "https://www.instagram.com/p/ABC123/",
  "quality": "high"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "message": "Download successful",
  "download_url": "/downloads/instagram_abc123.mp4"
}
```

#### Batch Download
**Endpoint:** `POST /api/v1/instagram/batch`

**Request Body:**
```json
{
  "urls": [
    "https://www.instagram.com/p/ABC123/",
    "https://www.instagram.com/reel/DEF456/"
  ],
  "quality": "high"
}
```

---

### Facebook API

#### Download Single Video
**Endpoint:** `POST /api/v1/facebook/download`

**Request Body:**
```json
{
  "url": "https://www.facebook.com/watch/?v=123456789",
  "quality": "high"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "message": "Facebook video downloaded successfully",
  "download_url": "/downloads/facebook_abc123.mp4"
}
```

#### Advanced Download (with metadata)
**Endpoint:** `POST /api/v1/facebook/download-advanced`

**Request Body:**
```json
{
  "url": "https://www.facebook.com/reel/123456789",
  "quality": "high",
  "include_metadata": true,
  "include_captions": false
}
```

**Response:**
```json
{
  "url": "https://www.facebook.com/reel/...",
  "download_url": "/downloads/facebook_abc123.mp4",
  "content_type": "reel",
  "session_id": "uuid-string",
  "is_live": false,
  "metadata": {
    "title": "Video Title",
    "author": "Page Name",
    "duration": 30.5,
    "view_count": 1000,
    "like_count": 500,
    "description": "Video description",
    "upload_date": "20250110",
    "content_type": "reel",
    "is_live": false,
    "thumbnail_url": "https://...",
    "page_name": "Page Name"
  }
}
```

#### Batch Download
**Endpoint:** `POST /api/v1/facebook/batch`

**Request Body:**
```json
{
  "urls": [
    "https://www.facebook.com/watch/?v=123",
    "https://fb.watch/abc123/"
  ],
  "quality": "high"
}
```

#### Supported Facebook URL Formats
```
https://www.facebook.com/watch/?v=VIDEO_ID
https://www.facebook.com/watch/VIDEO_ID
https://www.facebook.com/reel/REEL_ID
https://www.facebook.com/share/r/SHARE_ID
https://www.facebook.com/share/v/SHARE_ID
https://fb.watch/WATCH_ID
https://m.facebook.com/watch/?v=VIDEO_ID
```

---

### YouTube API

#### Download Single Video
**Endpoint:** `POST /api/v1/youtube/download`

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "quality": "high"
}
```

#### Advanced Download (with metadata)
**Endpoint:** `POST /api/v1/youtube/download-advanced`

**Request Body:**
```json
{
  "url": "https://www.youtube.com/shorts/ABC123",
  "quality": "high",
  "include_metadata": true,
  "include_subtitles": false
}
```

**Response:**
```json
{
  "url": "https://www.youtube.com/shorts/...",
  "download_url": "/downloads/youtube_abc123.mp4",
  "content_type": "shorts",
  "session_id": "uuid-string",
  "is_shorts": true,
  "metadata": {
    "title": "Video Title",
    "author": "Channel Name",
    "duration": 60.0,
    "view_count": 1000000,
    "like_count": 50000,
    "description": "Video description",
    "upload_date": "20250110",
    "content_type": "shorts",
    "is_shorts": true,
    "thumbnail_url": "https://i.ytimg.com/..."
  }
}
```

#### Batch Download
**Endpoint:** `POST /api/v1/youtube/batch`

#### Supported YouTube URL Formats
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
https://youtube.com/live/VIDEO_ID
```

---

### Audio Extraction API

Extract audio from **any** supported platform.

#### Extract Audio
**Endpoint:** `POST /api/v1/audio/extract`

**Request Body:**
```json
{
  "url": "https://www.tiktok.com/@user/video/123456789"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "message": "Audio extracted successfully",
  "audio_url": "/downloads/audio_abc123.mp3",
  "title": "Original Video Title",
  "duration": 30.5,
  "platform": "tiktok"
}
```

#### Batch Extract
**Endpoint:** `POST /api/v1/audio/batch-extract`

**Request Body:**
```json
{
  "urls": [
    "https://www.tiktok.com/@user/video/123",
    "https://www.instagram.com/reel/ABC123/",
    "https://www.youtube.com/watch?v=xyz"
  ]
}
```

---

## Swift Implementation

### Enums & Models

```swift
import Foundation

// MARK: - Platform Enum
enum Platform: String, Codable {
    case tiktok
    case instagram
    case facebook
    case youtube
}

// MARK: - Quality Enum
enum Quality: String, Codable {
    case high
    case medium
    case low
}

// MARK: - Content Types
enum FacebookContentType: String, Codable {
    case video
    case reel
    case live
    case story
    case post
}

enum YouTubeContentType: String, Codable {
    case video
    case shorts
    case playlist
    case live
}

// MARK: - Request Models
struct DownloadRequest: Codable {
    let url: String
    let platform: Platform?
    let quality: String?
    
    init(url: String, quality: Quality = .high, platform: Platform? = nil) {
        self.url = url
        self.quality = quality.rawValue
        self.platform = platform
    }
}

struct BatchDownloadRequest: Codable {
    let urls: [String]
    let platform: Platform?
    let quality: String?
    
    init(urls: [String], quality: Quality = .high, platform: Platform? = nil) {
        self.urls = urls
        self.quality = quality.rawValue
        self.platform = platform
    }
}

struct AudioExtractRequest: Codable {
    let url: String
}

struct AudioBatchExtractRequest: Codable {
    let urls: [String]
}

// MARK: - Response Models
struct DownloadResponse: Codable {
    let sessionId: String
    let status: String
    let message: String
    let downloadUrl: String?
    
    enum CodingKeys: String, CodingKey {
        case sessionId = "session_id"
        case status
        case message
        case downloadUrl = "download_url"
    }
}

struct DownloadStatus: Codable {
    let sessionId: String
    let status: String
    let progress: Double
    let message: String
    let downloadUrl: String?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case sessionId = "session_id"
        case status
        case progress
        case message
        case downloadUrl = "download_url"
        case error
    }
}

struct AudioExtractResponse: Codable {
    let sessionId: String
    let status: String
    let message: String
    let audioUrl: String?
    let title: String?
    let duration: Double?
    let platform: String?
    
    enum CodingKeys: String, CodingKey {
        case sessionId = "session_id"
        case status
        case message
        case audioUrl = "audio_url"
        case title
        case duration
        case platform
    }
}

// MARK: - Facebook-Specific Models
struct FacebookMediaMetadata: Codable {
    let title: String?
    let author: String?
    let duration: Double?
    let viewCount: Int?
    let likeCount: Int?
    let description: String?
    let uploadDate: String?
    let contentType: FacebookContentType
    let isLive: Bool
    let thumbnailUrl: String?
    let pageName: String?
    
    enum CodingKeys: String, CodingKey {
        case title, author, duration, description
        case viewCount = "view_count"
        case likeCount = "like_count"
        case uploadDate = "upload_date"
        case contentType = "content_type"
        case isLive = "is_live"
        case thumbnailUrl = "thumbnail_url"
        case pageName = "page_name"
    }
}

struct FacebookDownloadResponse: Codable {
    let url: String
    let downloadUrl: String
    let contentType: FacebookContentType
    let metadata: FacebookMediaMetadata
    let sessionId: String
    let isLive: Bool
    
    enum CodingKeys: String, CodingKey {
        case url
        case downloadUrl = "download_url"
        case contentType = "content_type"
        case metadata
        case sessionId = "session_id"
        case isLive = "is_live"
    }
}

// MARK: - YouTube-Specific Models
struct YouTubeMediaMetadata: Codable {
    let title: String?
    let author: String?
    let duration: Double?
    let viewCount: Int?
    let likeCount: Int?
    let description: String?
    let uploadDate: String?
    let contentType: YouTubeContentType
    let isShorts: Bool
    let thumbnailUrl: String?
    
    enum CodingKeys: String, CodingKey {
        case title, author, duration, description
        case viewCount = "view_count"
        case likeCount = "like_count"
        case uploadDate = "upload_date"
        case contentType = "content_type"
        case isShorts = "is_shorts"
        case thumbnailUrl = "thumbnail_url"
    }
}

struct YouTubeDownloadResponse: Codable {
    let url: String
    let downloadUrl: String
    let contentType: YouTubeContentType
    let metadata: YouTubeMediaMetadata
    let sessionId: String
    let isShorts: Bool
    
    enum CodingKeys: String, CodingKey {
        case url
        case downloadUrl = "download_url"
        case contentType = "content_type"
        case metadata
        case sessionId = "session_id"
        case isShorts = "is_shorts"
    }
}
```

### API Service Class

```swift
import Foundation

// MARK: - API Error
enum VideoDownloaderAPIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int)
    case decodingError(Error)
    case networkError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL format"
        case .invalidResponse:
            return "Invalid server response"
        case .httpError(let statusCode):
            return "HTTP error: \(statusCode)"
        case .decodingError(let error):
            return "Decoding error: \(error.localizedDescription)"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}

// MARK: - Video Downloader Service
class VideoDownloaderService {
    
    private let baseURL: String
    private let apiKey: String
    
    init(baseURL: String, apiKey: String) {
        self.baseURL = baseURL
        self.apiKey = apiKey
    }
    
    // MARK: - Generic Request Method
    private func makeRequest<T: Decodable, R: Encodable>(
        endpoint: String,
        method: String = "POST",
        body: R?,
        responseType: T.Type
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            throw VideoDownloaderAPIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw VideoDownloaderAPIError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw VideoDownloaderAPIError.httpError(statusCode: httpResponse.statusCode)
        }
        
        do {
            let decoder = JSONDecoder()
            return try decoder.decode(T.self, from: data)
        } catch {
            throw VideoDownloaderAPIError.decodingError(error)
        }
    }
    
    // MARK: - TikTok
    func downloadTikTok(url: String) async throws -> [String: Any] {
        guard let requestURL = URL(string: "\(baseURL)/api/v1/tiktok/download?url=\(url.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? url)") else {
            throw VideoDownloaderAPIError.invalidURL
        }
        
        var request = URLRequest(url: requestURL)
        request.httpMethod = "POST"
        request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw VideoDownloaderAPIError.invalidResponse
        }
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            throw VideoDownloaderAPIError.decodingError(NSError(domain: "", code: 0))
        }
        
        return json
    }
    
    func batchDownloadTikTok(urls: [String]) async throws -> [String: Any] {
        guard let requestURL = URL(string: "\(baseURL)/api/v1/tiktok/batch") else {
            throw VideoDownloaderAPIError.invalidURL
        }
        
        var request = URLRequest(url: requestURL)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        request.httpBody = try JSONEncoder().encode(urls)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw VideoDownloaderAPIError.invalidResponse
        }
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            throw VideoDownloaderAPIError.decodingError(NSError(domain: "", code: 0))
        }
        
        return json
    }
    
    // MARK: - Instagram
    func downloadInstagram(url: String, quality: Quality = .high) async throws -> DownloadResponse {
        let request = DownloadRequest(url: url, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/instagram/download",
            method: "POST",
            body: request,
            responseType: DownloadResponse.self
        )
    }
    
    func batchDownloadInstagram(urls: [String], quality: Quality = .high) async throws -> [DownloadResponse] {
        let request = BatchDownloadRequest(urls: urls, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/instagram/batch",
            method: "POST",
            body: request,
            responseType: [DownloadResponse].self
        )
    }
    
    // MARK: - Facebook
    func downloadFacebook(url: String, quality: Quality = .high) async throws -> DownloadResponse {
        let request = DownloadRequest(url: url, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/facebook/download",
            method: "POST",
            body: request,
            responseType: DownloadResponse.self
        )
    }
    
    func downloadFacebookAdvanced(url: String, quality: Quality = .high) async throws -> FacebookDownloadResponse {
        struct AdvancedRequest: Codable {
            let url: String
            let quality: String
            let include_metadata: Bool
            let include_captions: Bool
        }
        
        let request = AdvancedRequest(
            url: url,
            quality: quality.rawValue,
            include_metadata: true,
            include_captions: false
        )
        
        return try await makeRequest(
            endpoint: "/api/v1/facebook/download-advanced",
            method: "POST",
            body: request,
            responseType: FacebookDownloadResponse.self
        )
    }
    
    func batchDownloadFacebook(urls: [String], quality: Quality = .high) async throws -> [DownloadResponse] {
        let request = BatchDownloadRequest(urls: urls, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/facebook/batch",
            method: "POST",
            body: request,
            responseType: [DownloadResponse].self
        )
    }
    
    // MARK: - YouTube
    func downloadYouTube(url: String, quality: Quality = .high) async throws -> DownloadResponse {
        let request = DownloadRequest(url: url, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/youtube/download",
            method: "POST",
            body: request,
            responseType: DownloadResponse.self
        )
    }
    
    func downloadYouTubeAdvanced(url: String, quality: Quality = .high) async throws -> YouTubeDownloadResponse {
        struct AdvancedRequest: Codable {
            let url: String
            let quality: String
            let include_metadata: Bool
            let include_subtitles: Bool
        }
        
        let request = AdvancedRequest(
            url: url,
            quality: quality.rawValue,
            include_metadata: true,
            include_subtitles: false
        )
        
        return try await makeRequest(
            endpoint: "/api/v1/youtube/download-advanced",
            method: "POST",
            body: request,
            responseType: YouTubeDownloadResponse.self
        )
    }
    
    func batchDownloadYouTube(urls: [String], quality: Quality = .high) async throws -> [DownloadResponse] {
        let request = BatchDownloadRequest(urls: urls, quality: quality)
        return try await makeRequest(
            endpoint: "/api/v1/youtube/batch",
            method: "POST",
            body: request,
            responseType: [DownloadResponse].self
        )
    }
    
    // MARK: - Audio Extraction
    func extractAudio(url: String) async throws -> AudioExtractResponse {
        let request = AudioExtractRequest(url: url)
        return try await makeRequest(
            endpoint: "/api/v1/audio/extract",
            method: "POST",
            body: request,
            responseType: AudioExtractResponse.self
        )
    }
    
    func batchExtractAudio(urls: [String]) async throws -> [AudioExtractResponse] {
        let request = AudioBatchExtractRequest(urls: urls)
        return try await makeRequest(
            endpoint: "/api/v1/audio/batch-extract",
            method: "POST",
            body: request,
            responseType: [AudioExtractResponse].self
        )
    }
    
    // MARK: - Status Check
    func getStatus(sessionId: String, platform: Platform) async throws -> DownloadStatus {
        return try await makeRequest(
            endpoint: "/api/v1/\(platform.rawValue)/status/\(sessionId)",
            method: "GET",
            body: nil as String?,
            responseType: DownloadStatus.self
        )
    }
    
    // MARK: - Download File
    func getFullDownloadURL(relativePath: String) -> URL? {
        // Convert relative path like "/downloads/video.mp4" to full URL
        let cleanPath = relativePath.hasPrefix("/") ? String(relativePath.dropFirst()) : relativePath
        return URL(string: "\(baseURL)/\(cleanPath)")
    }
    
    func downloadFile(from relativePath: String) async throws -> Data {
        guard let url = getFullDownloadURL(relativePath: relativePath) else {
            throw VideoDownloaderAPIError.invalidURL
        }
        
        let (data, response) = try await URLSession.shared.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw VideoDownloaderAPIError.invalidResponse
        }
        
        return data
    }
}
```

### Usage Examples

```swift
// MARK: - Usage Examples

// Initialize the service
let service = VideoDownloaderService(
    baseURL: "https://tiktokwatermarkremover.com",
    apiKey: "YOUR_API_KEY"
)

// MARK: - TikTok Download
Task {
    do {
        let result = try await service.downloadTikTok(
            url: "https://www.tiktok.com/@user/video/123456789"
        )
        
        if let downloadPath = result["url"] as? String,
           let fullURL = service.getFullDownloadURL(relativePath: downloadPath) {
            print("Download URL: \(fullURL)")
        }
    } catch {
        print("TikTok download failed: \(error)")
    }
}

// MARK: - Instagram Download
Task {
    do {
        let response = try await service.downloadInstagram(
            url: "https://www.instagram.com/reel/ABC123/",
            quality: .high
        )
        
        if let downloadPath = response.downloadUrl,
           let fullURL = service.getFullDownloadURL(relativePath: downloadPath) {
            print("Download URL: \(fullURL)")
        }
    } catch {
        print("Instagram download failed: \(error)")
    }
}

// MARK: - Facebook Download with Metadata
Task {
    do {
        let response = try await service.downloadFacebookAdvanced(
            url: "https://www.facebook.com/reel/123456789",
            quality: .high
        )
        
        print("Title: \(response.metadata.title ?? "Unknown")")
        print("Author: \(response.metadata.author ?? "Unknown")")
        print("Duration: \(response.metadata.duration ?? 0) seconds")
        print("Content Type: \(response.contentType.rawValue)")
        
        if let fullURL = service.getFullDownloadURL(relativePath: response.downloadUrl) {
            print("Download URL: \(fullURL)")
        }
    } catch {
        print("Facebook download failed: \(error)")
    }
}

// MARK: - YouTube Shorts Download
Task {
    do {
        let response = try await service.downloadYouTubeAdvanced(
            url: "https://www.youtube.com/shorts/ABC123",
            quality: .high
        )
        
        print("Is Shorts: \(response.isShorts)")
        print("Title: \(response.metadata.title ?? "Unknown")")
        print("Views: \(response.metadata.viewCount ?? 0)")
        
        if let fullURL = service.getFullDownloadURL(relativePath: response.downloadUrl) {
            print("Download URL: \(fullURL)")
        }
    } catch {
        print("YouTube download failed: \(error)")
    }
}

// MARK: - Audio Extraction
Task {
    do {
        let response = try await service.extractAudio(
            url: "https://www.tiktok.com/@user/video/123456789"
        )
        
        print("Platform: \(response.platform ?? "Unknown")")
        print("Title: \(response.title ?? "Unknown")")
        print("Duration: \(response.duration ?? 0) seconds")
        
        if let audioPath = response.audioUrl,
           let fullURL = service.getFullDownloadURL(relativePath: audioPath) {
            print("Audio URL: \(fullURL)")
        }
    } catch {
        print("Audio extraction failed: \(error)")
    }
}

// MARK: - Batch Download (Mixed Platforms)
Task {
    do {
        // Extract audio from multiple platforms at once
        let results = try await service.batchExtractAudio(urls: [
            "https://www.tiktok.com/@user/video/123",
            "https://www.instagram.com/reel/ABC/",
            "https://www.youtube.com/watch?v=xyz"
        ])
        
        for result in results {
            print("[\(result.platform ?? "?")] \(result.title ?? "Unknown"): \(result.status)")
        }
    } catch {
        print("Batch extraction failed: \(error)")
    }
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Process response |
| `400` | Bad Request | Check request format |
| `401` | Unauthorized | Check API key |
| `404` | Not Found | Video may be deleted/private |
| `422` | Validation Error | Check URL format |
| `429` | Rate Limited | Wait and retry |
| `500` | Server Error | Retry later |

### Swift Error Handling Pattern

```swift
Task {
    do {
        let response = try await service.downloadFacebook(url: videoURL)
        // Handle success
    } catch VideoDownloaderAPIError.httpError(let statusCode) {
        switch statusCode {
        case 401:
            print("Invalid API key")
        case 404:
            print("Video not found or private")
        case 422:
            print("Invalid URL format")
        case 429:
            print("Rate limited - please wait")
        default:
            print("HTTP error: \(statusCode)")
        }
    } catch VideoDownloaderAPIError.invalidURL {
        print("Invalid URL format")
    } catch VideoDownloaderAPIError.networkError(let error) {
        print("Network error: \(error.localizedDescription)")
    } catch {
        print("Unknown error: \(error)")
    }
}
```

---

## Best Practices

### 1. URL Detection

```swift
func detectPlatform(from url: String) -> Platform? {
    let lowercased = url.lowercased()
    
    if lowercased.contains("tiktok.com") || lowercased.contains("vm.tiktok") {
        return .tiktok
    } else if lowercased.contains("instagram.com") {
        return .instagram
    } else if lowercased.contains("facebook.com") || lowercased.contains("fb.watch") {
        return .facebook
    } else if lowercased.contains("youtube.com") || lowercased.contains("youtu.be") {
        return .youtube
    }
    
    return nil
}
```

### 2. Universal Download Function

```swift
func downloadVideo(url: String, quality: Quality = .high) async throws -> String? {
    guard let platform = detectPlatform(from: url) else {
        throw VideoDownloaderAPIError.invalidURL
    }
    
    switch platform {
    case .tiktok:
        let result = try await service.downloadTikTok(url: url)
        return result["url"] as? String
    case .instagram:
        let result = try await service.downloadInstagram(url: url, quality: quality)
        return result.downloadUrl
    case .facebook:
        let result = try await service.downloadFacebook(url: url, quality: quality)
        return result.downloadUrl
    case .youtube:
        let result = try await service.downloadYouTube(url: url, quality: quality)
        return result.downloadUrl
    }
}
```

### 3. Save to Photos Library

```swift
import Photos

func saveVideoToPhotos(data: Data) async throws {
    try await PHPhotoLibrary.shared().performChanges {
        let options = PHAssetResourceCreationOptions()
        let request = PHAssetCreationRequest.forAsset()
        request.addResource(with: .video, data: data, options: options)
    }
}

// Usage
Task {
    if let downloadPath = response.downloadUrl {
        let videoData = try await service.downloadFile(from: downloadPath)
        try await saveVideoToPhotos(data: videoData)
        print("Video saved to Photos!")
    }
}
```

### 4. Progress Tracking with Combine

```swift
import Combine

class DownloadManager: ObservableObject {
    @Published var isLoading = false
    @Published var progress: Double = 0
    @Published var error: String?
    
    private let service: VideoDownloaderService
    
    init(service: VideoDownloaderService) {
        self.service = service
    }
    
    func download(url: String) async {
        await MainActor.run { isLoading = true }
        
        do {
            guard let platform = detectPlatform(from: url) else {
                throw VideoDownloaderAPIError.invalidURL
            }
            
            // Start download...
            // Poll for status updates...
            
        } catch {
            await MainActor.run { 
                self.error = error.localizedDescription 
            }
        }
        
        await MainActor.run { isLoading = false }
    }
}
```

---

## Quick Reference

### All Endpoints Summary

| Platform | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| TikTok | `/api/v1/tiktok/download` | POST | Single video |
| TikTok | `/api/v1/tiktok/batch` | POST | Multiple videos |
| TikTok | `/api/v1/tiktok/status/{id}` | GET | Check status |
| Instagram | `/api/v1/instagram/download` | POST | Single content |
| Instagram | `/api/v1/instagram/batch` | POST | Multiple contents |
| Instagram | `/api/v1/instagram/status/{id}` | GET | Check status |
| Facebook | `/api/v1/facebook/download` | POST | Single video |
| Facebook | `/api/v1/facebook/download-advanced` | POST | With metadata |
| Facebook | `/api/v1/facebook/batch` | POST | Multiple videos |
| Facebook | `/api/v1/facebook/batch-advanced` | POST | Batch with metadata |
| Facebook | `/api/v1/facebook/status/{id}` | GET | Check status |
| YouTube | `/api/v1/youtube/download` | POST | Single video |
| YouTube | `/api/v1/youtube/download-advanced` | POST | With metadata |
| YouTube | `/api/v1/youtube/batch` | POST | Multiple videos |
| YouTube | `/api/v1/youtube/batch-advanced` | POST | Batch with metadata |
| YouTube | `/api/v1/youtube/status/{id}` | GET | Check status |
| Audio | `/api/v1/audio/extract` | POST | Extract from any URL |
| Audio | `/api/v1/audio/batch-extract` | POST | Batch extraction |

---

## Support

For API issues, check:
1. API key is valid
2. URL format is correct
3. Video is public/accessible
4. Server is running

Server health check: `GET /health`
