"""
Rule-Based Keyword Matching Module
This module implements a simple rule-based response generation system
that matches user input against keywords defined in the intents file.
"""

import json
from typing import Tuple, Optional


class RuleBasedMatcher:
    """Rule-based chatbot matcher using keyword matching."""
    
    def __init__(self, intents_path: str, knowledge_base_path: str):
        """
        Initialize the rule-based matcher.
        
        Args:
            intents_path: Path to intents JSON file
            knowledge_base_path: Path to knowledge base JSON file
        """
        self.intents_path = intents_path
        self.knowledge_base_path = knowledge_base_path
        self.intents = self._load_intents()
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_intents(self) -> dict:
        """Load intents from JSON file."""
        try:
            with open(self.intents_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Intents file not found at {self.intents_path}")
            return {"intents": []}
    
    def _load_knowledge_base(self) -> dict:
        """Load knowledge base from JSON file."""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Knowledge base file not found at {self.knowledge_base_path}")
            return {}
    
    def match_keywords(self, user_input: str) -> Tuple[str, Optional[str], float]:
        """
        Match user input against keywords in intents.
        
        Args:
            user_input: The user's input text
        
        Returns:
            Tuple of (intent, response, confidence_score)
        """
        user_input_lower = user_input.lower()
        best_match_intent = None
        best_response = None
        best_score = 0.0
        
        for intent in self.intents.get("intents", []):
            keywords = intent.get("keywords", [])
            
            # Count matching keywords
            matching_keywords = sum(
                1 for keyword in keywords 
                if keyword in user_input_lower
            )
            
            if matching_keywords > 0:
                # Calculate confidence score based on keyword matches
                confidence = matching_keywords / len(keywords) if keywords else 0
                
                if confidence > best_score:
                    best_score = confidence
                    best_match_intent = intent.get("intent")
                    best_response = self._get_response(intent)
        
        # Return a minimum confidence threshold
        if best_score >= 0.3:  # At least 30% keyword match
            return best_match_intent, best_response, best_score
        
        return None, "I'm not sure I understand. Could you rephrase your question?", 0.0
    
    def _get_response(self, intent: dict) -> str:
        """
        Get response from knowledge base using the intent's response reference.
        
        Args:
            intent: The matched intent dictionary
        
        Returns:
            The response text
        """
        responses = intent.get("responses", [])
        
        if not responses:
            return "I don't have information about this topic."
        
        # Get the first response
        response_ref = responses[0]
        
        # If response is a direct text response
        if not response_ref.startswith("knowledge_base"):
            return response_ref
        
        # Parse knowledge base reference (e.g., "knowledge_base.admission_info.deadline")
        try:
            parts = response_ref.split(".")
            if parts[0] == "knowledge_base":
                data = self.knowledge_base
                for part in parts[1:]:
                    data = data[part]
                return str(data)
        except (KeyError, TypeError, IndexError):
            pass
        
        return "I don't have information about this topic."
    
    def get_all_intents(self) -> list:
        """Get list of all available intents."""
        return [intent.get("intent") for intent in self.intents.get("intents", [])]
