# Project Alfred - Deployment Guide

This guide provides step-by-step instructions for deploying Project Alfred to production using zero-budget infrastructure.

---

## Prerequisites

You will need free accounts on the following platforms:

1. **Vercel** (for frontend hosting) - https://vercel.com
2. **Railway** (for backend hosting) - https://railway.app
3. **Supabase** (for database) - https://supabase.com

---

## Step 1: Set Up Supabase Database

1. Go to https://supabase.com and create a free account.
2. Create a new project (choose a region close to your users).
3. Once the project is ready, go to **Settings > API**.
4. Copy the following values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

5. Go to **SQL Editor** and run the following schema:

```sql
-- Users table
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE,
  name TEXT,
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Conversations table
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  user_id TEXT REFERENCES users(id),
  title TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT REFERENCES conversations(id),
  role TEXT,
  content TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Step 2: Deploy Backend to Railway

### Option A: Using Railway CLI (Recommended)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Navigate to the backend directory:
   ```bash
   cd /home/ubuntu/project-alfred/backend
   ```

4. Initialize Railway project:
   ```bash
   railway init
   ```

5. Add environment variables:
   ```bash
   railway variables set OPENAI_API_KEY=your_key_here
   railway variables set SUPABASE_URL=your_supabase_url
   railway variables set SUPABASE_KEY=your_supabase_key
   ```

6. Deploy:
   ```bash
   railway up
   ```

7. Get your backend URL:
   ```bash
   railway domain
   ```

### Option B: Using Railway Web Interface

1. Go to https://railway.app and login.
2. Click **New Project** > **Deploy from GitHub repo** (or upload the backend folder).
3. Select the `backend` directory.
4. Add environment variables in the **Variables** tab.
5. Railway will automatically detect the Python app and deploy it.
6. Copy the generated domain (e.g., `https://your-app.railway.app`).

---

## Step 3: Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to the frontend directory:
   ```bash
   cd /home/ubuntu/project-alfred/frontend
   ```

3. Update `.env.production` with your Railway backend URL:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

4. Deploy:
   ```bash
   vercel --prod
   ```

5. Follow the prompts and copy the generated URL.

### Option B: Using Vercel Web Interface

1. Go to https://vercel.com and login.
2. Click **Add New** > **Project**.
3. Import the `frontend` directory (or connect your GitHub repo).
4. Add environment variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-backend-url.railway.app`
5. Click **Deploy**.
6. Copy the generated domain (e.g., `https://project-alfred.vercel.app`).

---

## Step 4: Update CORS Settings

1. Go back to your Railway backend.
2. Update the `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

3. Redeploy the backend if necessary.

---

## Step 5: Test the Deployment

1. Visit your Vercel frontend URL.
2. Try creating a conversation and sending a message.
3. Verify that the backend is responding correctly.
4. Check that data is being saved to Supabase.

---

## Congratulations!

Project Alfred is now live and publicly accessible. Share your URL with users and start gathering feedback!

---

## Custom Domain (Optional)

If you want to use a custom domain:

1. **For Frontend (Vercel):**
   - Go to your project settings in Vercel.
   - Click **Domains** and add your custom domain.
   - Update your DNS records as instructed.

2. **For Backend (Railway):**
   - Go to your project settings in Railway.
   - Click **Settings** > **Domains** and add your custom domain.
   - Update your DNS records as instructed.

---

## Monitoring & Maintenance

- **Vercel Dashboard:** Monitor frontend performance and analytics.
- **Railway Dashboard:** Monitor backend logs and resource usage.
- **Supabase Dashboard:** Monitor database usage and queries.

All three platforms provide free monitoring and alerting for their free tiers.
