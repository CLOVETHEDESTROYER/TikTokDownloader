# Facebook Video Download API - iOS Integration Guide

This document provides comprehensive documentation for integrating Facebook video download functionality into an iOS app using the TikTokDownloader backend API.

## Table of Contents

- [Base Configuration](#base-configuration)
- [Available Endpoints](#available-endpoints)
- [Request/Response Models](#requestresponse-models)
- [Swift Implementation Examples](#swift-implementation-examples)
- [Error Handling](#error-handling)
- [Supported Content Types](#supported-content-types)
- [Quality Options](#quality-options)
- [Testing Examples](#testing-examples)

---

## Base Configuration

### Base URL

The Facebook API endpoints are available at:

```
http://your-server-ip:8001/api/v1/facebook
```

Or via your domain:

```
https://your-domain.com/api/v1/facebook
```

### Headers

All requests should include:

```
Content-Type: application/json
```

If API key is required (check backend configuration):

```
X-API-Key: your-api-key-here
```

---

## Available Endpoints

### 1. Simple Download (Recommended)

**Endpoint:** `POST /api/v1/facebook/download`

**Description:** Download a single Facebook video with basic options.

**Request Body:**
```json
{
  "url": "https://www.facebook.com/watch/...",
  "quality": "high"
}
```

**Parameters:**
- `url` (string, required): Facebook video URL (must be from facebook.com or fb.watch)
- `quality` (string, optional): Video quality - `"high"`, `"medium"`, or `"low"` (default: `"high"`)

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "message": "Facebook video downloaded successfully",
  "download_url": "/downloads/facebook_abc123.mp4",
  "title": "Video Title",
  "author": "Page Name",
  "duration": 120.5,
  "is_live": false,
  "content_type": "video"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid URL)
- `422` - Validation Error
- `500` - Server Error

---

### 2. Advanced Download (With Metadata)

**Endpoint:** `POST /api/v1/facebook/download-advanced`

**Description:** Download a Facebook video with detailed metadata and advanced options.

**Request Body:**
```json
{
  "url": "https://www.facebook.com/watch/...",
  "quality": "high",
  "include_metadata": true,
  "include_captions": false
}
```

**Parameters:**
- `url` (string, required): Facebook video URL
- `quality` (string, optional): `"high"`, `"medium"`, or `"low"` (default: `"high"`)
- `include_metadata` (boolean, optional): Include detailed metadata (default: `true`)
- `include_captions` (boolean, optional): Include captions/subtitles (default: `false`)

**Response:**
```json
{
  "url": "https://www.facebook.com/watch/...",
  "download_url": "/downloads/facebook_abc123.mp4",
  "content_type": "video",
  "session_id": "uuid-string",
  "is_live": false,
  "metadata": {
    "title": "Video Title",
    "author": "Page Name",
    "duration": 120.5,
    "view_count": 1000,
    "like_count": 50,
    "description": "Video description text",
    "upload_date": "20240101",
    "content_type": "video",
    "is_live": false,
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "page_name": "Page Name"
  }
}
```

---

### 3. Batch Download

**Endpoint:** `POST /api/v1/facebook/batch`

**Description:** Download multiple Facebook videos in a single request.

**Request Body:**
```json
{
  "urls": [
    "https://www.facebook.com/watch/...",
    "https://www.facebook.com/reel/...",
    "https://fb.watch/..."
  ],
  "quality": "high"
}
```

**Parameters:**
- `urls` (array, required): Array of Facebook video URLs (min 1)
- `quality` (string, optional): `"high"`, `"medium"`, or `"low"` (default: `"high"`)

**Response:** Array of download responses (same format as simple download)

```json
[
  {
    "session_id": "uuid-1",
    "status": "completed",
    "download_url": "/downloads/facebook_abc123.mp4",
    ...
  },
  {
    "session_id": "uuid-2",
    "status": "completed",
    "download_url": "/downloads/facebook_def456.mp4",
    ...
  }
]
```

---

### 4. Batch Advanced Download

**Endpoint:** `POST /api/v1/facebook/batch-advanced`

**Description:** Download multiple Facebook videos with advanced options and metadata.

**Request Body:**
```json
{
  "urls": [
    "https://www.facebook.com/watch/...",
    "https://www.facebook.com/reel/..."
  ],
  "quality": "high",
  "include_metadata": true
}
```

**Response:** Array of advanced download responses (same format as advanced download)

---

### 5. Check Download Status

**Endpoint:** `GET /api/v1/facebook/status/{session_id}`

**Description:** Check the status of a download by session ID.

**URL Parameters:**
- `session_id` (string, required): Session ID returned from download request

**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "progress": 100
}
```

---

### 6. Get Reel Information

**Endpoint:** `GET /api/v1/facebook/reel-info/{video_id}`

**Description:** Get information about a Facebook Reel without downloading.

**URL Parameters:**
- `video_id` (string, required): Facebook video/reel ID

**Response:**
```json
{
  "video_id": "video-id-here",
  "is_reel": true
}
```

**Note:** This endpoint currently returns basic information. Full implementation may be added in future.

---

## Request/Response Models

### Quality Enum

```swift
enum FacebookQuality: String, Codable {
    case high = "high"      // Up to 1080p
    case medium = "medium"  // Up to 720p
    case low = "low"        // Up to 480p
}
```

### Content Type Enum

```swift
enum FacebookContentType: String, Codable {
    case video = "video"
    case reel = "reel"
    case live = "live"
    case story = "story"
    case post = "post"
}
```

### Simple Download Request

```swift
struct FacebookDownloadRequest: Codable {
    let url: String
    let quality: String  // "high", "medium", or "low"
}
```

### Simple Download Response

```swift
struct FacebookDownloadResponse: Codable {
    let session_id: String
    let status: String
    let message: String
    let download_url: String
    let title: String?
    let author: String?
    let duration: Double?
    let is_live: Bool
    let content_type: String
}
```

### Advanced Download Request

```swift
struct FacebookAdvancedDownloadRequest: Codable {
    let url: String
    let quality: FacebookQuality
    let include_metadata: Bool?
    let include_captions: Bool?
}
```

### Advanced Download Response

```swift
struct FacebookAdvancedDownloadResponse: Codable {
    let url: String
    let download_url: String
    let content_type: FacebookContentType
    let session_id: String
    let is_live: Bool
    let metadata: FacebookMediaMetadata
}

struct FacebookMediaMetadata: Codable {
    let title: String?
    let author: String?
    let duration: Double?
    let view_count: Int?
    let like_count: Int?
    let description: String?
    let upload_date: String?
    let content_type: FacebookContentType
    let is_live: Bool
    let thumbnail_url: String?
    let page_name: String?
}
```

---

## Swift Implementation Examples

### Complete Swift Service Implementation

```swift
import Foundation

class FacebookDownloadService {
    private let baseURL: String
    private let apiKey: String?
    
    init(baseURL: String, apiKey: String? = nil) {
        self.baseURL = baseURL
        self.apiKey = apiKey
    }
    
    // MARK: - Simple Download
    
    func downloadVideo(url: String, quality: String = "high") async throws -> FacebookDownloadResponse {
        let endpoint = "\(baseURL)/api/v1/facebook/download"
        let requestBody = FacebookDownloadRequest(url: url, quality: quality)
        
        return try await performRequest(
            endpoint: endpoint,
            method: "POST",
            body: requestBody,
            responseType: FacebookDownloadResponse.self
        )
    }
    
    // MARK: - Advanced Download
    
    func downloadVideoAdvanced(
        url: String,
        quality: FacebookQuality = .high,
        includeMetadata: Bool = true,
        includeCaptions: Bool = false
    ) async throws -> FacebookAdvancedDownloadResponse {
        let endpoint = "\(baseURL)/api/v1/facebook/download-advanced"
        let requestBody = FacebookAdvancedDownloadRequest(
            url: url,
            quality: quality,
            include_metadata: includeMetadata,
            include_captions: includeCaptions
        )
        
        return try await performRequest(
            endpoint: endpoint,
            method: "POST",
            body: requestBody,
            responseType: FacebookAdvancedDownloadResponse.self
        )
    }
    
    // MARK: - Batch Download
    
    func batchDownload(urls: [String], quality: String = "high") async throws -> [FacebookDownloadResponse] {
        let endpoint = "\(baseURL)/api/v1/facebook/batch"
        let requestBody: [String: Any] = [
            "urls": urls,
            "quality": quality
        ]
        
        return try await performRequest(
            endpoint: endpoint,
            method: "POST",
            body: requestBody,
            responseType: [FacebookDownloadResponse].self
        )
    }
    
    // MARK: - Check Status
    
    func checkStatus(sessionId: String) async throws -> DownloadStatus {
        let endpoint = "\(baseURL)/api/v1/facebook/status/\(sessionId)"
        
        return try await performRequest(
            endpoint: endpoint,
            method: "GET",
            body: nil as String?,
            responseType: DownloadStatus.self
        )
    }
    
    // MARK: - Helper Methods
    
    private func performRequest<T: Codable, U: Codable>(
        endpoint: String,
        method: String,
        body: T?,
        responseType: U.Type
    ) async throws -> U {
        guard let url = URL(string: endpoint) else {
            throw FacebookAPIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let apiKey = apiKey {
            request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        }
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw FacebookAPIError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw FacebookAPIError.httpError(statusCode: httpResponse.statusCode)
        }
        
        do {
            return try JSONDecoder().decode(responseType, from: data)
        } catch {
            throw FacebookAPIError.decodingError(error)
        }
    }
    
    // MARK: - Get Full Download URL
    
    func getFullDownloadURL(relativePath: String) -> String {
        // Convert relative path like "/downloads/facebook_abc123.mp4"
        // to full URL like "http://server:8001/downloads/facebook_abc123.mp4"
        let base = baseURL.replacingOccurrences(of: "/api/v1/facebook", with: "")
        return "\(base)\(relativePath)"
    }
}

// MARK: - Error Handling

enum FacebookAPIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int)
    case decodingError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let code):
            return "HTTP Error: \(code)"
        case .decodingError(let error):
            return "Decoding Error: \(error.localizedDescription)"
        }
    }
}

struct DownloadStatus: Codable {
    let session_id: String
    let status: String
    let progress: Int
}
```

### Usage Example

```swift
// Initialize service
let service = FacebookDownloadService(
    baseURL: "http://your-server:8001",
    apiKey: "your-api-key" // Optional
)

// Download a video
do {
    let response = try await service.downloadVideo(
        url: "https://www.facebook.com/watch/...",
        quality: "high"
    )
    
    print("Download completed!")
    print("Session ID: \(response.session_id)")
    print("Download URL: \(response.download_url)")
    print("Title: \(response.title ?? "N/A")")
    
    // Get full URL for downloading the file
    let fullURL = service.getFullDownloadURL(relativePath: response.download_url)
    print("Full URL: \(fullURL)")
    
    // Download the actual video file
    if let fileURL = URL(string: fullURL) {
        let (data, _) = try await URLSession.shared.data(from: fileURL)
        // Save data to file or display in app
    }
    
} catch {
    print("Error: \(error.localizedDescription)")
}
```

### Advanced Download Example

```swift
do {
    let response = try await service.downloadVideoAdvanced(
        url: "https://www.facebook.com/reel/...",
        quality: .high,
        includeMetadata: true
    )
    
    print("Content Type: \(response.content_type)")
    print("Is Live: \(response.is_live)")
    print("Metadata:")
    print("  Title: \(response.metadata.title ?? "N/A")")
    print("  Author: \(response.metadata.author ?? "N/A")")
    print("  Duration: \(response.metadata.duration ?? 0) seconds")
    print("  Views: \(response.metadata.view_count ?? 0)")
    print("  Likes: \(response.metadata.like_count ?? 0)")
    print("  Thumbnail: \(response.metadata.thumbnail_url ?? "N/A")")
    
} catch {
    print("Error: \(error.localizedDescription)")
}
```

---

## Error Handling

### Common HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request format or parameters
- `422 Unprocessable Entity` - Validation error (e.g., invalid Facebook URL)
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Error Handling Example

```swift
do {
    let response = try await service.downloadVideo(url: videoURL)
    // Handle success
} catch FacebookAPIError.httpError(let statusCode) {
    switch statusCode {
    case 400:
        print("Bad request - check your URL")
    case 422:
        print("Invalid Facebook URL format")
    case 429:
        print("Too many requests - please wait")
    case 500:
        print("Server error - please try again later")
    default:
        print("HTTP Error: \(statusCode)")
    }
} catch {
    print("Error: \(error.localizedDescription)")
}
```

---

## Supported Content Types

The API automatically detects and supports:

1. **Regular Videos** (`video`)
   - Standard Facebook video posts
   - URL format: `https://www.facebook.com/watch/?v=...`

2. **Facebook Reels** (`reel`)
   - Short-form video content
   - URL format: `https://www.facebook.com/reel/...`

3. **Live Videos** (`live`)
   - Currently streaming or recorded live videos
   - API will attempt to download the recorded version

4. **Stories** (`story`)
   - Facebook Stories (if downloadable)

5. **Posts** (`post`)
   - Video posts embedded in regular posts

### Supported URL Formats

- `https://www.facebook.com/watch/?v=VIDEO_ID`
- `https://www.facebook.com/watch/VIDEO_ID`
- `https://www.facebook.com/reel/REEL_ID`
- `https://fb.watch/WATCH_ID`
- `https://m.facebook.com/watch/?v=VIDEO_ID`
- Other Facebook video URL variations

---

## Quality Options

### High Quality (Recommended)
- Resolution: Up to 1080p
- File Size: Largest
- Use Case: Best viewing experience, storage available

### Medium Quality
- Resolution: Up to 720p
- File Size: Medium
- Use Case: Balanced quality and file size

### Low Quality
- Resolution: Up to 480p
- File Size: Smallest
- Use Case: Faster downloads, limited storage, previews

---

## Testing Examples

### cURL Examples

**Simple Download:**
```bash
curl -X POST http://your-server:8001/api/v1/facebook/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "url": "https://www.facebook.com/watch/...",
    "quality": "high"
  }'
```

**Advanced Download:**
```bash
curl -X POST http://your-server:8001/api/v1/facebook/download-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/reel/...",
    "quality": "high",
    "include_metadata": true
  }'
```

**Check Status:**
```bash
curl http://your-server:8001/api/v1/facebook/status/SESSION_ID
```

### Swift Testing

```swift
// Test in Swift Playground or unit tests
let service = FacebookDownloadService(baseURL: "http://localhost:8001")

Task {
    do {
        let response = try await service.downloadVideo(
            url: "https://www.facebook.com/watch/...",
            quality: "high"
        )
        print("✅ Success: \(response)")
    } catch {
        print("❌ Error: \(error)")
    }
}
```

---

## Important Notes

1. **Download URL Format**
   - The `download_url` in the response is a relative path (e.g., `/downloads/facebook_abc123.mp4`)
   - Convert to full URL: `http://server:8001/downloads/facebook_abc123.mp4`
   - The file is available immediately after the download completes

2. **Session IDs**
   - Each download returns a unique `session_id`
   - Use this to check download status if needed
   - Session IDs can be used for tracking downloads

3. **Content Type Detection**
   - The API automatically detects if content is a video, reel, live, story, or post
   - This information is available in the response for UI customization

4. **Rate Limiting**
   - The backend may implement rate limiting
   - Handle 429 status codes appropriately
   - Implement exponential backoff for retries

5. **Video Availability**
   - Some Facebook videos may be private or restricted
   - The API will return appropriate error codes for unavailable content
   - Public videos and videos accessible to the server are supported

6. **File Persistence**
   - Downloaded files are stored on the server
   - Files may be cleaned up after expiration (check backend configuration)
   - Download files promptly after receiving the download URL

7. **Metadata**
   - Metadata availability depends on what Facebook provides
   - Some fields may be `null` if unavailable
   - Always handle optional fields appropriately

---

## Integration Checklist

- [ ] Configure base URL in your iOS app
- [ ] Set up API key if required by backend
- [ ] Implement request/response models
- [ ] Create service class for API calls
- [ ] Implement error handling
- [ ] Handle download URL conversion (relative to absolute)
- [ ] Implement file download functionality
- [ ] Add loading states for async operations
- [ ] Test with various Facebook URL formats
- [ ] Test with different quality options
- [ ] Handle edge cases (private videos, errors, etc.)
- [ ] Implement retry logic for network errors
- [ ] Add user feedback for download progress

---

## Additional Resources

- Backend API Documentation: Check `/docs` endpoint on your server
- OpenAPI Schema: Available at `/openapi.json`
- Backend GitHub: [Repository URL]
- Support: [Your support contact]

---

## Version Information

- API Version: `v1`
- Last Updated: January 2026
- Backend Version: Check `/health` endpoint for version info

