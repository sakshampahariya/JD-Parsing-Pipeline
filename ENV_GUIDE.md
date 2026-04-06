# Environment Variables - Visual Guide

## 📊 Files & Keys Overview

```
YOUR PROJECT (jd-pipeline/)
│
├── 📄 .env.example          ← SAFE to push to GitHub ✅
│   (Has placeholder values only - NO real secrets)
│
├── .env                     ← NEVER push to GitHub ❌
│   (Your actual secret keys - in .gitignore)
│
├── .gitignore               ← Already configured
│   (Prevents .env from being pushed)
│
└── (All other files)        ← Safe to push ✅

```

---

## Configuration Flow

```
1. Repository Created
   ↓
2. Developers Clone Repo
   ├─→ Get .env.example (no secrets)
   ├─→ Get code files
   └─→ Get .gitignore rules
   ↓
3. Each Developer
   ├─→ cp .env.example .env
   ├─→ Add their own API keys to .env
   ├─→ NEVER commit .env
   └─→ .gitignore prevents accidental push
   ↓
4. Push to GitHub
   └─→ .env.example goes up ✅
   └─→ .env stays local (ignored) ✅
   └─→ Everyone keeps their keys private ✅
```

---

## Your .env File Structure

### Location
```
jd-pipeline/
└── .env  ← Create this file (it's in .gitignore)
```

