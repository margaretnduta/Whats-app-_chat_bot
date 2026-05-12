# 🤖 WhatsApp Chatbot with OpenAI ChatGPT

A production-ready WhatsApp chatbot that scrapes real-time information from websites and uses OpenAI's ChatGPT to provide intelligent, context-aware responses.

## 🎯 Features

✅ **Real-time Web Scraping** - Automatically scrapes click2skill.com for latest information
✅ **Smart Caching** - Reduces API calls by caching scraped data (configurable refresh rate)
✅ **AI-Powered Responses** - Uses ChatGPT-3.5-turbo to generate natural, helpful answers
✅ **Twilio WhatsApp Integration** - Seamlessly receive and send WhatsApp messages
✅ **Mobile-Friendly Formatting** - Responses optimized for WhatsApp display
✅ **Error Handling** - Graceful error management with fallback options
✅ **Webhook Support** - Ready for production deployment

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Framework** | Flask | Lightweight and perfect for webhooks |
| **Scraping** | BeautifulSoup4 + Requests | Fast and simple for most websites |
| **AI** | OpenAI ChatGPT 3.5-turbo | Cost-effective and powerful |
| **Messaging** | Twilio WhatsApp API | Industry-standard WhatsApp integration |
| **Tunneling** | ngrok | Essential for local testing with Twilio |

## 📋 Prerequisites

Before you start, ensure you have:

