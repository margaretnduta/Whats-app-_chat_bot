"""
Utility Functions Module
Contains helper functions for OpenAI API calls, message formatting, and logging
"""

import openai
from config import Config


# Initialize OpenAI API
openai.api_key = Config.OPENAI_API_KEY


class AIAssistant:
    """
    Handles communication with OpenAI's ChatGPT API
    """
    
    @staticmethod
    def generate_response(user_message, context_data):
        """
        Generate a response using ChatGPT with provided context
        
        Args:
            user_message: The user's question/message
            context_data: Scraped website content to use as context
        
        Returns:
            str: Generated response from ChatGPT
        """
        try:
            # Prepare the system prompt
            system_prompt = f"""You are a helpful WhatsApp chatbot assistant. 
Your role is to answer questions based ONLY on the following website information:

{context_data[:5000]}  # Limit context to first 5000 characters to avoid token limits

Important guidelines:
1. Only answer based on the provided website information
2. If the information is not in the provided context, politely say you don't have that information
3. Keep responses concise and mobile-friendly
4. Use clear formatting with bullet points and bold text when helpful
5. Be friendly and professional
"""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for cost-effectiveness
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=300,  # Keep responses concise for WhatsApp
                timeout=10,
            )
            
            return response["choices"][0]["message"]["content"]
        
        except openai.error.APIError as e:
            print(f"❌ OpenAI API Error: {e}")
            return "Sorry, I encountered an error processing your request. Please try again."
        
        except openai.error.AuthenticationError:
            print("❌ OpenAI Authentication Error: Invalid API key")
            return "Configuration error with the AI service. Please contact support."
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return "Sorry, something went wrong. Please try again later."


def format_whatsapp_message(text):
    """
    Format text for WhatsApp (supports markdown-like formatting)
    
    Args:
        text: Plain text to format
    
    Returns:
        str: WhatsApp-friendly formatted text
    """
    # WhatsApp supports *bold*, _italic_, and ~strikethrough~
    # The text from ChatGPT might already be formatted, so just ensure it's mobile-friendly
    
    # Limit line length for mobile screens
    max_line_length = 60
    lines = text.split("\n")
    formatted_lines = []
    
    for line in lines:
        if len(line) > max_line_length:
            # Break long lines
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 > max_line_length:
                    if current_line:
                        formatted_lines.append(current_line)
                    current_line = word
                else:
                    current_line = f"{current_line} {word}" if current_line else word
            if current_line:
                formatted_lines.append(current_line)
        else:
            formatted_lines.append(line)
    
    return "\n".join(formatted_lines)


def create_welcome_message():
    """
    Create a welcome message for new users
    
    Returns:
        str: Welcome message
    """
    return """👋 *Welcome to Click2Skill Assistant!*

I'm here to help you with information about Click2Skill. I can answer your questions about:
• Courses and training programs
• Skills and certifications
• Learning paths and resources
• And more!

Just ask me anything about Click2Skill, and I'll do my best to help! 📚

_Please note: I can only answer questions based on Click2Skill's information._"""


def create_thinking_message():
    """
    Create a "thinking" message for when the bot is processing
    
    Returns:
        str: Thinking message
    """
    return "🤔 Processing your request... Please wait a moment."


def log_message(sender, message, response):
    """
    Log conversation for debugging and analytics
    
    Args:
        sender: Phone number of the sender
        message: User's message
        response: Bot's response
    """
    print(f"\n📱 Message from {sender}:")
    print(f"   User: {message}")
    print(f"   Bot: {response[:100]}...")  # Print first 100 chars


def is_greeting(message):
    """
    Check if a message is a greeting
    
    Args:
        message: User message
    
    Returns:
        bool: True if greeting detected
    """
    greetings = ["hi", "hello", "hey", "start", "help"]
    message_lower = message.lower().strip()
    return any(message_lower.startswith(g) for g in greetings)
