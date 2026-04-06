# API Keys - Where to Find Them (Quick Lookup)

## 🔑 The 3 Keys You Need

### 1. GEMINI_API_KEY
**Where to get it:** https://aistudio.google.com/app/apikey

**Step-by-step:**
1. Visit: https://aistudio.google.com/app/apikey
2. Click: "Create API Key"
3. Select or create a Google Cloud project
4. Copy the API key
5. Add to .env:
   ```
   GEMINI_API_KEY=AIzaSy_your_actual_key_here
   ```

**Format:**
```
✓ Starts with: AIzaSy_
✓ Very long string (~100+ characters)
✓ Copy entire thing
```

---

### 2. SUPABASE_URL
**Where to get it:** https://app.supabase.com → Settings → API

**Step-by-step:**
1. Go to: https://app.supabase.com
2. Create/Open a project
3. Click: "Settings" (left sidebar, bottom)
4. Click: "API"
5. Find: "Project URL" 
6. Copy the URL (looks like: https://xxx.supabase.co)
7. Add to .env:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   ```

**Format:**
```
✓ Starts with: https://
✓ Ends with: .supabase.co
✓ Example: https://your-project-id.supabase.co
```

---

### 3. SUPABASE_KEY
**Where to get it:** https://app.supabase.com → Settings → API

**Step-by-step:**
1. Same page as SUPABASE_URL (Settings → API)
2. Find: "API Keys" section
3. Look for: "anon public" (or just "Project API keys")
4. Copy the long key (starts with `eyJ...`)
5. Add to .env:
   ```
   SUPABASE_KEY=eyJhbGc...very...long...string
   ```

**Format:**
```
✓ Starts with: eyJ
✓ Very long (~200+ characters)
✓ This is the "anon public" key
✓ Safe to use (Row Level Security enabled)
```

---

## 📝 Your .env File (After Getting Keys)

```env
ENVIRONMENT=development
SECRET_KEY=dev-key
DEBUG=True

# From Google Gemini
GEMINI_API_KEY=AIzaSy_your-actual-key-here

# From Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ-your-actual-key-here
```

---

## 🔐 GitHub Safety (Already Configured!)

**What's in .env.example (SAFE - push to GitHub):**
```env
GEMINI_API_KEY=your-google-gemini-api-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key-here
```
✅ NO real keys (just placeholders)

**What's in .env (PRIVATE - don't push):**
```env
GEMINI_API_KEY=AIzaSy_abc123xyz789
SUPABASE_URL=https://my-actual-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
❌ Real keys (in .gitignore - won't be pushed)

---

## ✅ Verification

Before pushing to GitHub:

```bash
# 1. Check that .env is ignored
git status
# Should NOT show .env in the list

# 2. Check that .env.example will be pushed
git status
# Should show: .env.example (if modified)

# 3. View what would be pushed
git diff --cached --name-only
# Should include .env.example, NOT .env
```

---

## 💰 Costs

| Service | Cost | Notes |
|---------|------|-------|
| Google Gemini | FREE | 60 requests per minute |
| Supabase | FREE | 500MB included |

---

## 🚀 Next Steps

1. **Get Gemini Key** (5 min): https://aistudio.google.com/app/apikey
2. **Get Supabase Keys** (5 min): https://app.supabase.com
3. **Create .env file**: `cp .env.example .env`
4. **Add your keys to .env**
5. **Run app**: `python app.py`
6. **Test**: `http://localhost:5000/health`
7. **Push**: `git push` (safely!)

---

## 📚 Full Guides

- **API_KEYS_SETUP.md** - Detailed setup with screenshots
- **KEYS_CHECKLIST.md** - Quick checklist
- **ENV_GUIDE.md** - Environment variables visual guide

---

**All your keys are safe!** ✅
Your .env.example has placeholders only, and .env is ignored by .gitignore