1. **Python 3.8+** installed on your machine
2. **Twilio Account** with WhatsApp API access ([Get it here](https://www.twilio.com/en-us/try-twilio))
3. **OpenAI Account** with API key ([Get it here](https://platform.openai.com/account/api-keys))
4. **ngrok** for local testing ([Download here](https://ngrok.com/download))

## 🚀 Setup Instructions

### Step 1: Clone/Create Project Structure

```bash
cd "Whats-app_chat_bot"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Edit `.env` and fill in your credentials:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+1234567890

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

FLASK_ENV=development
SECRET_KEY=your-random-secret-key
```

**Where to find these credentials:**

- **Twilio Credentials**: 
  - Go to [Twilio Console](https://console.twilio.com/)
  - Find Account SID and Auth Token on the dashboard
  - Find your WhatsApp number in Messaging > Services

- **OpenAI API Key**:
  - Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
  - Click "Create new secret key"
  - Copy and save it securely

### Step 5: Run the Application

```bash
python app.py
```

Expected output:
```
✅ Configuration validated successfully
🔄 Pre-loading website data on startup...
✅ Website data loaded successfully

🚀 Starting WhatsApp Chatbot Server...
📱 Webhook endpoint: http://localhost:5000/whatsapp
🔍 Status endpoint: http://localhost:5000/status

💡 Tip: Use ngrok to expose your local server for Twilio webhooks!
   Command: ngrok http 5000
```

### Step 6: Expose Local Server with ngrok

In a **new terminal**, run:

```bash
ngrok http 5000
```

You'll see output like:
```
Forwarding  https://abcd1234.ngrok.io -> http://localhost:5000
```

**Copy the https URL** - you'll need it for the next step.

### Step 7: Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging > Services**
3. Select your WhatsApp Service (or create one)
4. In **Integration** settings, find **Webhook Configuration**
5. Set:
   - **Inbound Messages Webhook URL**: `https://your-ngrok-url.ngrok.io/whatsapp`
   - **Method**: POST
   - Click Save

### Step 8: Opt-in to WhatsApp Sandbox

To test with the WhatsApp sandbox:

1. Open WhatsApp on your phone
2. Send a message to your Twilio WhatsApp number with:
   ```
   join [keyword]
   ```
   (The keyword is shown in your Twilio WhatsApp settings)

3. You'll receive a confirmation that you've joined the sandbox

### Step 9: Start Chatting! 💬

Send a message to your Twilio WhatsApp number:
- Type `hi` or `hello` to get the welcome message
- Ask any question about Click2Skill
- The bot will respond with information scraped from the website

---

## 📁 Project Structure

```
whatsapp-chatbot/
├── app.py                 # Main Flask application with Twilio webhook
├── scraper.py            # Web scraping module with caching
├── config.py             # Configuration management
├── utils.py              # Helper functions and AI integration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual credentials (DO NOT COMMIT)
├── cache/
│   └── website_data.json # Cached website content
└── README.md            # This file
```

## 📝 Code Structure Explained

### `app.py` - Main Application
- **`/whatsapp` (POST)** - Webhook for incoming WhatsApp messages
- **`/status` (GET)** - Health check endpoint
- **`/refresh-cache` (POST)** - Manually refresh cached data
- **`/` (GET)** - Information page

### `scraper.py` - Web Scraping
- **`WebScraper` class** - Handles scraping and caching
- **Caching System** - Stores data locally, refreshes based on `CACHE_EXPIRY_MINUTES`
- **Relevant Context** - Extracts only relevant paragraphs to reduce API costs

### `utils.py` - Helper Functions
- **`AIAssistant`** - Communicates with OpenAI ChatGPT
- **Message Formatting** - Formats responses for WhatsApp display
- **Welcome Messages** - Professional greeting templates

### `config.py` - Configuration
- Loads environment variables from `.env`
- Validates required credentials
- Central place for all configuration

## 🔄 How It Works - Message Flow

```
┌─────────────┐
│   User      │
│ WhatsApp    │
└──────┬──────┘
       │ Sends message: "What courses are available?"
       │
       ▼
┌──────────────────┐
│  Twilio API      │ Receives the message
└──────┬───────────┘
       │ Webhook POST request
       │
       ▼
┌──────────────────┐
│  Flask Server    │ /whatsapp endpoint
│  app.py          │
└──────┬───────────┘
       │
       ├─► Check if message is greeting
       │
       ├─► Call scraper.py to get website data
       │   (cached if fresh, or fetches new)
       │
       ├─► Extract relevant paragraphs from scraped data
       │
       ├─► Send to OpenAI with context:
       │   "Using this context: [website data]
       │    Answer: What courses are available?"
       │
       ▼
┌──────────────────┐
│  OpenAI API      │ Generates intelligent response
└──────┬───────────┘
       │ Returns: "Based on the website, available courses include..."
       │
       ▼
┌──────────────────┐
│  Format Response │ utils.py formats for mobile
└──────┬───────────┘
       │ Makes response mobile-friendly
       │
       ▼
┌──────────────────┐
│  Send via Twilio │ Send back to user's WhatsApp
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│   User      │
│ Receives    │ "✅ Courses include: Python, Data Science, ..."
│ Response    │
└─────────────┘
```

## 💰 Cost Optimization Tips

1. **Use Caching**: Responses use cached data by default (1-hour refresh rate)
   - Each cache refresh: ~$0.0001 for scraping + $0.001 for ChatGPT
   - Without caching: $0.001+ per message

2. **Context Limiting**: Only relevant paragraphs are sent to OpenAI
   - Saves ~40% on API costs
   - Faster response times

3. **Model Choice**: Using `gpt-3.5-turbo` instead of `gpt-4`
   - 10x cheaper
   - Still intelligent for FAQ-style queries

4. **Token Limits**: Maximum 300 tokens per response
   - Keeps responses concise
   - Saves money while staying professional

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "❌ Configuration error: Missing required environment variables" | Make sure all variables in `.env` are filled. Run `python -c "from config import Config"` to check. |
| Webhook not receiving messages | Check ngrok is running. Verify webhook URL in Twilio console includes `https://`. Restart ngrok if URL changes. |
| Bot not responding | Check Flask server is running. Look at console logs for errors. Try `/status` endpoint to verify connection. |
| Slow responses | First response will be slower (scraping + API call). Subsequent requests use cache. Check your internet connection. |
| "Invalid API key" error | Verify your OpenAI API key in `.env`. Don't include `sk-` prefix if it's already there. |
| Website scraping fails | Check if website is accessible. Verify `robots.txt` allows scraping. Website structure may have changed. |

## 🔐 Security Best Practices

✅ **DO:**
- Store `.env` file **locally only** - never commit to git
- Rotate API keys regularly
- Use environment-specific secrets
- Validate input messages

❌ **DON'T:**
- Share your `.env` file
- Commit credentials to version control
- Use the same API key in development and production
- Log sensitive information

### Git Setup (if using version control)

```bash
# Add .env to .gitignore
echo ".env" >> .gitignore
echo "cache/" >> .gitignore
```

## 📊 Monitoring & Debugging

### Check Bot Status
```bash
curl http://localhost:5000/status
```

### Manually Refresh Cache
```bash
curl -X POST http://localhost:5000/refresh-cache
```

### View Console Logs
The application logs all interactions:
```
📱 Message from +1234567890:
   User: What is Click2Skill?
   Bot: Click2Skill is a comprehensive online learning platform...
```

## 🚀 Deployment Guide

### For Production Use:

1. **Get a Domain**: Use services like Heroku, AWS Lambda, or DigitalOcean
2. **Update Webhook URL**: Use your production domain instead of ngrok
3. **Use Environment-Specific Secrets**: Manage secrets via your hosting platform
4. **Enable HTTPS**: Twilio requires HTTPS webhooks
5. **Set up Monitoring**: Add error tracking (e.g., Sentry)
6. **Scale Caching**: Consider upgrading to a database or Redis

Example Heroku deployment:
```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=xxx
heroku config:set TWILIO_AUTH_TOKEN=xxx
heroku config:set OPENAI_API_KEY=xxx
git push heroku main
```

## 📚 API Reference

### Webhook Payload (from Twilio)

```json
{
  "Body": "Hi, what courses do you have?",
  "From": "whatsapp:+1234567890",
  "To": "whatsapp:+0987654321",
  "AccountSid": "ACxxx...",
  "SmsMessageSid": "SMxxx...",
  "NumMedia": "0"
}
```

### Response Format

```python
# Flask returns empty TwiML response
# WhatsApp message is sent via twilio_client.messages.create()
```

## 🤝 Contributing

Feel free to improve this bot:
- Add more data sources
- Implement vector databases for better context retrieval
- Add conversation history/memory
- Support for media messages
- Multi-language support

## 📄 License

This project is open source. Feel free to use and modify for your needs.

## 📞 Support & Resources

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **OpenAI Docs**: https://platform.openai.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

---

## 🎉 You're All Set!

Your WhatsApp chatbot is ready to go live. Start with the setup instructions and customize it for your specific needs.

**Questions?** Check the troubleshooting section or review the inline code comments for detailed explanations.

Happy chatting! 🚀
