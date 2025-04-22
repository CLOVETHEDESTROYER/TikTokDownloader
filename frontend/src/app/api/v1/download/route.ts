import { NextRequest, NextResponse } from 'next/server';

export const POST = async (req: NextRequest) => {
  try {
    const body = await req.json();
    
    // Forward the request to your backend API
    const backendUrl = 'http://localhost:8000/api/v1/download';
    
    // Log the request being sent to the backend
    console.log('Forwarding request to backend:', body);
    
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    // Log response status
    console.log(`Backend response status: ${response.status}`);
    
    // Get response body as text first
    const responseText = await response.text();
    console.log('Raw response:', responseText);
    
    // Try to parse JSON
    let data;
    try {
      // Only try to parse if there's content
      data = responseText ? JSON.parse(responseText) : {};
    } catch (jsonError) {
      console.error('Error parsing JSON response:', jsonError);
      return NextResponse.json(
        { 
          error: 'Invalid response from server', 
          detail: 'The server returned an invalid JSON response' 
        },
        { status: 500 }
      );
    }
    
    // For 422 errors, return the validation errors from FastAPI
    if (response.status === 422) {
      console.error('Validation error from backend:', data);
      return NextResponse.json(
        { 
          error: 'Validation error', 
          detail: data.detail || 'The request was rejected due to validation errors',
          validation_errors: data.detail
        },
        { status: 422 }
      );
    }

    if (!response.ok) {
      console.error('Error response from backend:', data);
      return NextResponse.json(
        { 
          error: 'Backend error', 
          detail: data.detail || `Backend returned status ${response.status}`
        },
        { status: response.status }
      );
    }
    
    // Log successful response for debugging
    console.log('Received response from backend:', data);
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in download API route:', error);
    return NextResponse.json(
      { 
        error: 'Failed to process download request', 
        detail: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    );
  }
} 