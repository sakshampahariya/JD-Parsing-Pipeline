# Getting API Keys - Quick Checklist

## 🎯 What You Need (2 Services, 3 Keys)

### Service 1: Google Gemini (1 API Key)
- ✅ File: [API_KEYS_SETUP.md](API_KEYS_SETUP.md) - Full guide with screenshots
- ⏱️ Time: 3 minutes
- 💵 Free tier: 60 requests per minute (FREE!)

### Service 2: Supabase (2 Keys)
- ✅ File: [API_KEYS_SETUP.md](API_KEYS_SETUP.md) - Full guide with screenshots  
- ⏱️ Time: 5 minutes
- 💵 Free tier: 500MB storage (plenty!)

---

## 🚀 Quick Start (60 Seconds)

### Step 1: Get Your Keys (10 min total)
```
Google Gemini: https://aistudio.google.com/app/apikey
Supabase:      https://app.supabase.com → Settings → API
```

### Step 2: Add to .env
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your real keys
GEMINI_API_KEY=AIzaSy_your-actual-key
SUPABASE_URL=https://your-actual-url.supabase.co  
SUPABASE_KEY=eyJ-your-actual-key...
```

### Step 3: Run App
```bash
python app.py
# Open: http://localhost:5000
```

### Step 4: Push to GitHub (Safe!)
```bash
git add .
git commit -m "Add job pipeline app"
git push
# .env is ignored, .env.example is included (no secrets!)
```

---

## 📋 Keys You Need

| Service | Key | Where | Example |
|---------|-----|-------|---------|
| **Google Gemini** | `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey | `AIzaSy_...` |
| **Supabase** | `SUPABASE_URL` | Settings → API → Project URL | `https://xxx.supabase.co` |
| **Supabase** | `SUPABASE_KEY` | Settings → API → anon public | `eyJ...` |

---

## ✅ GitHub Safety Check

**Your project is already safe!** ✓

```
✅ .env             → In .gitignore (NOT pushed)
✅ .env.example     → No real keys (SAFE to push)
✅ .gitignore       → Has .env rules (READY!)
```

**Before pushing, verify:**
```bash
git status
# Should show:
# .env.example (green - will be pushed)
# NOT .env (should be untracked/ignored)
```

---

## 📖 Full Guide

👉 See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for:
- ✅ Detailed step-by-step instructions
- ✅ Where to find each key
- ✅ Cost breakdown
- ✅ Security best practices
- ✅ Troubleshooting

---

## Common Questions

### Q: Is .env file safe to commit?
**A:** NO! ❌ Keep it private. It's already in `.gitignore` ✅

### Q: Can I share .env.example on GitHub?
**A:** YES! ✅ It has no real keys, just placeholders

### Q: How much will this cost?
**A:** Completely FREE!
- Google Gemini: FREE tier with 60 requests/minute
- Supabase: FREE tier (500MB storage)

### Q: Do I need credit card?
**A:** Yes, for OpenAI (they charge per API use, but very affordable)

### Q: Can others use the repo?
**A:** YES! They just:
1. Copy `cp .env.example .env`
2. Add their own API keys
3. Never commit `.env`

---

## Next Steps

1. **Read**: [API_KEYS_SETUP.md](API_KEYS_SETUP.md)
2. **Get Keys**: OpenAI + Supabase
3. **Update**: .env file
4. **Test**: `python app.py`
5. **Push**: `git push` (safely!)

---

**Ready?** Start with [API_KEYS_SETUP.md](API_KEYS_SETUP.md) 👈
