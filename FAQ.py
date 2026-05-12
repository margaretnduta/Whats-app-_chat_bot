"""
FREQUENTLY ASKED QUESTIONS & TROUBLESHOOTING

Comprehensive guide to solve common issues
"""

FAQ = {
    "setup": {
        "title": "SETUP & INSTALLATION",
        "questions": {
            "Q1: Which Python version do I need?": """
A: Python 3.8 or higher. We recommend 3.11 for best compatibility.
Check your version: python --version
            """,
            
            "Q2: I'm getting 'pip: command not found'": """
A: pip is part of Python. Try:
   - Windows: python -m pip --version
   - macOS/Linux: pip3 --version
   
If still not found, reinstall Python and ensure you check 
"Add Python to PATH" during installation.
            """,
            
            "Q3: How do I create a virtual environment?": """
A: Run:
   python -m venv venv
   
Then activate:
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
   
You should see (venv) in your terminal prompt.
            """,
            
            "Q4: I'm getting 'Module not found' errors": """
A: Make sure you've installed requirements:
   pip install -r requirements.txt
   
And you're in the virtual environment:
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
            """,
        }
    },
    
    "credentials": {
        "title": "CREDENTIALS & API KEYS",
        "questions": {
            "Q5: Where do I get Twilio credentials?": """
A: 1. Go to https://console.twilio.com/
   2. Sign up or log in
   3. On dashboard, you'll see:
      - Account SID
      - Auth Token
   4. For WhatsApp number:
      - Go to Messaging > Services
      - Find your WhatsApp service
      - Copy the number (format: +1234567890)
            """,
            
            "Q6: Where do I get OpenAI API key?": """
A: 1. Go to https://platform.openai.com/account/api-keys
   2. Click "Create new secret key"
   3. Copy it immediately (you won't see it again!)
   4. Add to .env file as OPENAI_API_KEY=sk-xxx
   
⚠️ IMPORTANT: Keep this key secret! Never share it.
            """,
            
            "Q7: Invalid API key error - what's wrong?": """
A: Common causes:
   1. Key is incorrect or expired
      - Try generating a new one
   2. Key has leading/trailing spaces
      - Check for whitespace in .env
   3. Free trial expired
      - Set up billing at https://platform.openai.com/account/billing
   4. Used wrong key (dev vs prod)
      - Make sure it's the production key
            """,
            
            "Q8: How do I protect my API keys?": """
A: 1. NEVER commit .env to git
      - Add ".env" to .gitignore
   2. Use environment variables in production
   3. Rotate keys periodically (every 90 days)
   4. Use separate keys for dev/prod
   5. Monitor usage for suspicious activity
            """,
        }
    },
    
    "twilio": {
        "title": "TWILIO & WEBHOOK SETUP",
        "questions": {
            "Q9: How do I set up the Twilio webhook?": """
A: 1. Make sure your Flask app is running:
      python app.py
   
   2. Start ngrok in another terminal:
      ngrok http 5000
   
   3. Copy the https URL (e.g., https://abcd1234.ngrok.io)
   
   4. Go to Twilio Console > Messaging > Services
   
   5. Select your WhatsApp service
   
   6. Under "Integration", find "Webhook Configuration"
   
   7. Set:
      - Inbound Messages URL: https://your-ngrok-url/whatsapp
      - Method: POST
   
   8. Click Save
            """,
            
            "Q10: Webhook not receiving messages - why?": """
A: Common issues:
   1. Wrong URL format
      - Must start with https:// (not http://)
      - Example: https://abc123.ngrok.io/whatsapp ✓
   
   2. ngrok URL changed
      - ngrok generates a new URL each session
      - Update Twilio webhook with new URL
   
   3. Flask app crashed
      - Check console for errors
      - Restart: python app.py
   
   4. Message not sent to correct number
      - Verify you're using your bot's WhatsApp number
   
   5. Not opted into sandbox
      - Send "join [keyword]" to bot to activate
            """,
            
            "Q11: How do I opt-in to WhatsApp sandbox?": """
A: 1. Open WhatsApp on your phone
   
   2. Find your Twilio WhatsApp number (check Console)
   
   3. Send this message:
      join [keyword]
      
      (Replace [keyword] with the actual keyword from Twilio Console)
   
   4. You'll receive a confirmation
   
   5. Now you can send messages and test the bot!
            """,
            
            "Q12: I'm getting Twilio authentication errors": """
A: Check:
   1. Account SID is correct (not Auth Token)
   2. Auth Token is correct
   3. No extra spaces in .env
   4. Both values are from same account
   5. Try:
      from config import Config
      print(Config.TWILIO_ACCOUNT_SID)  # Should print your SID
            """,
        }
    },
    
    "runtime": {
        "title": "RUNTIME & PERFORMANCE",
        "questions": {
            "Q13: Bot responses are very slow": """
A: Reasons and solutions:
   1. First response (slow - normal):
      - Scraping + API call = 5-10 seconds ✓
   
   2. Subsequent responses slow:
      - Cache might be expired
      - Increase CACHE_EXPIRY_MINUTES to 120+ in .env
   
   3. OpenAI API is slow:
      - Check OpenAI status page
      - Try simpler queries
      - Consider upgrading to gpt-4 for better responses
   
   4. Network connection issue:
      - Check your internet speed
      - Look for error messages in console
            """,
            
            "Q14: Getting timeout errors": """
A: Flask server timeouts:
   1. Increase timeout in code:
      response = requests.get(url, timeout=20)
   
   2. For OpenAI, add timeout:
      model="gpt-3.5-turbo",
      timeout=30
   
   3. Check your network connection
   
   4. Website might be down
      - Test: curl https://click2skill.com
            """,
            
            "Q15: How can I speed up the bot?": """
A: Optimization tips:
   1. Enable caching (already done)
   2. Increase cache expiry time
      - CACHE_EXPIRY_MINUTES=240 (4 hours)
   3. Use Redis for caching (advanced)
   4. Use gpt-3.5-turbo (cheapest, still good)
   5. Limit response size (max_tokens=200)
   6. Use Gunicorn with multiple workers:
      gunicorn -w 4 app:app
            """,
        }
    },
    
    "scraping": {
        "title": "WEB SCRAPING ISSUES",
        "questions": {
            "Q16: Scraping fails - 'Connection refused'": """
A: 1. Check if website is online:
      - Try opening https://click2skill.com in browser
      - If it doesn't load, website is down
   
   2. Your internet is down
      - Check connection
   
   3. Website blocks your IP
      - This is rare with our headers
      - Try again in a few minutes
   
   4. Website structure changed
      - This could cause parsing issues
      - Try: python -c "from scraper import get_scraper; print(get_scraper().scrape_website())"
            """,
            
            "Q17: Scraped data looks incomplete": """
A: Causes:
   1. Website uses JavaScript to load content
      - Solution: Use Selenium/Playwright (advanced)
   
   2. Data is in hidden elements
      - BeautifulSoup might not extract it
   
   3. Website structure is complex
      - Try extracting specific sections
   
   4. Cache is old
      - Clear cache: 
        from scraper import get_scraper
        get_scraper().clear_cache()
            """,
            
            "Q18: Getting 'robots.txt denied' warnings": """
A: This is usually just a warning. But to be safe:
   1. Check if scraping is allowed:
      https://click2skill.com/robots.txt
   
   2. Respect the rules
   
   3. Or contact website owner for permission
            """,
            
            "Q19: How do I scrape dynamic websites?": """
A: For JavaScript-heavy sites, upgrade scraper.py:

   pip install playwright
   from playwright.sync_api import sync_playwright
   
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       page.goto('https://click2skill.com')
       content = page.content()
       browser.close()
   
   Then parse with BeautifulSoup.
            """,
        }
    },
    
    "deployment": {
        "title": "DEPLOYMENT & PRODUCTION",
        "questions": {
            "Q20: How do I deploy to production?": """
A: Three options:

   1. HEROKU (easiest):
      - Create Procfile (already provided)
      - heroku login
      - heroku create app-name
      - heroku config:set TWILIO_ACCOUNT_SID=xxx ...
      - git push heroku main
      - URL: https://app-name.herokuapp.com/whatsapp
   
   2. AWS LAMBDA (serverless):
      - More complex but cheaper at scale
      - See ADVANCED_GUIDE.py
   
   3. DOCKER (portable):
      - docker-compose up -d
      - Works anywhere with Docker
            """,
            
            "Q21: How do I get a permanent domain?": """
A: 1. Remove ngrok dependency by deploying to:
      - Heroku
      - AWS
      - DigitalOcean
      - Google Cloud
   
   2. Get a domain:
      - Namecheap, GoDaddy, Route53, etc.
   
   3. Update Twilio webhook to permanent URL
   
   4. Your bot now has a permanent home!
            """,
            
            "Q22: How do I monitor the bot in production?": """
A: Set up monitoring:
   1. Health checks:
      - curl https://your-bot.com/status
   
   2. Error tracking:
      - pip install sentry-sdk
      - Set SENTRY_DSN in .env
   
   3. Logging:
      - CloudWatch (AWS)
      - Heroku logs
      - Custom logging
   
   4. Metrics:
      - Messages per day
      - Response time
      - Error rate
      - API costs
            """,
        }
    },
    
    "errors": {
        "title": "COMMON ERROR MESSAGES",
        "questions": {
            "Q23: 'ModuleNotFoundError: No module named flask'": """
A: Solution:
   1. Activate virtual environment:
      - Windows: venv\Scripts\activate
      - macOS/Linux: source venv/bin/activate
   
   2. Install requirements:
      pip install -r requirements.txt
            """,
            
            "Q24: 'APIConnectionError' from OpenAI": """
A: Reasons:
   1. Internet connection issue
      - Check connection
   
   2. OpenAI API is down
      - Check https://status.openai.com
   
   3. Your API key is invalid
      - Regenerate at platform.openai.com
   
   4. Rate limited
      - Wait a minute and try again
      - Consider upgrading account
            """,
            
            "Q25: 'TwilioRestException: Authentication failed'": """
A: Fix:
   1. Verify Account SID:
      - Go to Twilio Console dashboard
      - Copy exact Account SID (not Auth Token)
   
   2. Verify Auth Token:
      - Must be current (not old/revoked)
   
   3. Check .env format:
      TWILIO_ACCOUNT_SID=ACxxxxxxxxxx
      TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
      
      (No quotes, no extra spaces)
            """,
            
            "Q26: 'JSONDecodeError' in cache": """
A: Cache file corrupted:
   1. Delete cache file:
      del cache/website_data.json
   
   2. Restart app:
      python app.py
   
   3. It will regenerate automatically
            """,
        }
    },
}


