# API Keys Setup Guide

## Overview

This project requires 2 sets of API keys. This guide shows you exactly where to find them.

---

## 1️⃣ OpenAI API Key

### What is it?
Authentication key to use OpenAI's GPT-4o-mini model for extracting job data.

### How to Get It

#### Step 1: Create OpenAI Account
1. Go to: https://platform.openai.com/signup
2. Sign up with email or Google/Microsoft account
3. Verify your email

#### Step 2: Add Payment Method
1. Go to: https://platform.openai.com/account/billing/overview
2. Click "Billing" → "Overview"
3. Add a credit card
   - OpenAI charges per API usage
   - GPT-4o-mini is very affordable (~$0.0001-0.0002 per extraction)
4. Set usage limits (optional but recommended)
   - Go to "Billing" → "Usage limits"
   - Set maximum monthly spend

#### Step 3: Create API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "Job Pipeline" (optional)
4. Click "Create secret key"
5. **Copy the key immediately** (you can't see it again!)
   - Format: `sk-proj-xxxxxxxxxxxxxx...`

#### Step 4: Copy to .env
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxx
```

### 💰 Cost Estimation
- Typical JD extraction: ~$0.00015
- 1000 extractions: ~$0.15
- Very affordable for testing

### 🔐 Keep It Safe
- ✅ Store in `.env` file
- ✅ Add `.env` to `.gitignore` (already done)
- ❌ Never commit to GitHub
- ❌ Never share publicly

---

## 2️⃣ Supabase API Keys (2 values needed)

### What is it?
Database credentials to store extracted job data in Supabase (PostgreSQL).

### How to Get It

#### Step 1: Create Supabase Account
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub or email
4. Verify email

#### Step 2: Create New Project
1. Click "New project"
2. Enter project name: "job-pipeline" (or your choice)
3. Create a password (database password - keep safe!)
4. Select region closest to you
5. Click "Create new project"
6. Wait 2-3 minutes for project setup

#### Step 3: Get API Keys & URL
Once project is created:

1. **Find in Sidebar**:
   - Click "Settings" (bottom left) → "API"

2. **You need to copy 2 values**:

   **Value #1: SUPABASE_URL**
   - Look for "Project URL" or "API URL"
   - Format: `https://your-project-id.supabase.co`
   - Copy the full URL

   **Value #2: SUPABASE_KEY**
   - Look for "anon public" or "API Keys" section
   - There will be several keys, use the "anon public" key
   - Format: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (very long)
   - Copy the full key

#### Step 4: Create Database Table
1. In Supabase, go to "SQL Editor" (left sidebar)
2. Click "New query"
3. Copy and paste all content from [supabase_setup.sql](supabase_setup.sql)
4. Click "Run" (green play button)
5. Verify success message appears

#### Step 5: Copy to .env
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 🔐 Security Notes
- The "anon public" key is safe for frontend (by design)
- Database has Row Level Security enabled
- Still keep `.env` private
- Add to `.gitignore` ✅

---

## Complete .env File Example

```env
# ============================================
# Flask Configuration
# ============================================
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True

# ============================================
# Required: OpenAI API Key
# Get from: https://platform.openai.com/api-keys
# ============================================
OPENAI_API_KEY=sk-proj-your-openai-key-here

# ============================================
# Required: Supabase Configuration
# Get from: https://app.supabase.com → Settings → API
# ============================================
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## For GitHub (Safe to Push)

### .env.example (Already Created - Safe!)

This file contains NO actual keys, just placeholders:

```env
# Environment Configuration

# Flask Configuration
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key-here
```

### GitHub Setup (Safe & Recommended)

1. **Keep `.env` private** (.gitignore already configured)
   ```
   .env          ← NEVER commit
   .env.example  ← ALWAYS commit (no real keys!)
   .env.local    ← NEVER commit
   ```

2. **For team members**:
   - They copy `cp .env.example .env`
   - They add their own API keys
   - They never commit `.env`

3. **Verify Before Pushing**:
   ```bash
   git status
   # .env should NOT appear in staged files
   # .env.example should appear
   ```

---

## Step-by-Step Setup Checklist

### ✅ OpenAI Setup (5 min)
- [ ] Go to https://platform.openai.com/signup
- [ ] Create account
- [ ] Add payment method (Settings → Billing)
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Click "Create new secret key"
- [ ] Copy key to `.env` as `OPENAI_API_KEY`

### ✅ Supabase Setup (5 min)
- [ ] Go to https://supabase.com
- [ ] Sign up / Login
- [ ] Create new project
- [ ] Wait for setup to complete
- [ ] Go to Settings → API
- [ ] Copy Project URL → `.env` as `SUPABASE_URL`
- [ ] Copy anon public key → `.env` as `SUPABASE_KEY`
- [ ] Run SQL setup from supabase_setup.sql
- [ ] Verify table created

### ✅ Application Setup (2 min)
- [ ] Ensure `.env` has all 3 keys filled
- [ ] Verify `.env` is in `.gitignore`
- [ ] Run `python app.py`
- [ ] Check http://localhost:5000/health
- [ ] Should show: "ai_processor": "ready", "database": "connected"

---

## Quick Reference

| Service | Key Name | Format | Where to Find |
|---------|----------|--------|---------------|
| OpenAI | `OPENAI_API_KEY` | `sk-proj-...` | https://platform.openai.com/api-keys |
| Supabase | `SUPABASE_URL` | `https://xxx.supabase.co` | Settings → API → Project URL |
| Supabase | `SUPABASE_KEY` | `eyJ...` (long) | Settings → API → anon public |

---

## Troubleshooting

### ❌ "AI processor not available"
- Check `OPENAI_API_KEY` is correct
- Verify no spaces or typos
- Restart Flask app: `python app.py`

### ❌ "Table not found" or "Database disconnected"
- Verify `SUPABASE_URL` and `SUPABASE_KEY`
- Check that SQL setup ran successfully
- Go to Supabase → Table Editor
- Confirm `job_extractions` table exists

### ❌ "Invalid API Key"
- Regenerate the key (might have been copied wrong)
- OpenAI: https://platform.openai.com/api-keys → copy again
- Supabase: Settings → API → copy again

### ❌ "Unexpected characters in key"
- Keys should be one continuous string with NO spaces
- Check for trailing newlines in `.env`
- Example correct format:
  ```
  OPENAI_API_KEY=sk-proj-abc123xyz789
  ```
  NOT:
  ```
  OPENAI_API_KEY = sk-proj-abc123xyz789
  OPENAI_API_KEY=sk-proj-abc123xyz789    
  ```

---

## Cost Breakdown

### OpenAI Costs
- **GPT-4o-mini**: $0.15 per 1M input tokens, $0.60 per 1M output tokens
- **Typical JD**: ~500-1000 input tokens, ~100-150 output tokens
- **Per extraction**: ~$0.00015
- **Monthly estimate (1000 extractions)**: ~$0.15

### Supabase Free Tier (No Cost!)
- Storage: 500MB (plenty for extractions)
- Connections: Unlimited
- Great for development and testing

---

## Security Best Practices

### ✅ DO
- Store keys in `.env` file only
- Use `.env.example` for repository
- Add `.env` to `.gitignore`
- Rotate keys periodically
- Use different keys for dev/prod
- Set OpenAI usage limits

### ❌ DON'T
- Commit `.env` to GitHub
- Share keys in chat/Slack
- Hardcode keys in source files
- Log keys to console
- Use same key for multiple projects
- Post keys in issues/discussions

---

## Environment Variables Summary

```bash
# For Development
ENVIRONMENT=development
DEBUG=True

# For Production
ENVIRONMENT=production
DEBUG=False

# Required for All Environments
OPENAI_API_KEY=...     # From OpenAI
SUPABASE_URL=...       # From Supabase
SUPABASE_KEY=...       # From Supabase
```

---

## Next Steps

1. **Get OpenAI Key**: Follow steps above (5 min)
2. **Get Supabase Keys**: Follow steps above (5 min)
3. **Update .env file**: Add your real keys
4. **Test Connection**:
   ```bash
   curl http://localhost:5000/health
   ```
5. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit - add project files"
   # .env is ignored, .env.example is included
   git push origin main
   ```

---

## Support

- **OpenAI Help**: https://help.openai.com
- **Supabase Docs**: https://supabase.com/docs
- **Check .gitignore**: Run `git status` before pushing

**All Good? Run the app!** 🚀
