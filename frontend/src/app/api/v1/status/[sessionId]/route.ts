// Import only necessary modules
const { API_BASE_URL } = require('../../../../../utils/api');

// Use a more basic approach without type annotations causing issues
export async function GET(request, context) {
  const sessionId = context.params.sessionId;
  
  try {
    // Forward the request to the backend API
    const backendUrl = `${API_BASE_URL}/status/${sessionId}`;
    
    const response = await fetch(backendUrl);
    
    // Get response data
    const data = await response.json();
    
    // If the backend returns an error, pass it through
    if (!response.ok) {
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