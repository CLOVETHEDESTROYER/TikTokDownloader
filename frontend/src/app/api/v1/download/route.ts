import { NextRequest, NextResponse } from 'next/server';
import { API_BASE_URL } from '../../../../utils/api';

export async function POST(request: NextRequest) {
  try {
    // Get request body
    const body = await request.json();
    
    // Forward the request to the backend API
    const backendUrl = `${API_BASE_URL}/download`;
    
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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
      return NextResponse.json(data, { status: response.status });
    }
    
    // Return the data
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error proxying download request:', error);
    
    return NextResponse.json(
      { 
        error: 'Failed to create download',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 