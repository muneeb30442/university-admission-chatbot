"""
NLP Similarity Module
This module uses TF-IDF vectorization and cosine similarity to find
the most similar pattern to user input and retrieve the corresponding response.
"""

import json
from typing import Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class NLPSimilarityMatcher:
    """NLP-based matcher using TF-IDF and cosine similarity."""
    
    def __init__(self, intents_path: str, knowledge_base_path: str):
        """
        Initialize the NLP similarity matcher.
        
        Args:
            intents_path: Path to intents JSON file
            knowledge_base_path: Path to knowledge base JSON file
        """
        self.intents_path = intents_path
        self.knowledge_base_path = knowledge_base_path
        self.intents = self._load_intents()
        self.knowledge_base = self._load_knowledge_base()
        
        # Store patterns and intents for similarity matching
        self.patterns = []
        self.pattern_to_intent = {}
        self.intent_to_responses = {}
        
        # TF-IDF vectorizer and pattern vectors
        self.vectorizer = None
        self.pattern_vectors = None
        
        # Build the similarity matcher
        self._build_matcher()
    
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
    
    def _build_matcher(self) -> None:
        """Build TF-IDF vectors for all patterns."""
        for intent in self.intents.get("intents", []):
            intent_name = intent.get("intent")
            patterns = intent.get("patterns", [])
            responses = intent.get("responses", [])
            
            self.intent_to_responses[intent_name] = responses
            
            for pattern in patterns:
                self.patterns.append(pattern)
                self.pattern_to_intent[pattern] = intent_name
        
        if not self.patterns:
            print("Warning: No patterns available for similarity matching")
            return
        
        # Fit TF-IDF vectorizer on all patterns
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=100,
            ngram_range=(1, 2)
        )
        
        self.pattern_vectors = self.vectorizer.fit_transform(self.patterns)
    
    def find_similar(self, user_input: str, top_k: int = 1) -> Tuple[Optional[str], Optional[str], float]:
        """
        Find the most similar pattern to user input using cosine similarity.
        
        Args:
            user_input: The user's input text
            top_k: Number of top matches to consider
        
        Returns:
            Tuple of (intent, response, similarity_score)
        """
        if self.vectorizer is None or self.pattern_vectors is None:
            return None, "Similarity matcher not initialized.", 0.0
        
        if not self.patterns:
            return None, "No patterns available for matching.", 0.0
        
        try:
            # Vectorize user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate cosine similarity with all patterns
            similarities = cosine_similarity(user_vector, self.pattern_vectors)[0]
            
            # Get top matches
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Get the best match
            best_index = top_indices[0]
            best_similarity = float(similarities[best_index])
            
            # Get the matched pattern and intent
            best_pattern = self.patterns[best_index]
            matched_intent = self.pattern_to_intent[best_pattern]
            
            # Get response
            response = self._get_response(matched_intent)
            
            return matched_intent, response, best_similarity
        
        except Exception as e:
            return None, f"Error during similarity matching: {str(e)}", 0.0
    
    def _get_response(self, intent: str) -> str:
        """
        Get response for the matched intent.
        
        Args:
            intent: The matched intent name
        
        Returns:
            The response text
        """
        responses = self.intent_to_responses.get(intent, [])
        
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
    
    def get_top_matches(self, user_input: str, top_k: int = 3) -> list:
        """
        Get top-k similar patterns with their similarity scores.
        
        Args:
            user_input: The user's input text
            top_k: Number of top matches to return
        
        Returns:
            List of tuples (pattern, intent, similarity_score)
        """
        if self.vectorizer is None or self.pattern_vectors is None:
            return []
        
        try:
            # Vectorize user input
            user_vector = self.vectorizer.transform([user_input])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(user_vector, self.pattern_vectors)[0]
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Build results
            results = []
            for idx in top_indices:
                pattern = self.patterns[idx]
                intent = self.pattern_to_intent[pattern]
                score = float(similarities[idx])
                results.append((pattern, intent, score))
            
            return results
        
        except Exception as e:
            print(f"Error getting top matches: {str(e)}")
            return []
