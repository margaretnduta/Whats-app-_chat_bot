"""
QUICK START GUIDE - Get Your Bot Running in 10 Minutes!

Follow these steps in order. Should take ~10 minutes for complete setup.
"""

QUICK_START = """
🚀 WHATSAPP CHATBOT - 10 MINUTE QUICK START
============================================

PREREQUISITES:
✓ Python 3.8+ installed (python --version)
✓ Twilio Account (https://www.twilio.com)
✓ OpenAI API Key (https://platform.openai.com)
✓ ngrok installed (https://ngrok.com/download)

STEP-BY-STEP:
═════════════

STEP 1: CREATE CREDENTIALS (3 minutes)
──────────────────────────────────────

A) Get Twilio Credentials:
   1. Go to https://console.twilio.com/
   2. Login or create account
   3. Copy "Account SID" (starts with AC...)
   4. Copy "Auth Token"
   5. Go to Messaging > Services > WhatsApp
   6. Copy your WhatsApp number (e.g., +1234567890)

B) Get OpenAI API Key:
   1. Go to https://platform.openai.com/account/api-keys
   2. Click "Create new secret key"
   3. Copy it (won't show again!)

C) Create .env file in project folder:
   
   ┌─────────────────────────────────────────────┐
   │ TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx       │
   │ TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxx     │
   │ TWILIO_WHATSAPP_NUMBER=+1234567890         │
   │ OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx        │
   │ FLASK_ENV=development                       │
   │ SECRET_KEY=dev-secret                       │
   └─────────────────────────────────────────────┘


STEP 2: INSTALL & RUN (5 minutes)
─────────────────────────────────

Terminal 1 - Start the bot:
   
   python -m venv venv           # Create environment
   venv\Scripts\activate          # Activate (Windows)
   # OR: source venv/bin/activate (macOS/Linux)
   
   pip install -r requirements.txt
   python app.py
   
   You should see:
   ✅ Configuration validated successfully
   🚀 Starting WhatsApp Chatbot Server...


Terminal 2 - Expose with ngrok:
   
   ngrok http 5000
   
   Copy the URL (e.g., https://abc123.ngrok.io)


STEP 3: CONFIGURE TWILIO (2 minutes)
────────────────────────────────────

1. Go to Twilio Console
2. Navigate to Messaging > Services > WhatsApp > Integration
3. In "Inbound Messages" section:
   - Webhook URL: https://your-ngrok-url/whatsapp
   - Method: POST
4. Click Save
5. Send "join [keyword]" to your WhatsApp bot number to activate


STEP 4: TEST THE BOT (1 minute)
───────────────────────────────

1. Open WhatsApp
2. Send message to your bot's WhatsApp number
3. Type: "Hi" or "Hello"
4. You should get a welcome message! 🎉
5. Ask: "What courses are available?"
6. Bot responds with scraped info from click2skill.com


DONE! 🎉 Your bot is live!


NEXT STEPS:
═══════════

1. Test different questions
2. Monitor responses in console
3. Review README.md for detailed documentation
4. Check ADVANCED_GUIDE.py for production deployment
5. See FAQ.py for troubleshooting


QUICK TROUBLESHOOTING:
═════════════════════

Problem: "Module not found"
→ Did you activate venv? (venv\Scripts\activate)
→ Did you run pip install -r requirements.txt?

Problem: "Invalid API key"
→ Check credentials in .env file
→ Make sure no extra spaces

Problem: Webhook not receiving messages
→ Is Flask app running? (Terminal 1)
→ Is ngrok running? (Terminal 2)
→ Did you update Twilio with ngrok URL?
→ Did you send "join [keyword]" to activate?

Problem: Slow responses
→ First response is slow (normal - 5-10 seconds)
→ Subsequent responses use cache (should be instant)

More help: python FAQ.py


IMPORTANT NOTES:
════════════════

✓ Keep .env file secure (never commit to git)
✓ Each ngrok session gets a new URL (update Twilio if it changes)
✓ Website scraping happens once per hour (configurable)
✓ Free tier: ~$0.15 per message with Twilio + $0.001 with OpenAI
✓ Cache reduces costs significantly (~70% saving)


DEPLOYMENT CHECKLIST:
═════════════════════

For production (live WhatsApp number):

□ Set FLASK_ENV=production
□ Use permanent domain (Heroku, AWS, etc.) instead of ngrok
□ Enable HTTPS (required by Twilio)
□ Set up monitoring/error tracking
□ Implement rate limiting
□ Set up daily backups
□ Monitor API costs
□ Test thoroughly before going live

See ADVANCED_GUIDE.py > Section 1 (Heroku) for production setup.


USEFUL COMMANDS:
════════════════

# Check bot status
curl http://localhost:5000/status

# Manually refresh cache
curl -X POST http://localhost:5000/refresh-cache

# Run tests/debugging
python test_and_debug.py

# View FAQ
python FAQ.py

# View advanced guides
python ADVANCED_GUIDE.py


PROJECT STRUCTURE:
══════════════════

whatsapp-chatbot/
├── app.py              ← Main Flask app
├── scraper.py          ← Website scraper
├── utils.py            ← Helper functions
├── config.py           ← Configuration
├── requirements.txt    ← Dependencies
├── .env                ← Your credentials
├── README.md           ← Full documentation
├── ADVANCED_GUIDE.py   ← Production tips
├── FAQ.py              ← Troubleshooting
└── cache/              ← Cached data
    └── website_data.json


FLOW DIAGRAM:
═════════════

User: "Hello"
  ↓
WhatsApp → Twilio
  ↓
Your Server (Flask)
  ├─ Check if greeting
  ├─ Scrape website data (cached)
  ├─ Send to ChatGPT
  └─ Return response
  ↓
Twilio → WhatsApp
  ↓
User: Gets answer! 🎉


GOTCHAS TO AVOID:
═════════════════

❌ Don't: Commit .env file to git
✓ Do: Add .env to .gitignore

❌ Don't: Restart ngrok without updating Twilio webhook
✓ Do: Keep ngrok URL current in Twilio Console

❌ Don't: Scrape every message
✓ Do: Use caching (already implemented)

❌ Don't: Send huge amounts of context to OpenAI
✓ Do: Extract relevant paragraphs (already implemented)

❌ Don't: Use free trial API key in production
✓ Do: Set up billing in OpenAI dashboard


COSTS:
══════

With 1000 messages/day:
- Twilio: ~$225/month
- OpenAI: ~$1/month (with caching)
- Total: ~$226/month

💡 TIP: Longer cache expiry reduces OpenAI costs by ~70%


NEED HELP?
══════════

1. Check README.md for detailed documentation
2. Run: python FAQ.py
3. Check console logs for error messages
4. Review test_and_debug.py for testing tips
5. See ADVANCED_GUIDE.py for deployment help


HAPPY CHATTING! 🚀

Questions? See README.md or FAQ.py
"""


