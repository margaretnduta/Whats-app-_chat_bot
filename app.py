"""
WhatsApp Chatbot - Main Application
Integrates Flask, Twilio WhatsApp API, and OpenAI ChatGPT
"""

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from config import Config
from scraper import get_scraped_content, get_scraper
from utils import (
    AIAssistant,
    format_whatsapp_message,
    create_welcome_message,
    create_thinking_message,
    log_message,
    is_greeting,
)


# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Initialize Twilio client
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

# Global variable to track message processing
user_states = {}  # To track conversations if needed


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """
    Webhook endpoint for Twilio WhatsApp messages
    This is where Twilio sends incoming messages
    
    Endpoint: POST /whatsapp
    
    How to set up in Twilio Console:
    1. Go to Twilio Console > Messaging > Services
    2. Select your WhatsApp sandbox or number
    3. Set the Webhook URL to: https://your-domain.com/whatsapp
    4. Set the method to POST
    5. Test with 'join [keyword]' in WhatsApp to opt-in to the sandbox
    """
    
    try:
        # Extract incoming message data
        incoming_msg = request.form.get("Body", "").strip()
        sender_phone = request.form.get("From", "")
        
        print(f"\n📱 Incoming message from {sender_phone}: {incoming_msg}")
        
        # Check for empty messages
        if not incoming_msg:
            return _send_whatsapp_message(sender_phone, "Please send a message.")
        
        # Handle greeting/help requests
        if is_greeting(incoming_msg):
            welcome_msg = create_welcome_message()
            return _send_whatsapp_message(sender_phone, welcome_msg)
        
        # Send "thinking" message for long processing
        thinking_msg = create_thinking_message()
        _send_whatsapp_message(sender_phone, thinking_msg)
        
        # Get scraped website content
        website_content = get_scraped_content()
        
        if not website_content:
            error_msg = "⚠️  Sorry, I couldn't fetch the website information right now. Please try again later."
            return _send_whatsapp_message(sender_phone, error_msg)
        
        # Get relevant context from scraped data
        scraper = get_scraper()
        relevant_context = scraper.get_relevant_context(incoming_msg, website_content)
        
        # Generate AI response
        ai_response = AIAssistant.generate_response(incoming_msg, relevant_context)
        
        # Format and send response
        formatted_response = format_whatsapp_message(ai_response)
        
        # Log the interaction
        log_message(sender_phone, incoming_msg, formatted_response)
        
        # Send the response
        return _send_whatsapp_message(sender_phone, formatted_response)
    
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        error_response = "Sorry, I encountered an error processing your message. Please try again."
        return _send_whatsapp_message(sender_phone, error_response)


def _send_whatsapp_message(to_number, message_body):
    """
    Send a WhatsApp message using Twilio
    
    Args:
        to_number: Recipient's WhatsApp number (in Twilio format)
        message_body: Message content to send
    
    Returns:
        str: XML response to Twilio
    """
    try:
        twilio_client.messages.create(
            from_=f"whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}",
            to=to_number,
            body=message_body,
        )
        print(f"✅ Message sent to {to_number}")
    except Exception as e:
        print(f"❌ Error sending message: {e}")
    
    # Return empty TwiML response
    resp = MessagingResponse()
    return str(resp)


@app.route("/status", methods=["GET"])
def status():
    """
    Health check endpoint to verify the bot is running
    Useful for monitoring and debugging
    
    Usage: GET /status
    """
    return {
        "status": "✅ Bot is running",
        "version": "1.0",
        "twilio_connected": bool(Config.TWILIO_ACCOUNT_SID),
        "openai_connected": bool(Config.OPENAI_API_KEY),
        "website": Config.TARGET_WEBSITE,
    }, 200


@app.route("/refresh-cache", methods=["POST"])
def refresh_cache():
    """
    Manually trigger a cache refresh (useful for testing)
    
    Usage: POST /refresh-cache
    """
    try:
        scraper = get_scraper()
        content = scraper.scrape_website(force_refresh=True)
        return {
            "status": "✅ Cache refreshed",
            "content_length": len(content),
        }, 200
    except Exception as e:
        return {"status": "❌ Error", "error": str(e)}, 500


@app.route("/", methods=["GET"])
def index():
    """
    Simple root endpoint
    """
    return """
    <h1>🤖 WhatsApp Chatbot is Running!</h1>
    <p>Send WhatsApp messages to your Twilio WhatsApp number to start chatting.</p>
    <h2>Endpoints:</h2>
    <ul>
        <li><strong>POST /whatsapp</strong> - Webhook for incoming WhatsApp messages (configured in Twilio)</li>
        <li><strong>GET /status</strong> - Health check status</li>
        <li><strong>POST /refresh-cache</strong> - Manually refresh cached website data</li>
    </ul>
    <h2>Setup Instructions:</h2>
    <ol>
        <li>Create a .env file with your Twilio and OpenAI credentials</li>
        <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
        <li>Run the app: <code>python app.py</code></li>
        <li>Use ngrok to expose your local server: <code>ngrok http 5000</code></li>
        <li>In Twilio Console, set the Webhook URL to: <code>https://your-ngrok-url.ngrok.io/whatsapp</code></li>
        <li>Opt-in to the WhatsApp sandbox by sending: <code>join [keyword]</code></li>
        <li>Start chatting!</li>
    </ol>
    """, 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {"error": "Endpoint not found"}, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    print(f"❌ Server error: {error}")
    return {"error": "Internal server error"}, 500


if __name__ == "__main__":
    # Validate configuration before starting
    try:
        Config.validate_config()
        print("✅ Configuration validated successfully")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set up your .env file with all required variables.")
        exit(1)
    
    # Pre-load scraped data on startup
    print("\n🔄 Pre-loading website data on startup...")
    try:
        get_scraped_content()
        print("✅ Website data loaded successfully\n")
    except Exception as e:
        print(f"⚠️  Warning: Could not pre-load data: {e}\n")
    
    # Start Flask server
    print("🚀 Starting WhatsApp Chatbot Server...")
    print("📱 Webhook endpoint: http://localhost:5000/whatsapp")
    print("🔍 Status endpoint: http://localhost:5000/status")
    print("\n💡 Tip: Use ngrok to expose your local server for Twilio webhooks!")
    print("   Command: ngrok http 5000\n")
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=Config.FLASK_ENV == "development",
    )
