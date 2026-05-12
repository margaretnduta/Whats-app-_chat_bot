"""
ADVANCED CONFIGURATION & DEPLOYMENT GUIDE

This file contains advanced setup instructions for different scenarios:
1. Production Deployment (Heroku, AWS, DigitalOcean)
2. Docker Deployment
3. Custom Scraping Configuration
4. Performance Optimization
"""

# ============================================================
# 1. HEROKU DEPLOYMENT
# ============================================================

HEROKU_SETUP = """
HEROKU DEPLOYMENT STEPS:

1. Install Heroku CLI:
   https://devcenter.heroku.com/articles/heroku-cli

2. Create Procfile (in project root):
   ---
   web: python app.py
   ---

3. Create runtime.txt (in project root):
   ---
   python-3.11.0
   ---

4. Initialize git and deploy:
   heroku login
   heroku create your-bot-name
   git push heroku main

5. Set environment variables:
   heroku config:set TWILIO_ACCOUNT_SID=xxx
   heroku config:set TWILIO_AUTH_TOKEN=xxx
   heroku config:set TWILIO_WHATSAPP_NUMBER=+1234567890
   heroku config:set OPENAI_API_KEY=xxx
   heroku config:set FLASK_ENV=production

6. View logs:
   heroku logs --tail

7. Update Twilio webhook:
   https://your-heroku-app.herokuapp.com/whatsapp
"""

# ============================================================
# 2. AWS LAMBDA DEPLOYMENT
# ============================================================

AWS_LAMBDA_SETUP = """
AWS LAMBDA DEPLOYMENT (Serverless):

1. Install AWS SAM CLI:
   https://docs.aws.amazon.com/serverless-application-model/

2. Create template.yaml:
   ---
   AWSTemplateFormatVersion: '2010-09-09'
   Transform: AWS::Serverless-2016-10-31

   Globals:
     Function:
       Timeout: 30

   Resources:
     WhatsAppBotFunction:
       Type: AWS::Serverless::Function
       Properties:
         CodeUri: .
         Handler: app.lambda_handler
         Runtime: python3.11
         Events:
           WhatsAppWebhook:
             Type: Api
             Properties:
               Path: /whatsapp
               Method: POST
         Environment:
           Variables:
             TWILIO_ACCOUNT_SID: !Ref TwilioAccountSid
             TWILIO_AUTH_TOKEN: !Ref TwilioAuthToken
             OPENAI_API_KEY: !Ref OpenAIKey

   Parameters:
     TwilioAccountSid:
       Type: String
     TwilioAuthToken:
       Type: String
     OpenAIKey:
       Type: String
   ---

3. Deploy:
   sam build
   sam deploy --guided

4. Get API endpoint from CloudFormation outputs
5. Update Twilio webhook to API endpoint
"""

# ============================================================
# 3. DOCKER DEPLOYMENT
# ============================================================

DOCKERFILE_CONTENT = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create cache directory
RUN mkdir -p cache

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:5000/status')"

# Run application
CMD ["python", "app.py"]
"""

DOCKER_COMPOSE = """
version: '3.8'

services:
  whatsapp-bot:
    build: .
    container_name: whatsapp_chatbot
    ports:
      - "5000:5000"
    environment:
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - TWILIO_WHATSAPP_NUMBER=${TWILIO_WHATSAPP_NUMBER}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./cache:/app/cache
    restart: unless-stopped

# Usage:
# docker-compose up -d
# docker-compose logs -f
# docker-compose down
"""

# ============================================================
# 4. PERFORMANCE OPTIMIZATION
# ============================================================

PERFORMANCE_TIPS = """
🚀 PERFORMANCE OPTIMIZATION GUIDE:

1. RESPONSE TIME OPTIMIZATION:
   ├─ Increase CACHE_EXPIRY_MINUTES: 60 → 120-240 minutes
   │  └─ Reduces cold starts by ~70%
   ├─ Use Redis for caching instead of JSON files
   │  └─ Speeds up cache retrieval by ~1000x
   └─ Implement request batching for bulk operations

2. API COST REDUCTION:
   ├─ Improve context selection algorithm
   │  └─ Send only 1-2 relevant paragraphs instead of full text
   ├─ Implement question categorization
   │  └─ FAQ questions can use pre-built responses
   └─ Cache frequently asked questions
      └─ Skip API calls for 80% of common queries

