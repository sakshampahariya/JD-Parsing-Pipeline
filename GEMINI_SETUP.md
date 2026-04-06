# Google Gemini API Setup Guide

## ✨ Why Google Gemini?

- **100% FREE** - No credit card required
- **60 requests per minute** - Great for development
- **Easy setup** - Takes 2 minutes
- **No billing worries** - No surprises in costs
- **Powerful models** - Gemini 1.5 Flash & Pro available

---

## 🚀 Getting Your Google Gemini API Key (2 Minutes)

### Step 1: Visit Google AI Studio
1. Go to: **https://aistudio.google.com/app/apikey**
2. You'll be greeted with the Google AI dashboard

### Step 2: Create API Key
1. Click the blue button: **"Create API Key"**
2. A dialog will appear asking to create a key in a Google Cloud project

### Step 3: Select or Create Project
- **Option A: Use existing project** (if you have one)
  - Select it from the dropdown
  - Click "Create API Key in existing project"

- **Option B: Create new project** (recommended for beginners)
  - Click "Create new project"
  - Wait a few seconds for creation
  - Google will automatically create a new project
  - Click "Create API Key in new project"

### Step 4: Copy Your API Key
1. A new page will show your generated API key
2. It will look like: `AIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
3. **Copy it immediately** by clicking the copy icon
4. Keep it safe - treat it like a password

---

## 📝 Add to Your Project

### Step 1: Create .env File
```bash
cd d:\task temp\jd-pipeline
cp .env.example .env
```

### Step 2: Edit .env
Open `.env` in your text editor and update:

```env
# From Google Gemini API
GEMINI_API_KEY=AIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Your Supabase keys (if using database)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key
```

---

## ✅ Verify Your Setup

### Test 1: Check Environment Variable
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSy_your-key"
echo $env:GEMINI_API_KEY

# Linux/Mac
export GEMINI_API_KEY="AIzaSy_your-key"
echo $GEMINI_API_KEY
```

### Test 2: Run Health Check
```bash
# Make sure Flask is running
python app.py

# In another terminal:
curl http://localhost:5000/health

# Should show:
# {
#   "status": "healthy",
#   "ai_processor": "ready",
#   "database": "connected"
# }
```

### Test 3: Process a Sample JD
1. Open: http://localhost:5000
2. Paste the sample job description from `sample_jd.txt`
3. Click "Process"
4. Should extract structured data successfully

---

## 📊 API Key Details

### Your API Key Format
```
APIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
│      │
│      └─ Random string (40+ characters)
└───────── Always starts with "AIzaSy_"
```

### Security Notes
- ✅ This API key is private to your Google Cloud project
- ✅ It's safe to use in development
- ✅ Keep it in `.env` (never in code)
- ✅ Add `.env` to `.gitignore` (already done)

### File Locations
```
.env                ← Your actual key (PRIVATE)
  GEMINI_API_KEY=AIzaSy_...

.env.example        ← Placeholder only (SAFE for GitHub)
  GEMINI_API_KEY=your-google-gemini-api-key-here

Both files use same variable name!
```

---

## 🆓 Free Tier Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Requests/minute | 60 | Plenty for development |
| Cost | $0 | Completely free |
| Storage | None | Stateless API |
| Expiration | Never | No trial period |

### Pro Tips for Free Tier
- Batch process JDs if you have >60 per minute
- No payments ever needed for development
- Perfect for prototyping

---

## 🔄 Upgrading (Optional)

When you need higher limits:

1. Go to: https://cloud.google.com/generative-ai/docs/pricing
2. Upgrade to **Gemini API** (paid tier)
3. Paid pricing: Very affordable (~$0.075 per 1M input tokens)
4. Same API key, just higher limits

---

## Troubleshooting

### ❌ "AI processor not available"
**Solution:**
1. Check `.env` file exists
2. Verify `GEMINI_API_KEY` is filled with actual key
3. Verify key starts with `AIzaSy_`
4. No extra spaces or newlines
5. Restart Flask: `python app.py`

### ❌ "Invalid API Key"
**Solution:**
1. Go back to: https://aistudio.google.com/app/apikey
2. Check if key is still valid (not revoked)
3. Generate a new key if needed
4. Update `.env` with new key

### ❌ "API Key not found in request"
**Solution:**
```bash
# Verify .env is being loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
# Should output your actual key (first 15 chars): AIzaSy_xxxxxxxx
```

### ❌ "Rate limit exceeded"
**Solution:**
- Free tier: 60 requests/minute
- Wait 60 seconds
- Or upgrade to paid tier if you need more

---

## Common Tasks

### Can I share my API key?
❌ **NO** - Keep it private
- It's like a password
- Only share `.env.example` (which has no real key)

### Can I use the same key in production?
✅ **YES** - Google Gemini free key works everywhere
- Same limits apply
- Upgrade to paid tier for higher limits

### How do I switch back to OpenAI?
❌ **Why?** Gemini is free!
- But if needed, see: [AI_PROCESSOR_SWITCH.md](AI_PROCESSOR_SWITCH.md)

### Can I use multiple API keys?
❌ **Not needed** for this app
- One key handles all requests

---

## Comparison: Gemini vs OpenAI

| Feature | Gemini | OpenAI |
|---------|--------|--------|
| **Cost** | FREE | Pay per use |
| **Setup** | 2 min | 5 min (+credit card) |
| **Rate Limit** | 60/min free | Limited by credits |
| **Models** | Gemini 1.5 | GPT-4o-mini |
| **JSON Output** | ✅ Supported | ✅ Supported |
| **Free Tier** | ✅ Generous | ✅ Limited ($5) |

---

## Next Steps

1. ✅ Get your Gemini API key (now!)
2. ✅ Add to `.env` file
3. ✅ Test health check: `curl http://localhost:5000/health`
4. ✅ Process sample JD from web UI
5. ✅ Push to GitHub safely (`.env` is ignored)

---

## Support

### Need Help?
- Check .env file setup
- Verify key is not expired
- Review Flask logs for errors
- Test with simple JD text first

### Report Issues
- Google AI Studio: https://aistudio.google.com
- Gemini API Docs: https://ai.google.dev

---

**You're all set!** 🚀

Your app now uses Google Gemini's powerful language models - completely free!
