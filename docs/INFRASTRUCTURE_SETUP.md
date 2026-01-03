# Project Alfred: Infrastructure Setup Guide

**Sprint 1 Deliverable**
**Date:** Jan 03, 2026

---

## Overview

This document provides complete instructions for deploying Project Alfred using our zero-budget infrastructure stack. The entire setup uses free tiers and requires no upfront costs.

---

## Tech Stack Summary

| Component | Technology | Hosting | Cost |
|-----------|-----------|---------|------|
| Frontend | Vite + React + TypeScript + TailwindCSS | Vercel | Free |
| Backend | FastAPI + Python 3.11 | Railway/Render | Free tier |
| Database | PostgreSQL | Supabase | Free (500MB) |
| Authentication | Supabase Auth | Supabase | Free |
| File Storage | Supabase Storage | Supabase | Free (1GB) |
| CI/CD | GitHub Actions | GitHub | Free (2000 min/month) |

---

## Step 1: Set Up Supabase (Database & Auth)

Supabase provides our PostgreSQL database, authentication, and file storage, all on their generous free tier.

**Instructions:**

1. Go to [https://supabase.com](https://supabase.com) and sign up for a free account.
2. Click "New Project" and fill in the details:
   - **Name:** project-alfred
   - **Database Password:** (Generate a strong password and save it securely)
   - **Region:** Choose the closest region to your location
3. Wait for the project to be provisioned (takes ~2 minutes).
4. Once ready, go to **Settings → API** and copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)
5. Save these credentials - you'll need them for the backend configuration.

---

## Step 2: Deploy Backend to Railway

Railway provides free backend hosting with $5 credit per month, which is more than enough for our MVP.

**Instructions:**

1. Go to [https://railway.app](https://railway.app) and sign up with GitHub.
2. Click "New Project" → "Deploy from GitHub repo".
3. Connect your GitHub account and select the `project-alfred` repository.
4. Railway will auto-detect the backend folder. If not, set:
   - **Root Directory:** `/backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Railway dashboard:
   ```
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-anon-key>
   ```
6. Railway will automatically deploy. Copy the public URL (e.g., `https://project-alfred-production.up.railway.app`).

**Alternative: Render.com**

If you prefer Render:
1. Go to [https://render.com](https://render.com) and sign up.
2. Click "New +" → "Web Service".
3. Connect your GitHub repo and select `project-alfred`.
4. Configure:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add the same environment variables as above.

---

## Step 3: Deploy Frontend to Vercel

Vercel provides the best free hosting for React applications with automatic deployments.

**Instructions:**

1. Go to [https://vercel.com](https://vercel.com) and sign up with GitHub.
2. Click "Add New..." → "Project".
3. Import the `project-alfred` repository.
4. Vercel will auto-detect the Vite configuration. Confirm:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `pnpm run build`
   - **Output Directory:** `dist`
5. Add environment variable:
   ```
   VITE_API_URL=<your-railway-backend-url>
   ```
6. Click "Deploy". Vercel will build and deploy in ~2 minutes.
7. Your frontend will be live at `https://project-alfred.vercel.app`.

---

## Step 4: Configure GitHub Actions (CI/CD)

We'll set up automatic testing and deployment whenever code is pushed to the repository.

**Instructions:**

1. In your GitHub repository, go to **Settings → Secrets and variables → Actions**.
2. Add the following secrets:
   - `VERCEL_TOKEN` (Get from Vercel → Settings → Tokens)
   - `RAILWAY_TOKEN` (Get from Railway → Account Settings → Tokens)
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

A GitHub Actions workflow file will be created in Sprint 2 to automate deployments.

---

## Step 5: Test the Deployment

Once everything is deployed, test the infrastructure:

**Backend Health Check:**
```bash
curl https://your-railway-url.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "api": "operational",
    "database": "pending",
    "core_engine": "pending"
  }
}
```

**Frontend:**
Visit `https://project-alfred.vercel.app` in your browser. You should see the default Vite + React welcome page.

---

## Current Status

**✅ Completed in Sprint 1:**
- Project structure created
- Backend API scaffolded with FastAPI
- Frontend scaffolded with Vite + React + TypeScript
- TailwindCSS configured with Deep Forest theme
- Deployment configurations created for all platforms
- Zero-budget infrastructure documented

**⏳ Pending (Next Sprints):**
- Supabase database schema
- Core agent engine
- Frontend UI implementation
- WebSocket integration
- Authentication system

---

## Free Tier Limits

| Service | Limit | Notes |
|---------|-------|-------|
| Vercel | Unlimited bandwidth, 100GB/month | More than enough for MVP |
| Railway | $5 credit/month (~500 hours) | Covers 24/7 operation |
| Supabase | 500MB database, 1GB storage | Sufficient for thousands of users |
| GitHub Actions | 2000 minutes/month | ~33 hours of CI/CD |

All limits are well above what we need for the MVP phase.

---

## Next Steps

With Sprint 1 complete, we are ready to move to **Sprint 2: Core Engine - Cognitive Loop**, where we will build the foundational AI agent architecture.