3. CONCURRENT REQUEST HANDLING:
   ├─ Use Gunicorn instead of Flask dev server:
   │  "gunicorn -w 4 app:app"
   ├─ Add request queuing for spike handling
   └─ Implement rate limiting per user

4. DATABASE OPTIMIZATION:
   ├─ Upgrade from JSON to SQLite:
   │  "pip install sqlalchemy"
   ├─ Or use PostgreSQL for production
   └─ Index frequently queried fields

5. MONITORING & ALERTING:
   ├─ Set up Sentry for error tracking
   ├─ CloudWatch for AWS metrics
   └─ DataDog/New Relic for APM monitoring
"""

# ============================================================
# 5. ADVANCED SCRAPING CONFIGURATION
# ============================================================

ADVANCED_SCRAPING = """
ADVANCED WEB SCRAPING SETUP:

1. HANDLING JAVASCRIPT-HEAVY SITES:
   Replace BeautifulSoup with Selenium/Playwright:
   
   from playwright.async_api import async_playwright
   
   async def scrape_with_js():
       async with async_playwright() as p:
           browser = await p.chromium.launch()
           page = await browser.new_page()
           await page.goto('https://click2skill.com')
           content = await page.content()
           await browser.close()
           return content

2. HANDLING ROBOTS.TXT:
   Check if scraping is allowed:
   
   from urllib.robotparser import RobotFileParser
   
   rp = RobotFileParser()
   rp.set_url('https://click2skill.com/robots.txt')
   rp.read()
   
   if rp.can_fetch('*', 'https://click2skill.com/'):
       # Safe to scrape
       pass

3. HANDLING RATE LIMITING:
   Implement backoff and retry logic:
   
   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry
   
   session = requests.Session()
   retry = Retry(total=3, backoff_factor=0.5)
   adapter = HTTPAdapter(max_retries=retry)
   session.mount('http://', adapter)
   session.mount('https://', adapter)

4. MULTI-SOURCE SCRAPING:
   Scrape multiple websites and combine:
   
   sources = [
       'https://click2skill.com',
       'https://learn.click2skill.com',
       'https://blog.click2skill.com'
   ]
   
   all_content = []
   for source in sources:
       content = scrape_website(source)
       all_content.append(content)

5. SCHEDULE REGULAR UPDATES:
   Use APScheduler for automatic refreshes:
   
   from apscheduler.schedulers.background import BackgroundScheduler
   
   scheduler = BackgroundScheduler()
   scheduler.add_job(refresh_cache, 'interval', hours=1)
   scheduler.start()
"""

# ============================================================
# 6. SECURITY BEST PRACTICES
# ============================================================

SECURITY_GUIDE = """
🔐 SECURITY BEST PRACTICES:

1. INPUT VALIDATION:
   ✓ Validate all WhatsApp message inputs
   ✓ Sanitize before sending to OpenAI
   ✓ Implement message length limits
   
   Example:
   MAX_MESSAGE_LENGTH = 1000
   if len(incoming_msg) > MAX_MESSAGE_LENGTH:
       return "Message too long. Please keep under 1000 characters."

2. RATE LIMITING:
   ✓ Limit messages per user per minute
   ✓ Prevent abuse and API overuse
   
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address
   
   limiter = Limiter(app, key_func=get_remote_address)
   
   @app.route('/whatsapp', methods=['POST'])
   @limiter.limit("10 per minute")
   def whatsapp_webhook():
       pass

3. AUTHENTICATION:
   ✓ Verify Twilio webhook signatures
   
   from twilio.request_validator import RequestValidator
   
   validator = RequestValidator(Config.TWILIO_AUTH_TOKEN)
   
   if not validator.validate(request.url, request.form, 
                             request.headers.get('X-Twilio-Signature')):
       return 'Unauthorized', 403

4. API KEY ROTATION:
   ✓ Rotate OpenAI keys every 90 days
   ✓ Use separate keys for dev/prod
   ✓ Store keys in secure vaults (AWS Secrets Manager, HashiCorp Vault)

5. LOGGING & MONITORING:
   ✓ Never log API keys or tokens
   ✓ Monitor for suspicious patterns
   ✓ Set up alerts for repeated failures
   
   # Safe logging
   print(f"Received message from {phone_number}")  # Safe
   print(f"API Key: {api_key}")  # NEVER DO THIS!

6. HTTPS/TLS:
   ✓ Always use HTTPS for webhooks
   ✓ Verify SSL certificates
   ✓ Pin certificates for added security
"""

# ============================================================
# 7. SCALING STRATEGIES
# ============================================================

SCALING_GUIDE = """
📈 SCALING STRATEGIES:

