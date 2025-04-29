// Type definitions for Next.js 15+ App Router
declare module 'next/server' {
  export class NextResponse extends Response {
    static json(body: any, init?: ResponseInit): NextResponse;
  }

  export type NextRequest = Request;

  // Define the correct context param structure for route handlers
  export interface RouteHandlerContext {
    params: Record<string, string | string[]>;
  }
}

// Define correct route handler types
declare module 'next' {
  export interface RouteSegmentConfig {
    dynamic?: 'auto' | 'force-dynamic' | 'error' | 'force-static';
    revalidate?: false | 0 | number;
    fetchCache?: 'auto' | 'default-cache' | 'only-cache' | 'force-cache' | 'force-no-store' | 'default-no-store' | 'only-no-store';
    runtime?: 'nodejs' | 'edge';
    preferredRegion?: 'auto' | 'global' | 'home' | string | string[];
  }
}

// Additional type declaration to allow the correct route handler parameters
declare namespace NextApiRequest {
  interface Context {
    params: Record<string, string | string[]>;
  }
} 