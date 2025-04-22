'use client';

import React from 'react';
import { Shield, Download, Zap, CheckCircle, Banknote, RefreshCw, HelpCircle } from 'lucide-react';
import AdBanner from '@/components/AdBanner';

const AboutPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-6 text-center bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
          How TikSave Works
        </h1>
        
        <p className="text-lg text-tiktok-dark/80 dark:text-gray-300 mb-10 text-center">
          Our service makes it easy to download TikTok videos without the watermark, 
          all while maintaining the highest quality possible.
        </p>
        
        {/* Main Content */}
        <div className="bg-white/90 dark:bg-gray-800 rounded-xl shadow-lg border border-tiktok-secondary/20 p-6 md:p-8 mb-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
            The Process
          </h2>
          
          <div className="space-y-8">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-tiktok-secondary/20 dark:bg-tiktok-secondary/30 flex items-center justify-center flex-shrink-0">
                <Download className="w-5 h-5 text-tiktok-primary dark:text-tiktok-secondary" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                  Video Processing
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  When you enter a TikTok URL, our system fetches the video from TikTok&apos;s servers. 
                  We process the video to extract the original content without the watermark that 
                  TikTok adds to all downloaded videos.
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-tiktok-primary/10 dark:bg-tiktok-primary/20 flex items-center justify-center flex-shrink-0">
                <Zap className="w-5 h-5 text-tiktok-primary dark:text-tiktok-secondary" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                  Quality Options
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  We provide multiple quality options for your downloads. You can choose between 
                  HD quality for the best viewing experience or a lower quality for faster downloads 
                  and smaller file sizes.
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-tiktok-accent/10 dark:bg-tiktok-accent/20 flex items-center justify-center flex-shrink-0">
                <Shield className="w-5 h-5 text-tiktok-accent dark:text-tiktok-secondary" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                  Privacy and Security
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Your privacy is important to us. We don&apos;t store the videos on our servers permanently, 
                  and all downloads are processed securely. We also don&apos;t require you to create an account 
                  or provide any personal information to use our service.
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Benefits Section */}
        <div className="bg-white/90 dark:bg-gray-800 rounded-xl shadow-lg border border-tiktok-secondary/20 p-6 md:p-8 mb-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
            Benefits of Using TikSave
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">No Watermark</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Download clean videos without the TikTok logo or username watermark
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">High Quality</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Maintain the original video quality with our HD download options
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">Fast Processing</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Our servers quickly process your download requests with minimal waiting time
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">No Registration</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Use our service instantly without creating an account or providing personal info
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">Completely Free</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Our service is free to use with no hidden fees or premium features
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-tiktok-primary flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-1">Works with All Videos</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Compatible with all public TikTok videos regardless of length or content type
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* FAQ Section */}
        <div className="bg-white/90 dark:bg-gray-800 rounded-xl shadow-lg border border-tiktok-secondary/20 p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <HelpCircle className="w-5 h-5 mr-2 text-tiktok-primary dark:text-tiktok-secondary" />
            Frequently Asked Questions
          </h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                Is this service legal?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Our service allows you to download videos for personal use only. It&apos;s important to respect copyright laws and the intellectual property of content creators. Don&apos;t use downloaded videos for commercial purposes without proper permission.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                Why can&apos;t I download some videos?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Some videos may be private or restricted by the creator. Our service only works with public TikTok videos. If you&apos;re having trouble downloading a specific video, make sure it&apos;s publicly accessible.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                How do you make money if the service is free?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                We sustain our service through non-intrusive advertisements displayed on our website. This allows us to keep the service completely free for all users while covering our server and development costs.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                Is there a limit to how many videos I can download?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Currently, there are no strict limits on how many videos you can download. However, we may implement fair usage policies in the future to ensure the service remains available for everyone.
              </p>
            </div>
          </div>
        </div>
        
        {/* Ad Banner */}
        <AdBanner location="bottom" className="mt-8" />
      </div>
    </div>
  );
};

export default AboutPage; 