def print_all_faqs():
    """Print all FAQs in organized format"""
    for section_key, section in FAQ.items():
        print(f"\n{'=' * 70}")
        print(f"📚 {section['title']}")
        print(f"{'=' * 70}\n")
        
        for question, answer in section['questions'].items():
            print(f"{question}")
            print(f"{answer}")
            print()


def search_faq(keyword):
    """Search FAQs for a keyword"""
    results = []
    keyword_lower = keyword.lower()
    
    for section_key, section in FAQ.items():
        for question, answer in section['questions'].items():
            if keyword_lower in question.lower() or keyword_lower in answer.lower():
                results.append((section['title'], question, answer))
    
    return results


def print_section(section_key):
    """Print a specific FAQ section"""
    if section_key in FAQ:
        section = FAQ[section_key]
        print(f"\n{'=' * 70}")
        print(f"📚 {section['title']}")
        print(f"{'=' * 70}\n")
        
        for question, answer in section['questions'].items():
            print(f"{question}")
            print(f"{answer}")
            print()
    else:
        print(f"❌ Section not found. Available: {', '.join(FAQ.keys())}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "search":
            keyword = " ".join(sys.argv[2:])
            results = search_faq(keyword)
            if results:
                print(f"\n🔍 Search results for '{keyword}':\n")
                for section_title, question, answer in results:
                    print(f"[{section_title}]")
                    print(f"{question}")
                    print(f"{answer}")
                    print()
            else:
                print(f"❌ No results found for '{keyword}'")
        elif sys.argv[1] in FAQ:
            print_section(sys.argv[1])
        else:
            print("❌ Invalid section. Available: setup, credentials, twilio, runtime, scraping, deployment, errors")
    else:
        # Interactive menu
        print("=" * 70)
        print("🤖 WhatsApp Chatbot - FAQ & Troubleshooting")
        print("=" * 70)
        print("\nAvailable sections:")
        for i, (key, section) in enumerate(FAQ.items(), 1):
            print(f"{i}. {section['title']}")
        
        choice = input("\nEnter section number (or 'all' for everything): ").strip().lower()
        
        if choice == "all":
            print_all_faqs()
        elif choice.isdigit():
            section_key = list(FAQ.keys())[int(choice) - 1]
            print_section(section_key)
        else:
            print("❌ Invalid choice")
