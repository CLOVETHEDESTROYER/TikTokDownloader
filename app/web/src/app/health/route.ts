// frontend/src/app/health/route.ts
export async function GET() {
  try {
    // Use the backend service name and correct port from docker-compose
    const healthUrl = 'http://backend:8001/health';
    console.log('Proxying health check to:', healthUrl);
    
    const response = await fetch(healthUrl, {
      // Add these headers to ensure the request works within Docker network
      headers: {
        'Accept': 'application/json',
      },
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Health check failed:', errorText);
      return Response.json(
        { error: 'Health check failed', detail: errorText },
        { status: response.status }
      );
    }
    
    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error proxying health request:', error);
    
    return Response.json(
      { 
        error: 'Failed to check API health',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 