1. VERTICAL SCALING (Single Server):
   ├─ Increase server resources (CPU, RAM)
   ├─ Upgrade from gpt-3.5-turbo to gpt-4 if needed
   └─ Use Redis caching for 10x speed improvement

2. HORIZONTAL SCALING (Multiple Servers):
   ├─ Load balancer (AWS ELB, Nginx)
   ├─ Shared cache (Redis cluster)
   ├─ Centralized database (PostgreSQL)
   └─ Message queue (RabbitMQ) for high throughput

3. ARCHITECTURE FOR 100K+ USERS:
   ┌─────────────────────────────────────┐
   │    Twilio WhatsApp Gateway          │
   ├─────────────────────────────────────┤
   │ (Load Balancer - Nginx/HAProxy)    │
   ├─────────────────────────────────────┤
   │  ┌─────────────┐  ┌─────────────┐  │
   │  │   Flask     │  │   Flask     │  │
   │  │  Instance 1 │  │  Instance 2 │  │
   │  └─────────────┘  └─────────────┘  │
   ├─────────────────────────────────────┤
   │    Message Queue (RabbitMQ)         │
   ├─────────────────────────────────────┤
   │    Shared Cache (Redis)             │
   ├─────────────────────────────────────┤
   │    Database (PostgreSQL)            │
   └─────────────────────────────────────┘

4. CACHING STRATEGY:
   Layer 1: In-memory (Python dict) - microseconds
   Layer 2: Redis - milliseconds
   Layer 3: Database - milliseconds
   Layer 4: API call - seconds

5. ASYNC PROCESSING:
   ├─ Use Celery for heavy tasks
   ├─ Process long-running requests asynchronously
   └─ Keep webhook responses fast (<2s)
"""

# ============================================================
# 8. MONITORING & OBSERVABILITY
# ============================================================

MONITORING_SETUP = """
📊 MONITORING & OBSERVABILITY SETUP:

1. SENTRY ERROR TRACKING:
   pip install sentry-sdk
   
   import sentry_sdk
   sentry_sdk.init("your-sentry-dsn")
   
   Capture errors automatically + get alerts

2. DATADOG MONITORING:
   pip install datadog
   
   from datadog import initialize, api
   options = {'api_key': 'xxx', 'app_key': 'xxx'}
   initialize(**options)
   
   Track custom metrics and dashboards

3. PROMETHEUS METRICS:
   pip install prometheus-client
   
   from prometheus_client import Counter, Histogram
   
   message_counter = Counter('whatsapp_messages_total', 'Total messages')
   response_time = Histogram('response_time_seconds', 'Response time')

4. STRUCTURED LOGGING:
   pip install python-json-logger
   
   import logging
   from pythonjsonlogger import jsonlogger
   
   handler = logging.StreamHandler()
   formatter = jsonlogger.JsonFormatter()
   handler.setFormatter(formatter)
   logger.addHandler(handler)

5. KEY METRICS TO TRACK:
   - Messages processed per day
   - Average response time
   - Error rate
   - API costs
   - Cache hit rate
   - Concurrent users
"""

# ============================================================
# PRINT GUIDES
# ============================================================

if __name__ == "__main__":
    import os
    
    print("=" * 70)
    print("🚀 ADVANCED CONFIGURATION & DEPLOYMENT GUIDE")
    print("=" * 70)
    
    options = {
        "1": ("Heroku Deployment", HEROKU_SETUP),
        "2": ("AWS Lambda (Serverless)", AWS_LAMBDA_SETUP),
        "3": ("Docker Deployment", DOCKER_COMPOSE),
        "4": ("Performance Optimization", PERFORMANCE_TIPS),
        "5": ("Advanced Scraping", ADVANCED_SCRAPING),
        "6": ("Security Best Practices", SECURITY_GUIDE),
        "7": ("Scaling Strategies", SCALING_GUIDE),
        "8": ("Monitoring & Observability", MONITORING_SETUP),
    }
    
    print("\nSelect a guide to view:")
    for key, (name, _) in options.items():
        print(f"{key}. {name}")
    
    choice = input("\nEnter your choice (1-8): ").strip()
    
    if choice in options:
        name, content = options[choice]
        print(f"\n{'=' * 70}")
        print(f"📖 {name}")
        print(f"{'=' * 70}\n")
        print(content)
    else:
        print("\n❌ Invalid choice. Please run again and select 1-8.")
