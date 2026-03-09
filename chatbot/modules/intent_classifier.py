"""
Intent Classification Module
This module uses scikit-learn to classify user input into predefined intents
using TF-IDF vectorization and logistic regression or Naive Bayes.
"""

import json
import pickle
import numpy as np
from typing import Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class IntentClassifier:
    """Intent classifier using scikit-learn."""
    
    def __init__(self, intents_path: str, knowledge_base_path: str):
        """
        Initialize the intent classifier.
        
        Args:
            intents_path: Path to intents JSON file
            knowledge_base_path: Path to knowledge base JSON file
        """
        self.intents_path = intents_path
        self.knowledge_base_path = knowledge_base_path
        self.intents = self._load_intents()
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize the ML pipeline
        self.pipeline = None
        self.intent_labels = []
        self.intent_responses = {}
        
        # Train the classifier
        self._train_classifier()
    
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
    
    def _train_classifier(self) -> None:
        """Train the intent classifier on pattern data."""
        training_data = []
        labels = []
        
        for intent in self.intents.get("intents", []):
            intent_name = intent.get("intent")
            patterns = intent.get("patterns", [])
            responses = intent.get("responses", [])
            
            self.intent_labels.append(intent_name)
            self.intent_responses[intent_name] = responses
            
            for pattern in patterns:
                training_data.append(pattern)
                labels.append(intent_name)
        
        if not training_data:
            print("Warning: No training data available")
            return
        
        # Create and train the pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english', max_features=100)),
            ('classifier', MultinomialNB())
        ])
        
        self.pipeline.fit(training_data, labels)
    
    def classify(self, user_input: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Classify user input into an intent and get a response.
        
        Args:
            user_input: The user's input text
        
        Returns:
            Tuple of (intent, response, confidence_score)
        """
        if self.pipeline is None:
            return None, "Classifier not trained properly.", 0.0
        
        try:
            # Get intent prediction
            predicted_intent = self.pipeline.predict([user_input])[0]
            
            # Get confidence (probability) score
            probabilities = self.pipeline.predict_proba([user_input])[0]
            confidence = float(np.max(probabilities))
            
            # Get response
            response = self._get_response(predicted_intent)
            
            return predicted_intent, response, confidence
        
        except Exception as e:
            return None, f"Error during classification: {str(e)}", 0.0
    
    def _get_response(self, intent: str) -> str:
        """
        Get response for the predicted intent.
        
        Args:
            intent: The predicted intent name
        
        Returns:
            The response text
        """
        responses = self.intent_responses.get(intent, [])
        
        if not responses:
            return "I don't have information about this topic."
        
        response_ref = responses[0]
        
        # If response is direct text
        if not response_ref.startswith("knowledge_base"):
            return response_ref
        
        # Parse knowledge base reference
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
    
    def get_intent_distribution(self, user_input: str) -> dict:
        """
        Get probability distribution across all intents.
        
        Args:
            user_input: The user's input text
        
        Returns:
            Dictionary with intent names and probabilities
        """
        if self.pipeline is None:
            return {}
        
        try:
            probabilities = self.pipeline.predict_proba([user_input])[0]
            distribution = {}
            
            for intent, prob in zip(self.pipeline.classes_, probabilities):
                distribution[intent] = float(prob)
            
            return distribution
        except Exception as e:
            print(f"Error getting distribution: {str(e)}")
            return {}
