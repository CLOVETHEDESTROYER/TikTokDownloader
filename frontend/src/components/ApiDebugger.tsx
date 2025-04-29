import { useEffect, useState } from 'react';
import { API_BASE_URL, FRONTEND_API_BASE_URL } from '../utils/api';
import { checkApiHealth } from '../utils/apiDirect';

interface DebugInfo {
  API_BASE_URL: string;
  FRONTEND_API_BASE_URL: string;
  NODE_ENV: string | undefined;
  NEXT_PUBLIC_API_URL: string | undefined;
  apiHealth: {
    status: 'loading' | 'success' | 'error';
    message: string;
    data?: any;
  };
}

export default function ApiDebugger() {
  const [debugInfo, setDebugInfo] = useState<DebugInfo>({
    API_BASE_URL,
    FRONTEND_API_BASE_URL,
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    apiHealth: {
      status: 'loading',
      message: 'Checking API health...',
    }
  });
  
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Check API health
    checkApiHealth()
      .then(data => {
        setDebugInfo(prev => ({
          ...prev,
          apiHealth: {
            status: 'success',
            message: 'API is healthy',
            data
          }
        }));
      })
      .catch(error => {
        setDebugInfo(prev => ({
          ...prev,
          apiHealth: {
            status: 'error',
            message: `API health check failed: ${error.message}`
          }
        }));
      });
  }, []);

  if (!isVisible) {
    return (
      <button 
        onClick={() => setIsVisible(true)}
        className="fixed bottom-2 right-2 bg-blue-500 text-white p-2 rounded shadow z-50"
      >
        Show API Debug
      </button>
    );
  }

  return (
    <div className="fixed bottom-0 right-0 w-full md:w-96 bg-white border border-gray-200 shadow-lg rounded-t-lg z-50 p-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-bold">API Debug Info</h3>
        <button 
          onClick={() => setIsVisible(false)}
          className="text-gray-500 hover:text-gray-700"
        >
          Hide
        </button>
      </div>
      
      <div className="space-y-2 text-xs font-mono overflow-auto max-h-60">
        <div className="p-2 bg-gray-100 rounded">
          <p>API_BASE_URL: {debugInfo.API_BASE_URL}</p>
          <p>FRONTEND_API_BASE_URL: {debugInfo.FRONTEND_API_BASE_URL}</p>
          <p>NODE_ENV: {debugInfo.NODE_ENV}</p>
          <p>NEXT_PUBLIC_API_URL: {debugInfo.NEXT_PUBLIC_API_URL || 'not set'}</p>
        </div>
        
        <div className={`p-2 rounded ${
          debugInfo.apiHealth.status === 'success' 
            ? 'bg-green-100' 
            : debugInfo.apiHealth.status === 'error'
              ? 'bg-red-100'
              : 'bg-yellow-100'
        }`}>
          <p>API Health: {debugInfo.apiHealth.message}</p>
          {debugInfo.apiHealth.data && (
            <pre className="mt-1 text-xs">
              {JSON.stringify(debugInfo.apiHealth.data, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
} 