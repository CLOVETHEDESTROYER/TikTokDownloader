import { NextRequest } from 'next/server';

// Use a more basic approach without type annotations causing issues
export async function GET(request: NextRequest, context: { params: { sessionId: string } }) {
  const sessionId = context.params.sessionId;
  
  try {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (process.env.NEXT_PUBLIC_WEBSITE_API_KEY) {
      headers['X-API-Key'] = process.env.NEXT_PUBLIC_WEBSITE_API_KEY;
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/status/${sessionId}`, {
      method: 'GET',
      headers,
    });
    
    // Get response data
    const data = await response.json();
    
    // If the backend returns an error, pass it through
    if (!response.ok) {
      console.error('Backend API error:', data);
      return Response.json(data, { status: response.status });
    }
    
    // Return the data
    return Response.json(data);
  } catch (error) {
    console.error('Error proxying status request:', error);
    
    return Response.json(
      { 
        error: 'Failed to get download status',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 