from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import google.generativeai as genai
import os

class ActionGeminiResponse(Action):
    def name(self) -> Text:
        return "action_gemini_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user message
        user_message = tracker.latest_message.get('text')
        
        # Configure Gemini (same as your JS code)
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Create the prompt (same as your JS code)
        prompt = f"""The following is a conversation with an AI assistant built for a personal finance tracker.
        The assistant gives short, concise answers (no more than 250 characters). 
        The assistant can help the user with financial guidance, advice, money management tips, budgeting rules, and general finance-related questions. It is helpful, creative, clever, and very friendly. The assistant also keeps small talk light and engaging, making the user feel comfortable while discussing finance topics.
        The assistant should provide advice, tips, or general knowledge about finance, budgeting, saving, and spending.
        The assistant should respond in a friendly, approachable, and conversational tone.
        If a user question requires database access or real-time personal finance data, the assistant will not handle it; only general advice and guidance are in scope for this prompt.
        The assistant can explain complex finance concepts in simple terms, provide best practices, and offer actionable tips where appropriate.
        
        User input: {user_message}
        Suggested AI Response:"""
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            dispatcher.utter_message(text=response.text)
            
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I'm having trouble right now. Please try again.")
            
        return []