import { NextResponse } from 'next/server';
import { API_BASE_URL } from '../../../../../utils/api';

export async function GET(
  request: Request,
  { params }: { params: { sessionId: string } }
) {
  const sessionId = params.sessionId;
  
  try {
    // Forward the request to the backend API
    const backendUrl = `${API_BASE_URL}/status/${sessionId}`;
    
    const response = await fetch(backendUrl);
    
    // Get response data
    const data = await response.json();
    
    // If the backend returns an error, pass it through
    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }
    
    // Return the data
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error proxying status request:', error);
    
    return NextResponse.json(
      { 
        error: 'Failed to get download status',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 