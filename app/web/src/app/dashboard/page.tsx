"use client";

import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { supabaseService } from "@/services/supabaseService";
import {
  Home,
  CheckCircle2,
  AlertCircle,
  ChevronRight,
  Search,
  Plus,
  Settings,
  Users,
  BarChart3,
  FileText,
  Shield,
  Bell,
  Edit,
  Video,
  Download,
  RefreshCw,
  Upload,
  Clock,
  Trash2,
  ExternalLink,
} from "lucide-react";

interface DashboardStats {
  total_accounts: number;
  active_accounts: number;
  total_content_collected: number;
  content_by_status: Record<string, number>;
  downloads_pending: number;
  scheduled_posts: number;
  recent_activity: Array<{
    type: string;
    platform: string;
    count: number;
    timestamp: string;
  }>;
}

interface TaskItem {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  required: boolean;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedApp, setSelectedApp] = useState("SocialMediaManager");
  const [contentItems, setContentItems] = useState<any[]>([]);
  const [accounts, setAccounts] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Helper function for API calls
  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    const apiKey = process.env.NEXT_PUBLIC_WEBSITE_API_KEY || "website_key_123";
    const baseUrl =
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

    return fetch(`${baseUrl}${endpoint}`, {
      ...options,
      headers: {
        "X-API-Key": apiKey,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  };

  useEffect(() => {
    fetchDashboardData();
    fetchContentItems();
    fetchAccounts();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Try to fetch real data from Supabase
      const statsData = await supabaseService.getDashboardStats();
      setStats(statsData);
      console.log("✅ Successfully loaded data from Supabase!");
    } catch (error: any) {
      console.error("Error fetching dashboard data:", error);

      // Check if it's a table not found error
      if (error?.code === "PGRST205") {
        setError(
          "⚠️ Database tables not found. Please run the SQL schema in your Supabase project first!"
        );
      } else {
        setError("Failed to load dashboard data. Please try again later.");
      }

      // Fallback to mock data
      const mockStats = {
        total_accounts: 2,
        active_accounts: 1,
        total_content_collected: 12,
        content_by_status: {
          collected: 12,
          downloading: 3,
          ready_to_post: 8,
          posted_deleted: 15,
        },
        downloads_pending: 3,
        scheduled_posts: 2,
        recent_activity: [
          {
            action: "Downloaded",
            item: "Amazing Dance Reel",
            time: "2 min ago",
          },
          { action: "Posted", item: "Cooking Tutorial", time: "1 hour ago" },
        ],
      };
      setStats(mockStats);
    } finally {
      setLoading(false);
    }
  };

  const fetchContentItems = async () => {
    try {
      const items = await supabaseService.getContentItems();
      setContentItems(items);
      console.log("✅ Successfully loaded content items from Supabase!");
    } catch (error: any) {
      console.error("Error fetching content items:", error);
      if (error?.code !== "PGRST205") {
        // Only log non-table-missing errors since we already handle that in fetchDashboardData
        console.warn("Content items will be empty until database is set up");
      }
      setContentItems([]);
    }
  };

  const fetchAccounts = async () => {
    try {
      const accountsData = await supabaseService.getSocialAccounts();
      setAccounts(accountsData);
      console.log("✅ Successfully loaded accounts from Supabase!");
    } catch (error: any) {
      console.error("Error fetching accounts:", error);
      if (error?.code !== "PGRST205") {
        // Only log non-table-missing errors since we already handle that in fetchDashboardData
        console.warn("Accounts will be empty until database is set up");
      }
      setAccounts([]);
    }
  };

  const connectInstagram = async () => {
    try {
      // For demo purposes, let's add a sample Instagram account
      const sampleAccount = {
        platform: "instagram" as const,
        account_id: "demo_instagram_" + Date.now(),
        username: "your_instagram_handle",
        access_token: "demo_token_" + Date.now(),
        is_active: true,
      };

      const newAccount = await supabaseService.addSocialAccount(sampleAccount);

      // Add some sample content items for this account
      const sampleContent = [
        {
          source_account_id: newAccount.id,
          original_url: "https://www.instagram.com/p/DEMO1234567/",
          platform: "instagram" as const,
          content_type: "reel" as const,
          title: "Amazing Dance Reel",
          author: "@user123",
          status: "collected" as const,
        },
        {
          source_account_id: newAccount.id,
          original_url: "https://www.instagram.com/p/DEMO7890123/",
          platform: "instagram" as const,
          content_type: "post" as const,
          title: "Beautiful Sunset",
          author: "@photographer",
          status: "downloaded" as const,
        },
      ];

      for (const content of sampleContent) {
        await supabaseService.addContentItem(content);
      }

      alert(
        "✅ Instagram account connected successfully! Check your dashboard for new content."
      );

      // Refresh the data
      fetchDashboardData();
      fetchContentItems();
      fetchAccounts();
    } catch (error) {
      console.error("Error connecting Instagram:", error);
      alert("Failed to connect Instagram. Please try again later.");
    }
  };

  const sidebarItems = [
    { icon: Home, label: "Dashboard", id: "dashboard", active: true },
    { icon: Shield, label: "Required actions", id: "required", active: false },
    { icon: FileText, label: "Use cases", id: "use-cases", active: false },
    { icon: CheckCircle2, label: "Review", id: "review", active: false },
    { icon: BarChart3, label: "Publish", id: "publish", active: false },
    { icon: Settings, label: "App settings", id: "settings", active: false },
    { icon: Users, label: "App roles", id: "roles", active: false },
    { icon: Bell, label: "Alert Inbox", id: "alerts", active: false },
  ];

  const taskItems: TaskItem[] = [
    {
      id: "1",
      title:
        "Customize the Authenticate and request data from users with Facebook Login use case",
      description: "Set up Facebook Login integration for user authentication",
      completed: false,
      required: true,
    },
    {
      id: "2",
      title: "Review and complete testing requirements",
      description: "Complete all testing requirements for app review",
      completed: false,
      required: true,
    },
    {
      id: "3",
      title: "Business verification",
      description: "Verify your business to access advanced features",
      completed: false,
      required: true,
    },
    {
      id: "4",
      title: "App Review",
      description: "Submit your app for review by Meta",
      completed: false,
      required: true,
    },
    {
      id: "5",
      title: "Check that all requirements are met, then publish your app",
      description: "Final step to make your app live",
      completed: false,
      required: true,
    },
  ];

  const toggleTask = (taskId: string) => {
    // This would update the task status in your backend
    console.log("Toggle task:", taskId);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-tiktok-light via-white to-tiktok-secondary/20">
      {/* Sidebar */}
      <div className="w-64 bg-white/80 backdrop-blur-lg border-r border-gray-200 shadow-lg flex flex-col">
        {/* App Selector */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-tiktok rounded-xl flex items-center justify-center shadow-md">
              <span className="text-white text-sm font-bold">SM</span>
            </div>
            <select
              value={selectedApp}
              onChange={(e) => setSelectedApp(e.target.value)}
              className="flex-1 bg-transparent border-none text-sm font-semibold text-gray-800 focus:outline-none"
            >
              <option value="SocialMediaManager">SocialMediaManager</option>
            </select>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {sidebarItems.map((item) => (
              <li key={item.id}>
                <button
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left text-sm font-medium transition-all duration-200 ${
                    item.active
                      ? "bg-gradient-tiktok text-white shadow-lg"
                      : "text-gray-700 hover:bg-tiktok-light hover:text-tiktok-accent"
                  }`}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white/90 backdrop-blur-lg border-b border-gray-200 px-8 py-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-tiktok-primary to-tiktok-accent bg-clip-text text-transparent">
                Dashboard
              </h1>
            </div>

            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                className="bg-white/80 hover:bg-tiktok-light border-gray-300"
              >
                <Edit className="h-4 w-4 mr-2" />
                Add use cases
              </Button>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search"
                  className="pl-10 pr-4 py-3 bg-white/80 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-tiktok-primary focus:border-transparent w-64 shadow-sm"
                />
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto p-8 bg-gradient-to-br from-tiktok-light/30 via-white/50 to-tiktok-secondary/10">
          <div className="max-w-4xl mx-auto">
            {/* Error Display */}
            {error && (
              <Card className="mb-6 bg-red-50 border-red-200 shadow-lg">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <AlertCircle className="h-5 w-5 text-red-600" />
                    <p className="text-red-800 font-medium">{error}</p>
                  </div>
                  {error.includes("Database tables not found") && (
                    <div className="mt-3 p-3 bg-red-100 rounded-lg">
                      <p className="text-sm text-red-700">
                        <strong>Quick Fix:</strong> Go to your Supabase project
                        → SQL Editor → Run the schema from{" "}
                        <code>supabase_schema.sql</code>
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
            {/* Content Pipeline Status */}
            <Card className="mb-8 bg-white/80 backdrop-blur-lg border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="pb-4">
                <CardTitle className="text-xl font-bold text-gray-800 flex items-center space-x-2">
                  <Video className="h-6 w-6 text-tiktok-primary" />
                  <span>Content Pipeline Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-blue-50 p-4 rounded-xl border border-blue-200">
                    <div className="text-2xl font-bold text-blue-600">12</div>
                    <div className="text-sm text-blue-700">Collected URLs</div>
                  </div>
                  <div className="bg-yellow-50 p-4 rounded-xl border border-yellow-200">
                    <div className="text-2xl font-bold text-yellow-600">3</div>
                    <div className="text-sm text-yellow-700">Downloading</div>
                  </div>
                  <div className="bg-green-50 p-4 rounded-xl border border-green-200">
                    <div className="text-2xl font-bold text-green-600">8</div>
                    <div className="text-sm text-green-700">Ready to Post</div>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-xl border border-purple-200">
                    <div className="text-2xl font-bold text-purple-600">15</div>
                    <div className="text-sm text-purple-700">
                      Posted & Deleted
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card className="mb-8 bg-white/80 backdrop-blur-lg border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="pb-4">
                <CardTitle className="text-xl font-bold text-gray-800 flex items-center space-x-2">
                  <Download className="h-6 w-6 text-tiktok-primary" />
                  <span>Content Pipeline Actions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <Button
                    onClick={connectInstagram}
                    className="h-14 justify-start bg-gradient-tiktok hover:bg-gradient-purple text-white shadow-md hover:shadow-lg transition-all duration-200"
                  >
                    <Plus className="h-5 w-5 mr-3" />
                    Connect Social Accounts
                  </Button>
                  <Button
                    className="h-14 justify-start bg-white hover:bg-tiktok-light border-gray-300 text-gray-700 hover:text-tiktok-accent shadow-md hover:shadow-lg transition-all duration-200"
                    variant="outline"
                  >
                    <RefreshCw className="h-5 w-5 mr-3" />
                    Sync Liked Posts
                  </Button>
                  <Button
                    className="h-14 justify-start bg-white hover:bg-tiktok-light border-gray-300 text-gray-700 hover:text-tiktok-accent shadow-md hover:shadow-lg transition-all duration-200"
                    variant="outline"
                  >
                    <Download className="h-5 w-5 mr-3" />
                    Start Downloads
                  </Button>
                  <Button
                    className="h-14 justify-start bg-white hover:bg-tiktok-light border-gray-300 text-gray-700 hover:text-tiktok-accent shadow-md hover:shadow-lg transition-all duration-200"
                    variant="outline"
                  >
                    <Upload className="h-5 w-5 mr-3" />
                    Schedule Posts
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Content Queue */}
            <Card className="mb-8 bg-white/80 backdrop-blur-lg border-gray-200 shadow-lg">
              <CardHeader className="pb-4">
                <CardTitle className="text-xl font-bold text-gray-800 flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Clock className="h-6 w-6 text-tiktok-primary" />
                    <span>Content Queue</span>
                  </div>
                  <Button variant="outline" size="sm" className="bg-white/80">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {/* Sample content items */}
                  <div className="flex items-center justify-between p-4 bg-blue-50 border border-blue-200 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                        <Video className="h-8 w-8 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-800">
                          Amazing Dance Reel
                        </h4>
                        <p className="text-sm text-gray-600">
                          @user123 • Instagram
                        </p>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                            Collected
                          </span>
                          <span className="text-xs text-gray-500">
                            2 min ago
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm">
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-16 bg-yellow-100 rounded-lg flex items-center justify-center">
                        <Video className="h-8 w-8 text-yellow-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-800">
                          Cooking Tutorial
                        </h4>
                        <p className="text-sm text-gray-600">
                          @chef_mike • TikTok
                        </p>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full">
                            Downloading
                          </span>
                          <span className="text-xs text-gray-500">
                            5 min ago
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-yellow-500 h-2 rounded-full"
                          style={{ width: "65%" }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600">65%</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center">
                        <Video className="h-8 w-8 text-green-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-800">
                          Travel Vlog
                        </h4>
                        <p className="text-sm text-gray-600">
                          @wanderer_x • Instagram
                        </p>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                            Ready to Post
                          </span>
                          <span className="text-xs text-gray-500">
                            1 hour ago
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="bg-green-100 text-green-700 hover:bg-green-200"
                      >
                        <Upload className="h-4 w-4 mr-1" />
                        Post Now
                      </Button>
                      <Button variant="outline" size="sm">
                        <Clock className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stats Overview */}
            {stats && (
              <Card className="mt-6 bg-white/80 backdrop-blur-lg border-gray-200 shadow-lg">
                <CardHeader>
                  <CardTitle className="text-lg font-medium text-foreground">
                    Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-4 gap-4">
                    <div className="text-center p-4 bg-muted/50 rounded-lg">
                      <div className="text-2xl font-bold text-foreground">
                        {stats.total_accounts}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Total Accounts
                      </div>
                    </div>
                    <div className="text-center p-4 bg-muted/50 rounded-lg">
                      <div className="text-2xl font-bold text-foreground">
                        {stats.active_accounts}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Active Accounts
                      </div>
                    </div>
                    <div className="text-center p-4 bg-muted/50 rounded-lg">
                      <div className="text-2xl font-bold text-foreground">
                        {stats.total_content_collected}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Content Items
                      </div>
                    </div>
                    <div className="text-center p-4 bg-muted/50 rounded-lg">
                      <div className="text-2xl font-bold text-foreground">
                        {stats.scheduled_posts}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Scheduled Posts
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
