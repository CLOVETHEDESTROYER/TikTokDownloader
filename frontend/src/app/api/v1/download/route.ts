import { NextRequest } from 'next/server';

// Use a more basic approach without type annotations causing issues
export async function POST(request: NextRequest) {
  try {
    // Get request body
    const body = await request.json();
    
    // Get backend URL from environment or use default for development
    const backendUrl = '/api/v1/download';
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