'use client';

import React from 'react';
import { Shield, AlertTriangle } from 'lucide-react';
import AdBanner from '@/components/AdBanner';

const PrivacyPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-6 text-center bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
          Privacy Policy & Terms
        </h1>
        
        <p className="text-lg text-gray-700 dark:text-gray-300 mb-10 text-center">
          Your privacy matters to us. Learn about how we handle your data.
        </p>
        
        {/* Privacy Policy */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8 mb-8">
          <div className="flex items-center mb-6">
            <Shield className="w-6 h-6 text-teal-600 dark:text-teal-400 mr-3" />
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Privacy Policy
            </h2>
          </div>
          
          <div className="space-y-6 text-gray-700 dark:text-gray-300 text-sm">
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Information Collection
              </h3>
              <p>
                When you use our TikTok video downloader service, we collect minimal information needed to provide our service. This includes:
              </p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>TikTok video URLs that you submit for processing</li>
                <li>Basic device information including browser type and operating system</li>
                <li>IP address and approximate location (country/region)</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                How We Use Information
              </h3>
              <p>
                We use the information we collect for the following purposes:
              </p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>To provide and maintain our service</li>
                <li>To detect, prevent, and address technical issues</li>
                <li>To improve our website and user experience</li>
                <li>To monitor usage patterns and analyze trends</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Cookies and Tracking
              </h3>
              <p>
                We use cookies and similar tracking technologies to track activity on our website and store certain information. Cookies are files with a small amount of data which may include an anonymous unique identifier. These are sent to your browser from a website and stored on your device.
              </p>
              <p className="mt-2">
                You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some portions of our service.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Third-Party Services
              </h3>
              <p>
                Our service contains advertising from third-party ad networks. These networks may use cookies and similar technologies to collect information about your browsing activities over time and across different websites. We do not control these third parties&apos; tracking technologies or how they may be used.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Data Storage
              </h3>
              <p>
                We do not permanently store the videos you download using our service. Once the download is complete, the video is removed from our servers. However, we may temporarily store videos during the processing period to optimize our service.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Policy Updates
              </h3>
              <p>
                We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. You are advised to review this Privacy Policy periodically for any changes.
              </p>
            </div>
          </div>
        </div>
        
        {/* Terms of Service */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8 mb-8">
          <div className="flex items-center mb-6">
            <AlertTriangle className="w-6 h-6 text-purple-600 dark:text-purple-400 mr-3" />
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              Terms of Service
            </h2>
          </div>
          
          <div className="space-y-6 text-gray-700 dark:text-gray-300 text-sm">
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Acceptance of Terms
              </h3>
              <p>
                By accessing or using our service, you agree to be bound by these Terms of Service. If you disagree with any part of the terms, you may not access the service.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Service Description
              </h3>
              <p>
                TikSave provides a web-based service that enables users to download TikTok videos without watermarks. The service is provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo; without any warranties of any kind.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Intellectual Property Rights
              </h3>
              <p>
                Our service allows you to download videos for personal use only. We do not claim ownership of the content you download. All videos belong to their respective creators and are subject to TikTok&apos;s Terms of Service.
              </p>
              <p className="mt-2">
                You are responsible for ensuring that your use of downloaded videos complies with applicable laws and does not infringe on any third-party rights. We strongly discourage using downloaded content for commercial purposes without proper authorization.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Limitations of Use
              </h3>
              <p>
                You agree not to:
              </p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Use our service for any illegal purpose or in violation of any local, state, national, or international law</li>
                <li>Interfere with or disrupt the service or servers or networks connected to the service</li>
                <li>Use automated scripts, bots, or other software to access our service</li>
                <li>Attempt to bypass any measures we may use to prevent or restrict access to the service</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Disclaimer
              </h3>
              <p>
                We are not affiliated with, endorsed by, or sponsored by TikTok or ByteDance Ltd. All TikTok logos, trademarks, and service marks are the property of ByteDance Ltd.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Limitation of Liability
              </h3>
              <p>
                In no event shall TikSave, its directors, employees, partners, agents, suppliers, or affiliates be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the service.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white text-base mb-2">
                Changes to Terms
              </h3>
              <p>
                We reserve the right to modify or replace these Terms at any time at our sole discretion. By continuing to access or use our service after those revisions become effective, you agree to be bound by the revised terms.
              </p>
            </div>
          </div>
        </div>
        
        {/* DMCA Section */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
            DMCA / Copyright Policy
          </h2>
          
          <div className="text-gray-700 dark:text-gray-300 text-sm space-y-4">
            <p>
              TikSave respects the intellectual property rights of others and expects users of the service to do the same. We will respond to notices of alleged copyright infringement that comply with applicable law and are properly provided to us.
            </p>
            
            <p>
              If you believe that your copyrighted work has been copied in a way that constitutes copyright infringement, please provide us with the following information:
            </p>
            
            <ul className="list-disc pl-5 space-y-2">
              <li>A physical or electronic signature of the copyright owner or a person authorized to act on their behalf</li>
              <li>Identification of the copyrighted work claimed to have been infringed</li>
              <li>Identification of the material that is claimed to be infringing or to be the subject of infringing activity</li>
              <li>Your contact information, including your address, telephone number, and an email address</li>
              <li>A statement by you that you have a good faith belief that use of the material in the manner complained of is not authorized by the copyright owner, its agent, or the law</li>
              <li>A statement that the information in the notification is accurate, and, under penalty of perjury, that you are authorized to act on behalf of the copyright owner</li>
            </ul>
            
            <p className="mt-4">
              Contact us at: <span className="text-teal-600 dark:text-teal-400">dmca@tiksave.com</span>
            </p>
          </div>
        </div>
        
        {/* Ad Banner */}
        <AdBanner location="bottom" className="mt-8" />
      </div>
    </div>
  );
};

export default PrivacyPage; 