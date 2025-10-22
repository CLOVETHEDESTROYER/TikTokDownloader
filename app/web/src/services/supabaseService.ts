import { supabase, SocialAccount, ContentItem, DownloadQueue, ScheduledPost } from '@/lib/supabase'

export class SupabaseService {
  // Dashboard Stats
  async getDashboardStats() {
    try {
      // Get total accounts
      const { count: totalAccounts } = await supabase
        .from('social_accounts')
        .select('*', { count: 'exact', head: true })

      // Get active accounts
      const { count: activeAccounts } = await supabase
        .from('social_accounts')
        .select('*', { count: 'exact', head: true })
        .eq('is_active', true)

      // Get total content collected
      const { count: totalContent } = await supabase
        .from('content_items')
        .select('*', { count: 'exact', head: true })

      // Get content by status
      const { data: contentByStatus } = await supabase
        .from('content_items')
        .select('status')

      // Get downloads pending
      const { count: downloadsPending } = await supabase
        .from('download_queue')
        .select('*', { count: 'exact', head: true })
        .in('status', ['pending', 'downloading'])

      // Get scheduled posts
      const { count: scheduledPosts } = await supabase
        .from('scheduled_posts')
        .select('*', { count: 'exact', head: true })
        .eq('status', 'scheduled')

      // Get recent activity
      const { data: recentContent } = await supabase
        .from('content_items')
        .select('title, status, created_at, updated_at')
        .order('updated_at', { ascending: false })
        .limit(5)

      // Process content by status
      const statusCounts = {
        collected: 0,
        downloading: 0,
        ready_to_post: 0,
        posted_deleted: 0
      }

      contentByStatus?.forEach(item => {
        if (item.status === 'collected') statusCounts.collected++
        else if (item.status === 'downloading') statusCounts.downloading++
        else if (item.status === 'downloaded') statusCounts.ready_to_post++
        else if (item.status === 'posted' || item.status === 'deleted') statusCounts.posted_deleted++
      })

      // Format recent activity
      const recentActivity = recentContent?.map(item => ({
        action: item.status === 'downloaded' ? 'Downloaded' : 'Collected',
        item: item.title || 'Untitled',
        time: this.formatTimeAgo(new Date(item.updated_at || item.created_at))
      })) || []

      return {
        total_accounts: totalAccounts || 0,
        active_accounts: activeAccounts || 0,
        total_content_collected: totalContent || 0,
        content_by_status: statusCounts,
        downloads_pending: downloadsPending || 0,
        scheduled_posts: scheduledPosts || 0,
        recent_activity: recentActivity
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
      throw error
    }
  }

  // Content Items
  async getContentItems(status?: string, platform?: string, limit = 20, offset = 0) {
    try {
      let query = supabase
        .from('content_items')
        .select(`
          *,
          source_account:social_accounts(username, platform)
        `)
        .order('created_at', { ascending: false })
        .range(offset, offset + limit - 1)

      if (status) {
        query = query.eq('status', status)
      }
      if (platform) {
        query = query.eq('platform', platform)
      }

      const { data, error } = await query

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching content items:', error)
      throw error
    }
  }

  // Social Accounts
  async getSocialAccounts() {
    try {
      const { data, error } = await supabase
        .from('social_accounts')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching social accounts:', error)
      throw error
    }
  }

  async addSocialAccount(account: Omit<SocialAccount, 'id' | 'created_at'>) {
    try {
      const { data, error } = await supabase
        .from('social_accounts')
        .insert([account])
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error adding social account:', error)
      throw error
    }
  }

  // Content Collection
  async addContentItem(item: Omit<ContentItem, 'id' | 'created_at' | 'updated_at'>) {
    try {
      const { data, error } = await supabase
        .from('content_items')
        .insert([item])
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error adding content item:', error)
      throw error
    }
  }

  async updateContentItemStatus(id: string, status: string, downloadPath?: string) {
    try {
      const updateData: any = { status }
      if (downloadPath) {
        updateData.download_path = downloadPath
      }

      const { data, error } = await supabase
        .from('content_items')
        .update(updateData)
        .eq('id', id)
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error updating content item status:', error)
      throw error
    }
  }

  // Download Queue
  async getDownloadQueue() {
    try {
      const { data, error } = await supabase
        .from('download_queue')
        .select(`
          *,
          content_item:content_items(*)
        `)
        .order('priority', { ascending: false })
        .order('created_at', { ascending: true })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching download queue:', error)
      throw error
    }
  }

  async addToDownloadQueue(contentItemId: string, priority = 0) {
    try {
      const { data, error } = await supabase
        .from('download_queue')
        .insert([{
          content_item_id: contentItemId,
          priority,
          status: 'pending'
        }])
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error adding to download queue:', error)
      throw error
    }
  }

  // Scheduled Posts
  async getScheduledPosts() {
    try {
      const { data, error } = await supabase
        .from('scheduled_posts')
        .select(`
          *,
          content_item:content_items(*)
        `)
        .order('scheduled_time', { ascending: true })

      if (error) throw error
      return data || []
    } catch (error) {
      console.error('Error fetching scheduled posts:', error)
      throw error
    }
  }

  async schedulePost(post: Omit<ScheduledPost, 'id' | 'created_at' | 'posted_at'>) {
    try {
      const { data, error } = await supabase
        .from('scheduled_posts')
        .insert([post])
        .select()
        .single()

      if (error) throw error
      return data
    } catch (error) {
      console.error('Error scheduling post:', error)
      throw error
    }
  }

  // Utility function to format time ago
  private formatTimeAgo(date: Date): string {
    const now = new Date()
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

    if (diffInSeconds < 60) return `${diffInSeconds} sec ago`
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} min ago`
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hour ago`
    return `${Math.floor(diffInSeconds / 86400)} days ago`
  }
}

export const supabaseService = new SupabaseService()
