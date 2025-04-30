// No imports needed
export async function GET(request, context) {
  try {
    const sessionId = context.params.sessionId;

    // Forward the request to the backend API using the correct path
    const backendUrl = `http://localhost:8000/api/v1/file/${sessionId}`;

    console.log(`Proxying file download request to: ${backendUrl}`);

    const response = await fetch(backendUrl, {
      method: "GET",
      headers: {
        Accept: "video/mp4",
      },
    });

    // If the backend returns an error, pass it through
    if (!response.ok) {
      console.error(`Error from backend: ${response.status}`);

      try {
        const errorData = await response.json();
        return Response.json(
          {
            error: errorData.detail || `Failed with status: ${response.status}`,
            detail: errorData.detail,
          },
          { status: response.status }
        );
      } catch {
        // If we can't parse JSON error, return a generic error
        return Response.json(
          { error: `Failed with status: ${response.status}` },
          { status: response.status }
        );
      }
    }

    // Get the file content as an array buffer
    const fileBuffer = await response.arrayBuffer();

    // Get the content type and other headers from the backend response
    const contentType = response.headers.get("Content-Type") || "video/mp4";
    const contentDisposition = response.headers.get("Content-Disposition");

    // Create response with proper headers for download
    const res = new Response(fileBuffer, {
      status: 200,
      headers: {
        "Content-Type": contentType,
        "Content-Disposition":
          contentDisposition || 'attachment; filename="video.mp4"',
        "Cache-Control": "no-cache, no-store, must-revalidate",
        Pragma: "no-cache",
        Expires: "0",
      },
    });

    return res;
  } catch (error) {
    console.error("Error proxying file download:", error);

    return Response.json(
      {
        error: "Failed to download file",
        detail: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
