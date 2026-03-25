import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from database.dbconn import sqlExecute

load_dotenv()

key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool (Function Calling Schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_lead_to_db",
            "description": "Call this function ONLY when you have collected all 4 required pieces of information from the user. IMPORTANT: All text data must be translated to English before calling this function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The client's full name. MUST be translated to English (e.g., 'Иван' -> 'Ivan')."},
                    "contact_info": {"type": "string", "description": "This is where the customer's contact information is stored. It could be a Telegram ID, phone number, email address, Instagram username, or Facebook username."},
                    "contact_type": {"type": "string", "description": "This field stores a type of contact information—just a single word, such as Telegram, Instagram, phone number, email, Facebook username etc."},
                    "service": {"type": "string", "description": "The type of service they want, strictly followed by a short project description in parentheses, e.g., 'website (online bicycle store)' or 'telegram bot (crypto exchange)'. If the user did not provide any specific details, just leave the parentheses empty or omit them."},
                    "budget": {"type": "integer", "description": "The client's budget strictly in USD (integer). If the user provided a budget in another currency (e.g., EUR, RUB, UAH), you MUST calculate the approximate equivalent in USD before saving."},
                    "farewell_message": {"type": "string", "description": "Generate a polite final goodbye message FOR THE CLIENT in the exact language they used in the chat. Thank them and confirm that a manager will contact them."},

                },
                "required": ["name", "contact_info", "contact_type", "service", "budget", "farewell_message"]
            }
        }
    }
]

def process_chat(messages):
    """
    Takes the conversation history, sends it to OpenAI, 
    and checks if the AI decided to save the lead.
    """
    # System prompt defines the AI's persona and strict rules
    system_prompt = {
        "role": "system",
        "content": """
        You are Alex, a polite and professional AI Sales Manager at 'A-Simero Digital Agency'.
        Your goal is to naturally collect 4 pieces of information from the client: 
        1. Name 
        2. Preferred contact method and details (phone, email, Telegram, Instagram)
        3. Desired service (website, AI automation, app, etc.)
        4. Budget.
        
        LANGUAGE RULES:
        - ALWAYS communicate with the user in the language they are using (e.g., if they speak Russian, reply in Russian; if German, reply in German).
        - However, when you finally call the 'save_lead_to_db' function, you MUST translate the Name and Service into ENGLISH.
        - IMPORTANT: You are a MALE. When speaking languages with grammatical gender (like Russian, Spanish, French, etc.), ALWAYS use masculine verb forms and adjectives when referring to yourself (e.g., in Russian say "я понял", NOT "я поняла").
        
        BEHAVIOR RULES:
        - Ask for missing information conversationally, ONE or TWO questions at a time. Do not overwhelm the user.
        - Be friendly and concise.
        - Once you have ALL 4 pieces of information, call the 'save_lead_to_db' function.
        - Always clarify the budget in USD. If the user names a budget in another currency, politely let them know the approximate USD equivalent you are recording.
        - When discussing the desired service, politely ask the user for a brief 1-2 sentence description of their project (e.g., 'What kind of business is this website for?'). This helps our team prepare for the call.
        - If the user provides a handle (e.g., '@alex' or 'myname123'), NEVER guess the platform. Politely ask them to clarify if it is Telegram, Instagram, or something else.
        """
    }
    
    # Prepare the conversation history
    conversation = [system_prompt] + messages
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        tools=tools,
        tool_choice="auto",
        temperature=0.3
    )
    
    response_message = response.choices[0].message
    
    # Check if AI triggered our Function Call
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        
        if tool_call.function.name == "save_lead_to_db":
            # Extract the JSON data collected by the AI
            lead_data = json.loads(tool_call.function.arguments)
            
            name = lead_data.get("name")
            contact_info = lead_data.get("contact_info")
            contact_type = lead_data.get("contact_type")
            farewell_message = lead_data.get("farewell_message")
            service = lead_data.get("service")
            budget = lead_data.get("budget")
            
            # SAVE TO DATABASE!
            sql = f"INSERT INTO Leads (name, contact_info, contact_type, service, budget) VALUES ('{name}', '{contact_info}', '{contact_type}', '{service}', {budget})"
            try:
                sqlExecute(sql)
                # Final message from our Python backend (not the AI)
                return farewell_message
            except Exception as e:
                return "Oops, there was a technical error saving your data. Please try again later."
    
    # If no function was called, just return the AI's normal text response
    return response_message.content
