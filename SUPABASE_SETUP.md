# 🚀 Supabase Database Setup Instructions

## Quick Fix for Console Errors

The console errors you're seeing are because the database tables don't exist yet in your Supabase project.

## Steps to Fix:

### 1. Go to Your Supabase Project
- Visit: https://supabase.com/dashboard/projects
- Click on your project: `vbbwydfwcegxxhiwdadu`

### 2. Open SQL Editor
- In the left sidebar, click **"SQL Editor"**
- Click **"New Query"**

### 3. Run the Database Schema
- Copy the entire contents of `supabase_schema.sql` (in your project root)
- Paste it into the SQL Editor
- Click **"Run"** (or press Ctrl/Cmd + Enter)

### 4. Verify Setup
- After running the script, you should see:
  - ✅ Tables created successfully
  - ✅ Sample data inserted
  - ✅ Indexes and triggers created

### 5. Test Your Dashboard
- Refresh your dashboard at `http://localhost:3000/dashboard`
- You should see:
  - ✅ No more console errors
  - ✅ Real data from Supabase
  - ✅ "Connect Social Accounts" button working

## What the Schema Creates:

### Tables:
- **`social_accounts`** - Your connected Instagram/TikTok accounts
- **`content_items`** - All collected video URLs with status tracking
- **`download_queue`** - Queue for processing downloads
- **`scheduled_posts`** - Automated posting schedule

### Sample Data:
- 2 sample social accounts (Instagram & TikTok)
- 3 sample content items in different stages
- 2 sample download queue entries

## Troubleshooting:

### If you get permission errors:
1. Make sure you're logged into the correct Supabase account
2. Verify you're in the right project (`vbbwydfwcegxxhiwdadu`)

### If the script fails:
1. Try running it in smaller chunks
2. Check the error message in the SQL Editor
3. Make sure you have the `uuid-ossp` extension enabled

### Still having issues?
- Check the browser console for any new error messages
- Verify your environment variables are correct
- Make sure your Supabase project is active and not paused

## Next Steps After Setup:
Once the database is working, you can:
1. ✅ Connect real social media accounts
2. ✅ Integrate with Instagram/TikTok APIs
3. ✅ Connect to your existing video downloader
4. ✅ Set up automated posting
5. ✅ Implement storage cleanup

Your content pipeline will be: **Liked Posts → Database → Download → Repost → Delete** 🎉
