# 🍌 Nano Banana AI Bot — Deployed on Render.com

This bot automatically generates 20 AI-themed posts daily (07:00–21:00 UTC) with text + image and sends them to your Telegram channel using Gemini 2.5 Flash Image and Gemini 1.5 Flash.

## 🚀 How to Deploy on Render.com

1. Go to [https://render.com](https://render.com) and sign up.
2. Click **New +** → **Web Service**
3. Connect your GitHub repo (or paste code manually)
4. In **Environment Variables**, add:
   - `GOOGLE_API_KEY` → Your Google AI Studio API Key (get from [AI Studio](https://makersuite.google.com/app/apikey))
   - `TELEGRAM_BOT_TOKEN` → Your Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
   - `TELEGRAM_CHANNEL_ID` → Your channel username (e.g., `@ai_learn_uz`)
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python main.py`
7. **Runtime**: `Python 3.10`
8. **Health Check Path**: `/health`
9. Click **Create Web Service**

💡 **Free Tier Note**: To keep your bot active 24/7 on the free plan, set up a free uptime monitor (like UptimeRobot) to ping your service URL every 5 minutes.

✅ Bot will start automatically and run 24/7!

## 💡 Features
- Generates real images using Gemini 2.5 Flash Image Preview
- "Nano Banana" visual metaphor in every post
- Fallback: text-as-image if image generation fails
- Works in Uzbek language
- Posts every 42 minutes between 07:00–21:00 UTC

## 📌 Note
Gemini 2.5 Flash Image is in preview mode — may occasionally fail. Fallback ensures 100% uptime.