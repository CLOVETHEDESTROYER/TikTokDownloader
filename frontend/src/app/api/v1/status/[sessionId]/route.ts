import { NextRequest } from 'next/server';

// Use a more basic approach without type annotations causing issues
export async function GET(request: NextRequest, context: { params: { sessionId: string } }) {
  const sessionId = context.params.sessionId;
  
  try {
    // Forward the request to the backend API using direct URL
    const backendUrl = `http://localhost:8000/api/v1/status/${sessionId}`;
    console.log('Forwarding status request to:', backendUrl);
    
    const response = await fetch(backendUrl, {
      headers: {
        'Accept': 'application/json',
        'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || 'website_key_456',
      }
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