### Content (Keep Private!)
```env
# ========================================
# FLASK SETTINGS
# ========================================
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True

# ========================================
# YOUR ACTUAL API KEYS (Keep Private!)
# ========================================

# From: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-abc123xyz789...

# From: https://app.supabase.com → Settings → API
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Security Rules
```
✅ Stored locally only
✅ In .gitignore
✅ NOT in version control
✅ Each developer has their copy
```

---

## .env.example (On GitHub)

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

### Why this is safe:
- ❌ NO actual keys
- ✅ Only placeholders
- ✅ Shows structure
- ✅ Shows required variables
- ✅ Safe to commit

---

## API Key Origins

```
┌─────────────────────────────────────────────────────────────┐
│                   YOUR LOCAL .env FILE                      │
│                  (Never commit to GitHub)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GEMINI_API_KEY ←── https://aistudio.google.com/app/apikey │
│  (Starts with: AIzaSy_)                                     │
│                                                              │
│  SUPABASE_URL ←────── https://app.supabase.com              │
│  (Format: https://xxx.supabase.co)                          │
│                                                              │
│  SUPABASE_KEY ←────── https://app.supabase.com              │
│  (Settings → API → Copy anon public key)                    │
│  (Very long string starting with: eyJ...)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         ↓
    .gitignore rules prevent push
         ↓
    Only .env.example goes to GitHub (with placeholders only!)
```

---

## Step-by-Step Setup

### 1️⃣ Create .env file
```bash
# In project directory:
cp .env.example .env
```

### 2️⃣ Get API Keys

#### Google Gemini Key (3 minutes)
```
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Select/Create Google Cloud project
4. Copy the key (AIzaSy_...)
5. Paste into .env as: GEMINI_API_KEY=...
```

#### Supabase URL (3 minutes)
```
1. Go to: https://app.supabase.com
2. Open your project
3. Go to: Settings → API
4. Copy "Project URL"
5. Paste into .env as: SUPABASE_URL=...
```

#### Supabase Key (3 minutes)
```
1. Same page: Settings → API
2. Copy "anon public" key
3. Paste into .env as: SUPABASE_KEY=...
```

### 3️⃣ Verify .env is ignored
```bash
git status
# .env should NOT appear in the list
# .env.example should appear
```

### 4️⃣ Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main

# Result:
# - .env.example uploaded (safe!)
# - .env not uploaded (ignored!)
# - Your keys stay private ✅
```

---

## Checklist Before Pushing

```
❌ .env contains REAL keys?        → ✅ Check .gitignore has .env
❌ .env.example has real keys?     → ✅ Should only have placeholders
❌ Accidentally added .env?         → ✅ Run: git rm --cached .env
❌ Other secrets exposed?           → ✅ Review all files before push
```

**Safe to push?**
```bash
git status
```
Should show:
```
Modified: .env.example
New files: (your code files)
    ... (no .env file listed!)
```

---

## Security Reminders

```
🔐 PRIVATE KEYS
   ├─ Keep .env locally
   ├─ Add to .gitignore
   ├─ Never share
   ├─ Never commit
   └─ Never post in chat

📄 PUBLIC (Placeholder) KEYS
   ├─ .env.example is fine
   ├─ Safe on GitHub
   ├─ Helps others set up
   └─ No real values

📦 PRODUCTION
   ├─ Use environment variables
   ├─ Set on server/platform
   ├─ Never use .env files
   └─ Rotate keys periodically
```

---

## For Team Members / Contributors

When they clone your repo:

```bash
# 1. Clone repository
git clone https://github.com/yourname/jd-pipeline.git

# 2. Create their .env
cp .env.example .env

# 3. Add their own API keys
# (Edit .env with their OpenAI & Supabase keys)

# 4. Never commit .env
# .gitignore prevents this automatically

# 5. Ready to use
python app.py
```

---

## Quick Reference

| File | Should Push? | Contains |
|------|------|----------|
| `.env.example` | ✅ YES | Placeholders only |
| `.env` | ❌ NO | Real secret keys |
| `.gitignore` | ✅ YES | Rules (.env ignored) |
| `app.py` | ✅ YES | Application code |
| `config.py` | ✅ YES | Config structure |
| `database.py` | ✅ YES | DB operations |
| `ai_processor.py` | ✅ YES | AI logic |
| `utils.py` | ✅ YES | Utilities |
| `requirements.txt` | ✅ YES | Dependencies |
| `README.md` | ✅ YES | Documentation |

---

## Environment Loading Order

```
Python starts app.py
    ↓
Loads config.py
    ↓
config.py runs: load_dotenv()  (from python-dotenv)
    ↓
Reads .env file (from root directory)
    ↓
Sets environment variables
    ↓
app.py accesses via: os.getenv('OPENAI_API_KEY')
    ↓
Routes/modules use the keys
```

---

## Troubleshooting

### "Module not found: dotenv"
```bash
pip install python-dotenv
# Already in requirements.txt, so just run:
pip install -r requirements.txt
```

### ".env file not found"
```bash
# Create it:
cp .env.example .env
# Then add your keys
```

### "API key is None or empty"
```bash
# Check .env has values (not placeholders):
cat .env

# Should show:
OPENAI_API_KEY=sk-proj-actual-value
# NOT:
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### ".env is being tracked (about to commit)"
```bash
# Stop tracking it:
git rm --cached .env

# Verify .gitignore has it:
cat .gitignore | grep "^.env"
# Should output: .env

# Commit:
git add .gitignore
git commit -m "Stop tracking .env"
```

---

## Summary

```
Your .env file (PRIVATE - local only):
├── ENVIRONMENT=development
├── SECRET_KEY=dev-value
├── DEBUG=True
├── GEMINI_API_KEY=AIzaSy_REAL-KEY-HERE
├── SUPABASE_URL=https://real-url.supabase.co
└── SUPABASE_KEY=eyJ-REAL-KEY-HERE...

Your .env.example file (PUBLIC - on GitHub):
├── ENVIRONMENT=development
├── SECRET_KEY=your-secret-key-here-change...
├── DEBUG=True
├── GEMINI_API_KEY=your-google-gemini-api-key-here
├── SUPABASE_URL=https://your-project.supabase.co
└── SUPABASE_KEY=your-supabase-api-key-here

Result on GitHub:
✅ Code goes up
✅ .env.example goes up (safe!)
❌ .env stays private (via .gitignore)
```

---

**All set!** Your project is secure and ready to share 🚀
