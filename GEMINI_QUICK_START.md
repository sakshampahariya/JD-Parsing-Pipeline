# Gemini API Key - Quick Card

## 🎯 Get Gemini API Key in 2 Steps

### Step 1: Visit AI Studio
👉 **https://aistudio.google.com/app/apikey**

### Step 2: Create Key
- Click **"Create API Key"**
- Select/Create Google Cloud project
- Click **"Create API Key in new project"**
- **Copy the key** (starts with `AIzaSy_`)

✅ **DONE!** Your key looks like: `AIzaSy_xxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 🔧 Use Your Key

### In .env File
```env
GEMINI_API_KEY=AIzaSy_your-actual-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key
```

### Test It
```bash
python app.py
# Visit: http://localhost:5000/health
# Should show: "ai_processor": "ready"
```

---

## 💰 Free Tier

- **60 requests/minute** - Plenty for testing
- **$0 cost** - Completely free
- **No credit card** - Really!

---

## 🔐 Security

- ✅ Store in `.env` only
- ✅ Never push `.env` to GitHub
- ✅ `.env` is in `.gitignore` (safe!)
- ✅ Share `.env.example` (no real keys)

---

## ⚡ That's It!

You have 2 minutes of work, then your app uses FREE Gemini API! 🚀

---

## Need Help?

- **Full Setup**: [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Troubleshooting**: [README.md](README.md)
- **Visual Guide**: [WHERE_TO_FIND_KEYS.md](WHERE_TO_FIND_KEYS.md)

---

**Get key**: https://aistudio.google.com/app/apikey ← GO!
