// Import only necessary modules
const { API_BASE_URL } = require('../../../../utils/api');

// Use a more basic approach without type annotations causing issues
export async function POST(request) {
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