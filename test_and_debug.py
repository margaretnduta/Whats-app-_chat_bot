"""
Testing & Quick Start Guide for WhatsApp Chatbot
This file contains examples and testing tips
"""

# ============================================================
# QUICK START - 5 MINUTE SETUP
# ============================================================

"""
1. Create .env file:
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=+1234567890
   OPENAI_API_KEY=your_key

2. Install dependencies:
   pip install -r requirements.txt

3. Start the app:
   python app.py

4. In another terminal, expose with ngrok:
   ngrok http 5000

5. Configure Twilio webhook:
   https://your-ngrok-url/whatsapp

6. Send a message to test!
"""

# ============================================================
# TESTING THE BOT LOCALLY
# ============================================================

import requests
import json
from datetime import datetime

# Test health status
def test_status():
    """Check if bot is running"""
    response = requests.get("http://localhost:5000/status")
    print("Status Check:")
    print(json.dumps(response.json(), indent=2))

# Simulate Twilio webhook
def simulate_whatsapp_message(phone_number, message_text):
    """
    Simulate a WhatsApp message from Twilio
    
    Args:
        phone_number: User's WhatsApp number (format: whatsapp:+1234567890)
        message_text: Message content
    """
    
    payload = {
        "Body": message_text,
        "From": phone_number,
        "To": "whatsapp:+your-bot-number",
        "AccountSid": "test",
        "SmsMessageSid": "test",
        "NumMedia": "0"
    }
    
    print(f"\n📱 Simulating message from {phone_number}")
    print(f"💬 Message: {message_text}")
    
    try:
        response = requests.post(
            "http://localhost:5000/whatsapp",
            data=payload
        )
        print(f"✅ Response Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test scraping
def test_scraping():
    """Test the scraper module"""
    print("\n🔍 Testing Web Scraper:")
    try:
        from scraper import get_scraped_content, get_scraper
        
        # Get content
        content = get_scraped_content()
        print(f"✅ Scraped {len(content)} characters")
        print(f"First 200 chars: {content[:200]}...")
        
        # Test refresh
        print("\n🔄 Testing cache refresh...")
        scraper = get_scraper()
        fresh_content = scraper.scrape_website(force_refresh=True)
        print(f"✅ Refreshed cache with {len(fresh_content)} characters")
        
    except Exception as e:
        print(f"❌ Scraping error: {e}")

# Test AI response
def test_ai_response():
    """Test ChatGPT integration"""
    print("\n🤖 Testing AI Response:")
    try:
        from utils import AIAssistant
        
        sample_context = """
        Click2Skill offers online courses in:
        - Python Programming (4 weeks)
        - Data Science (6 weeks)
        - Web Development (5 weeks)
        - Machine Learning (8 weeks)
        
        All courses include live mentoring and project-based learning.
        Certificates are provided upon completion.
        """
        
        sample_query = "What courses do you offer?"
        
        print(f"Query: {sample_query}")
        response = AIAssistant.generate_response(sample_query, sample_context)
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"❌ AI error: {e}")

# ============================================================
# SAMPLE CONVERSATIONS
# ============================================================

SAMPLE_CONVERSATIONS = [
    {
        "user": "Hi",
        "expected": "Welcome message with bot description"
    },
    {
        "user": "Hello",
        "expected": "Welcome message"
    },
    {
        "user": "What courses are available?",
        "expected": "List of courses from the website"
    },
    {
        "user": "How much does a course cost?",
        "expected": "Pricing information if available on website"
    },
    {
        "user": "Tell me about Python training",
        "expected": "Details about Python course"
    },
    {
        "user": "How long does the program take?",
        "expected": "Course duration information"
    },
]

# ============================================================
# DEBUGGING TIPS
# ============================================================

def print_debug_tips():
    """Print helpful debugging information"""
    print("""
    🛠️  DEBUGGING TIPS:
    
    1. Check Environment:
       python -c "from config import Config; print('✅ Config OK')"
    
    2. Test Scraper:
       python -c "from scraper import get_scraped_content; print(get_scraped_content()[:200])"
    
    3. View Console Logs:
       The app.py prints all interactions. Check for:
       - ✅ Message received
       - ✅ Data fetched
       - ✅ Response generated
    
    4. Check Twilio Webhook:
       - Verify URL is correct (https://, not http://)
       - Check POST method is selected
       - Look at Twilio Console > Logs for webhook calls
    
    5. Test ngrok Connection:
       - ngrok should show "Forwarding  https://xxx -> http://localhost:5000"
       - If connection drops, ngrok URL changes - update Twilio webhook
    
    6. Common Issues:
       - "Invalid API key": Check OpenAI key is copied correctly
       - "Webhook not called": Verify Twilio webhook URL
       - "Timeout errors": Check your internet connection/API rate limits
    """)

# ============================================================
# PERFORMANCE MONITORING
# ============================================================

def monitor_performance():
    """Monitor bot performance metrics"""
    print("""
    📊 PERFORMANCE METRICS TO TRACK:
    
    1. Response Time:
       - Should be < 5 seconds for most queries
       - First message might be slower (scraping takes time)
    
    2. Cache Hit Rate:
       - Subsequent messages within CACHE_EXPIRY_MINUTES should use cache
       - Look for "✅ Using cached data" in logs
    
    3. API Usage:
       - OpenAI: Check billing dashboard for token usage
       - Scraping: Should only happen once per CACHE_EXPIRY_MINUTES
    
    4. Error Rate:
       - Track failed messages in logs
       - Implement alerting for errors > 5%
    """)

# ============================================================
# COST ESTIMATION
# ============================================================

def estimate_costs():
    """Estimate monthly costs"""
    print("""
    💰 ESTIMATED MONTHLY COSTS (Rough):
    
    Assumption: 1000 messages per day, 30 days
    
    Twilio:
      - ~30,000 WhatsApp messages @ $0.0075/msg = $225/month
    
    OpenAI (ChatGPT-3.5):
      - ~900 API calls (1/msg, with caching) @ $0.001/msg = $0.90/month
    
    Web Scraping:
      - ~30 scrapes/month @ $0 (included in infrastructure)
    
    Total: ~$225-250/month
    
    ✅ TIP: Optimize with:
       - Longer cache expiry (2-4 hours instead of 1 hour): saves ~$0.60/month
       - Shorter responses (max_tokens=200): saves ~30% on ChatGPT costs
       - Better context filtering: reduces tokens per request
    """)

# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 WhatsApp Chatbot - Testing & Debugging")
    print("=" * 60)
    
    print("\n⚠️  IMPORTANT: Make sure app.py is running before testing!")
    print("   Command: python app.py\n")
    
    # You can uncomment these to run tests
    # test_status()
    # test_scraping()
    # test_ai_response()
    
    print("\n" + "=" * 60)
    print_debug_tips()
    print("\n" + "=" * 60)
    monitor_performance()
    print("\n" + "=" * 60)
    estimate_costs()
    print("\n" + "=" * 60)
    
    # Example: Simulate a message
    # Uncomment to test:
    # simulate_whatsapp_message("whatsapp:+1234567890", "Hi there!")
