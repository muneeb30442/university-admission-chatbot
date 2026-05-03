"""
University Admission Chatbot Orchestrator
Combines three response generation methods: rule-based, intent classification, and NLP similarity.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from modules.rule_based import RuleBasedMatcher
from modules.intent_classifier import IntentClassifier
from modules.nlp_similarity import NLPSimilarityMatcher
from modules.out_of_context_detector import OutOfContextDetector


class UniversityAdmissionChatbot:
    """Main chatbot orchestrator."""
    
    def __init__(self, intents_path: str = "intents.json", 
                 knowledge_base_path: str = "knowledge_base.json",
                 logs_dir: str = "logs"):
        """
        Initialize the chatbot with all three response modules.
        
        Args:
            intents_path: Path to intents JSON file
            knowledge_base_path: Path to knowledge base JSON file
            logs_dir: Directory for logging
        """
        self.intents_path = intents_path
        self.knowledge_base_path = knowledge_base_path
        self.logs_dir = logs_dir
        
        # Initialize the three response generation modules
        self.rule_based = RuleBasedMatcher(intents_path, knowledge_base_path)
        self.intent_classifier = IntentClassifier(intents_path, knowledge_base_path)
        self.nlp_similarity = NLPSimilarityMatcher(intents_path, knowledge_base_path)
        
        # Initialize out-of-context detector
        self.out_of_context_detector = OutOfContextDetector(knowledge_base_path)
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Method weights for ensemble (can be adjusted)
        self.method_weights = {
            'rule_based': 0.2,
            'intent_classifier': 0.4,
            'nlp_similarity': 0.4
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging system."""
        # Create logs directory if it doesn't exist
        Path(self.logs_dir).mkdir(exist_ok=True)
        
        # Configure logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = Path(self.logs_dir) / f"chatbot_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        return logger
    
    def process_query(self, user_input: str, method: str = "ensemble") -> Dict:
        """
        Process user query using one or multiple methods.
        
        Args:
            user_input: The user's input text
            method: 'rule_based', 'intent_classifier', 'nlp_similarity', or 'ensemble'
        
        Returns:
            Dictionary with response and metadata
        """
        # Log the user query
        self.logger.info(f"User Query: {user_input}")
        
        result = {
            'user_input': user_input,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'responses': {},
            'is_out_of_context': False,
            'out_of_context_reason': None
        }
        
        # Check if query is out of context
        is_out_of_context, reason = self.out_of_context_detector.is_out_of_context(user_input)
        
        if is_out_of_context:
            result['is_out_of_context'] = True
            result['out_of_context_reason'] = reason
            result['final_response'] = self.out_of_context_detector.get_apology_message()
            result['confidence'] = 1.0
            result['method'] = 'out_of_context_detection'
            
            # Log the out-of-context response
            self.logger.info(f"Out-of-Context Query Detected (Reason: {reason}). Apology Message Sent.")
            
            return result
        
        if method == "rule_based":
            result['responses']['rule_based'] = self._get_rule_based_response(user_input)
            result['final_response'] = result['responses']['rule_based']['response']
            result['confidence'] = result['responses']['rule_based']['confidence']
        
        elif method == "intent_classifier":
            result['responses']['intent_classifier'] = self._get_intent_classifier_response(user_input)
            result['final_response'] = result['responses']['intent_classifier']['response']
            result['confidence'] = result['responses']['intent_classifier']['confidence']
        
        elif method == "nlp_similarity":
            result['responses']['nlp_similarity'] = self._get_nlp_similarity_response(user_input)
            result['final_response'] = result['responses']['nlp_similarity']['response']
            result['confidence'] = result['responses']['nlp_similarity']['confidence']
        
        elif method == "ensemble":
            result['responses']['rule_based'] = self._get_rule_based_response(user_input)
            result['responses']['intent_classifier'] = self._get_intent_classifier_response(user_input)
            result['responses']['nlp_similarity'] = self._get_nlp_similarity_response(user_input)
            
            # Get ensemble result
            ensemble_result = self._ensemble_responses(result['responses'])
            result['final_response'] = ensemble_result['response']
            result['confidence'] = ensemble_result['confidence']
            result['ensemble_method'] = ensemble_result['best_method']
        
        # Log the response
        self.logger.info(f"Response: {result['final_response']} (Confidence: {result['confidence']:.2f})")
        
        return result
    
    def _get_rule_based_response(self, user_input: str) -> Dict:
        """Get response from rule-based module."""
        intent, response, confidence = self.rule_based.match_keywords(user_input)
        return {
            'intent': intent,
            'response': response,
            'confidence': confidence
        }
    
    def _get_intent_classifier_response(self, user_input: str) -> Dict:
        """Get response from intent classifier module."""
        intent, response, confidence = self.intent_classifier.classify(user_input)
        return {
            'intent': intent,
            'response': response,
            'confidence': confidence
        }
    
    def _get_nlp_similarity_response(self, user_input: str) -> Dict:
        """Get response from NLP similarity module."""
        intent, response, confidence = self.nlp_similarity.find_similar(user_input)
        return {
            'intent': intent,
            'response': response,
            'confidence': confidence
        }
    
    def _ensemble_responses(self, responses: Dict) -> Dict:
        """
        Combine responses from all three methods using weighted average.
        
        Args:
            responses: Dictionary with responses from all methods
        
        Returns:
            Dictionary with ensemble response
        """
        # Calculate weighted confidence
        total_weight = 0
        weighted_confidence = 0
        best_response = None
        best_confidence = 0
        best_method = None
        
        for method, response_data in responses.items():
            weight = self.method_weights.get(method, 0.33)
            confidence = response_data.get('confidence', 0)
            
            weighted_confidence += confidence * weight
            total_weight += weight
            
            # Track best individual response
            if confidence > best_confidence:
                best_confidence = confidence
                best_response = response_data['response']
                best_method = method
        
        # Normalize weighted confidence
        ensemble_confidence = weighted_confidence / total_weight if total_weight > 0 else 0
        
        return {
            'response': best_response,
            'confidence': ensemble_confidence,
            'best_method': best_method
        }
    
    def get_conversation_log(self) -> List[Dict]:
        """
        Get conversation history from log file.
        
        Returns:
            List of conversation entries
        """
        log_file = Path(self.logs_dir) / f"chatbot_{datetime.now().strftime('%Y%m%d')}.log"
        
        if not log_file.exists():
            return []
        
        conversations = []
        with open(log_file, 'r') as f:
            for line in f:
                if 'User Query:' in line or 'Response:' in line:
                    conversations.append(line.strip())
        
        return conversations
    
    def save_interaction(self, user_input: str, response: str, method: str, 
                       confidence: float) -> None:
        """
        Save interaction details to JSON log file.
        
        Args:
            user_input: User's input
            response: Chatbot's response
            method: Response method used
            confidence: Confidence score
        """
        interaction_log_file = Path(self.logs_dir) / "interactions.jsonl"
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'method': method,
            'confidence': confidence
        }
        
        # Append to JSONL file
        with open(interaction_log_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')
    
    def get_statistics(self) -> Dict:
        """
        Get chatbot statistics from interactions.
        
        Returns:
            Dictionary with statistics
        """
        interaction_log_file = Path(self.logs_dir) / "interactions.jsonl"
        
        if not interaction_log_file.exists():
            return {
                'total_interactions': 0,
                'average_confidence': 0,
                'method_distribution': {},
                'top_intents': []
            }
        
        interactions = []
        with open(interaction_log_file, 'r') as f:
            for line in f:
                if line.strip():
                    interactions.append(json.loads(line))
        
        if not interactions:
            return {
                'total_interactions': 0,
                'average_confidence': 0,
                'method_distribution': {},
                'top_intents': []
            }
        
        # Calculate statistics
        total = len(interactions)
        avg_confidence = sum(i.get('confidence', 0) for i in interactions) / total
        
        # Method distribution
        method_counts = {}
        for interaction in interactions:
            method = interaction.get('method', 'unknown')
            method_counts[method] = method_counts.get(method, 0) + 1
        
        return {
            'total_interactions': total,
            'average_confidence': round(avg_confidence, 3),
            'method_distribution': method_counts,
            'last_interaction': interactions[-1] if interactions else None
        }