# Print formatted guides
def print_quick_start():
    """Print the quick start guide"""
    print(QUICK_START)


def print_file_structure():
    """Print what files were created"""
    files = {
        "Core Application": [
            "app.py - Main Flask app with Twilio webhook",
            "scraper.py - Website scraping with caching",
            "utils.py - Helper functions and AI integration",
            "config.py - Configuration management",
        ],
        "Configuration": [
            ".env.example - Template for credentials",
            ".env - Your actual credentials (create this!)",
            "requirements.txt - Python dependencies",
            "requirements-dev.txt - Development tools",
        ],
        "Deployment": [
            "Procfile - Heroku deployment",
            "Dockerfile - Docker container",
            "docker-compose.yml - Docker compose",
            "runtime.txt - Python version for Heroku",
        ],
        "Documentation": [
            "README.md - Complete documentation",
            "ADVANCED_GUIDE.py - Production tips",
            "FAQ.py - Troubleshooting guide",
            "test_and_debug.py - Testing utilities",
        ],
        "Other": [
            ".gitignore - Git ignore rules",
        ],
    }
    
    print("\n" + "=" * 70)
    print("📁 PROJECT FILES CREATED")
    print("=" * 70 + "\n")
    
    for category, file_list in files.items():
        print(f"✓ {category}:")
        for file in file_list:
            print(f"  - {file}")
        print()


def print_next_steps():
    """Print next steps"""
    print("=" * 70)
    print("📋 NEXT STEPS")
    print("=" * 70 + "\n")
    
    steps = [
        "1. Create .env file (copy from .env.example)",
        "2. Fill in your Twilio and OpenAI credentials",
        "3. Run: python -m venv venv",
        "4. Activate virtual environment",
        "5. Run: pip install -r requirements.txt",
        "6. Run: python app.py",
        "7. In another terminal: ngrok http 5000",
        "8. Update Twilio webhook with ngrok URL",
        "9. Send 'join [keyword]' to activate WhatsApp",
        "10. Start chatting!",
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n💡 Full instructions in README.md")
    print("❓ Questions? Check FAQ.py or ADVANCED_GUIDE.py\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "files":
            print_file_structure()
        elif sys.argv[1] == "next":
            print_next_steps()
        else:
            print_quick_start()
    else:
        print_quick_start()
        print_file_structure()
        print_next_steps()
