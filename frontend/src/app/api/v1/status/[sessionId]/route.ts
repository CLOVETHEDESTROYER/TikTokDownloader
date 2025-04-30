// Import only necessary modules
const { API_BASE_URL } = require('../../../../../utils/api');

// Use a more basic approach without type annotations causing issues
export async function GET(request, context) {
  const sessionId = context.params.sessionId;
  
  try {
    // Forward the request to the backend API using direct URL
    const backendUrl = `http://localhost:8000/api/v1/status/${sessionId}`;
    console.log('Forwarding status request to:', backendUrl);
    
    const response = await fetch(backendUrl);
    
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