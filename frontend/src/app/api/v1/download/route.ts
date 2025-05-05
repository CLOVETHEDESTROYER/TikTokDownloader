import { NextRequest } from 'next/server';

// Use a more basic approach without type annotations causing issues
export async function POST(request: NextRequest) {
  try {
    // Get request body
    const body = await request.json();
    
    // Determine if we're running on the server or client
    const isServer = typeof window === 'undefined';

    // Build the backend URL
    let backendUrl: string;

    if (isServer) {
      // On the server, use the full URL (from env or fallback)
      // DigitalOcean: NEXT_PUBLIC_API_URL should be set to /api/v1
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      backendUrl = apiBase.endsWith('/download') ? apiBase : `${apiBase}/download`;
    } else {
      // On the client, use a relative path
      backendUrl = '/api/v1/download';
    }

    console.log('Forwarding download request to:', backendUrl);
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (process.env.NEXT_PUBLIC_WEBSITE_API_KEY) {
      headers['X-API-Key'] = process.env.NEXT_PUBLIC_WEBSITE_API_KEY;
    }

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
    
    // Get response data
    const contentType = response.headers.get('Content-Type') || '';
    let data;
    
    if (contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = { message: await response.text() };
    }
    
    // If the backend returns an error, pass it through
    if (!response.ok) {
      console.error('Backend API error:', data);
      return Response.json(data, { status: response.status });
    }
    
    // Return the data
    return Response.json(data);
  } catch (error) {
    console.error('Error proxying download request:', error);
    
    return Response.json(
      { 
        error: 'Failed to create download',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 