'use client';

import React, { useState } from 'react';
import { AlertCircle, Download, ExternalLink, Loader2, TestTube } from 'lucide-react';
import { downloadSoraVideo, testSoraExtraction, isValidSoraUrl, SoraVideoData, SoraTestResult } from '@/services/soraService';
import ProcessingProgress from './ProcessingProgress';

type QualityOption = 'high' | 'medium' | 'low';

interface SoraDownloadFormProps {
  onVideoFetched: (videoData: SoraVideoData) => void;
}

const SoraDownloadForm: React.FC<SoraDownloadFormProps> = ({ onVideoFetched }) => {
  const [url, setUrl] = useState('');
  const [quality, setQuality] = useState<QualityOption>('high');
  const [cookies, setCookies] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<SoraTestResult | null>(null);
  const [processingStage, setProcessingStage] = useState<'analyzing' | 'downloading' | 'processing'>('analyzing');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isValidSoraUrl(url)) {
      setError('Please enter a valid Sora 2 video URL');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setProcessingStage('analyzing');
    
    try {
      // Simulate the stages with delays
      await new Promise(resolve => setTimeout(resolve, 1000));
      setProcessingStage('downloading');
      
      await new Promise(resolve => setTimeout(resolve, 1500));
      setProcessingStage('processing');
      
      // Call the download service with the selected quality and cookies
      const videoData = await downloadSoraVideo(url, quality, cookies || undefined);
      onVideoFetched(videoData);
    } catch (err: unknown) {
      let errorMessage = 'Failed to process this video. Please try again or try another URL.';
      
      if (err instanceof Error && err.message) {
        if (err.message.includes('validation')) {
          errorMessage = 'Invalid URL format. Please make sure you\'re using a correct Sora 2 video URL.';
        } else if (err.message.includes('status 403')) {
          errorMessage = 'This video is private or restricted. Please try another video.';
        } else if (err.message.includes('status 404')) {
          errorMessage = 'Video not found. The URL may be incorrect or the video has been removed.';
        } else if (err.message.includes('status 429')) {
          errorMessage = 'Too many requests. Please wait a few minutes and try again.';
        } else if (err.message.includes('status 5')) {
          errorMessage = 'Server error. Our backend is having issues. Please try again later.';
        } else {
          errorMessage = `Error: ${err.message}`;
        }
      }
      
      setError(errorMessage);
      console.error('Download error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTest = async () => {
    if (!isValidSoraUrl(url)) {
      setError('Please enter a valid Sora 2 video URL first');
      return;
    }
    
    setIsTesting(true);
    setError(null);
    setTestResult(null);
    
    try {
      const result = await testSoraExtraction(url, cookies || undefined);
      setTestResult(result);
    } catch (err: unknown) {
      let errorMessage = 'Failed to test video extraction.';
      
      if (err instanceof Error && err.message) {
        errorMessage = `Test Error: ${err.message}`;
      }
      
      setError(errorMessage);
      console.error('Test error:', err);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <>
      <ProcessingProgress 
        isVisible={isLoading} 
        stage={processingStage}
      />
      
      <div className="w-full max-w-3xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8 transition-all duration-300">
          <h2 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Download Sora 2 Videos Without Watermark
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Extract and download AI-generated videos from OpenAI Sora 2 without watermarks
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="sora-url" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Sora 2 Video URL
              </label>
              <div className="flex space-x-2">
                <input
                  id="sora-url"
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://sora.chatgpt.com/p/s_..."
                  className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  disabled={isLoading || isTesting}
                />
                <button
                  type="button"
                  onClick={handleTest}
                  disabled={isLoading || isTesting || !url.trim()}
                  className="px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
                >
                  {isTesting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <TestTube className="w-4 h-4" />
                  )}
                  <span className="hidden sm:inline">Test</span>
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="cookies" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                ChatGPT Cookies (Optional)
              </label>
              <textarea
                id="cookies"
                value={cookies}
                onChange={(e) => setCookies(e.target.value)}
                placeholder="Paste your ChatGPT cookies here for authentication (optional)"
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white h-24 resize-none"
                disabled={isLoading || isTesting}
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Required for accessing private Sora videos. Get cookies from browser dev tools.
              </p>
            </div>

            <div>
              <label htmlFor="quality" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Quality
              </label>
              <select
                id="quality"
                value={quality}
                onChange={(e) => setQuality(e.target.value as QualityOption)}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                disabled={isLoading || isTesting}
              >
                <option value="high">High Quality (1080p+)</option>
                <option value="medium">Medium Quality (720p)</option>
                <option value="low">Low Quality (480p)</option>
              </select>
            </div>

            {error && (
              <div className="flex items-center space-x-2 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                <p className="text-red-700 dark:text-red-400 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || isTesting || !url.trim()}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 transition-colors font-medium"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Download className="w-5 h-5" />
              )}
              <span>{isLoading ? 'Processing...' : 'Download Without Watermark'}</span>
            </button>
          </form>

          {/* Test Results */}
          {testResult && (
            <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                🧪 Test Results
              </h3>
              <div className="space-y-2 text-sm">
                <p><strong>Title:</strong> {testResult.title || 'Unknown'}</p>
                <p><strong>Extractor:</strong> {testResult.extractor}</p>
                <p><strong>Duration:</strong> {testResult.duration ? `${testResult.duration}s` : 'Unknown'}</p>
                <p><strong>Uploader:</strong> {testResult.uploader || 'Unknown'}</p>
                <p><strong>Formats Found:</strong> {testResult.formats?.length || 0}</p>
                
                {testResult.formats && testResult.formats.length > 0 && (
                  <div className="mt-3">
                    <p className="font-medium mb-2">Available Formats:</p>
                    <div className="max-h-32 overflow-y-auto space-y-1">
                      {testResult.formats.slice(0, 5).map((format, index) => (
                        <div key={index} className="text-xs bg-white dark:bg-gray-600 p-2 rounded">
                          <span className="font-mono">{format.ext || 'unknown'}</span>
                          {format.format_note && (
                            <span className="text-gray-500 ml-2">({format.format_note})</span>
                          )}
                          {format.resolution && (
                            <span className="text-gray-500 ml-2">- {format.resolution}</span>
                          )}
                        </div>
                      ))}
                      {testResult.formats.length > 5 && (
                        <p className="text-gray-500 text-xs">... and {testResult.formats.length - 5} more</p>
                      )}
                    </div>
                  </div>
                )}
                
                {testResult.error && (
                  <div className="mt-3 p-2 bg-red-100 dark:bg-red-900/30 rounded text-red-700 dark:text-red-400">
                    <strong>Error:</strong> {testResult.error}
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              💡 <strong>Tip:</strong> Use the "Test" button first to see what formats are available before downloading
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default SoraDownloadForm;
