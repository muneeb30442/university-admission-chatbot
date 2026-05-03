"""
Out-of-Context Query Detector Module
Detects queries that are unrelated to university admissions and triggers
an apology message instead of attempting to answer.
"""

import json
from typing import Tuple


class OutOfContextDetector:
    """Detects queries that are out of scope for university admissions chatbot."""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        """
        Initialize the out-of-context detector.
        
        Args:
            knowledge_base_path: Path to knowledge base JSON file
        """
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()
        
        # Keywords and phrases related to university admissions
        self.admission_keywords = {
            'admission', 'apply', 'application', 'admit', 'enrolled', 'degree',
            'tuition', 'fee', 'scholarship', 'financial', 'aid', 'gpa', 'sat',
            'act', 'toefl', 'ielts', 'deadline', 'requirement', 'document',
            'major', 'program', 'course', 'major', 'student', 'campus', 'dorm',
            'hostel', 'facility', 'facility', 'transfer', 'international',
            'domestic', 'transcript', 'grade', 'university', 'college', 'school',
            'admissions', 'enrolling', 'enroll', 'student life', 'housing',
            'accommodation', 'registrar', 'semester', 'trimester', 'academic',
            'curriculum', 'syllabus', 'merit', 'need-based', 'loan', 'grant',
            'scholarship eligibility', 'test score', 'prerequisite', 'credit',
            'transcript', 'recommendation letter', 'essay', 'interview',
            'application portal', 'application fee', 'application status'
        }
        
        # Common out-of-context topics
        self.out_of_context_keywords = {
            'weather', 'pizza', 'movie', 'game', 'sports', 'cooking', 'recipe',
            'music', 'song', 'joke', 'funny', 'laugh', 'animal', 'pet', 'dog',
            'cat', 'travel', 'vacation', 'hotel', 'flight', 'car', 'mechanic',
            'politics', 'election', 'president', 'government', 'law', 'legal',
            'doctor', 'medical', 'health', 'disease', 'medicine', 'pharmacy',
            'restaurant', 'food', 'drink', 'coffee', 'tea', 'alcohol', 'wine',
            'dating', 'relationship', 'love', 'marriage', 'divorce', 'romance',
            'cryptocurrency', 'bitcoin', 'stock', 'investment', 'forex',
            'hacking', 'malware', 'virus', 'porn', 'adult', 'explicit',
            'bomb', 'gun', 'weapon', 'illegal', 'crime', 'criminal',
            'python code', 'javascript', 'programming', 'code', 'debug',
            'sql', 'database', 'technical', 'software', 'hardware'
        }
    
    def _load_knowledge_base(self) -> dict:
        """Load knowledge base from JSON file."""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def is_out_of_context(self, user_input: str, confidence_threshold: float = 0.3) -> Tuple[bool, str]:
        """
        Detect if a query is out of context (unrelated to university admissions).
        
        Args:
            user_input: The user's input text
            confidence_threshold: Minimum confidence score to consider in-context
        
        Returns:
            Tuple of (is_out_of_context: bool, reason: str)
        """
        user_input_lower = user_input.lower()
        
        # Check for very short inputs (likely just greeting or acknowledgment)
        words = user_input_lower.split()
        if len(words) == 0:
            return False, "empty_input"
        
        # Count admission-related keywords
        admission_count = sum(1 for keyword in self.admission_keywords 
                            if keyword in user_input_lower)
        
        # Count out-of-context keywords
        out_of_context_count = sum(1 for keyword in self.out_of_context_keywords 
                                   if keyword in user_input_lower)
        
        total_keywords_found = admission_count + out_of_context_count
        
        # If no relevant keywords found at all
        if total_keywords_found == 0:
            return True, "no_relevant_keywords"
        
        # Calculate relevance score
        if total_keywords_found > 0:
            relevance_score = admission_count / total_keywords_found
        else:
            relevance_score = 0
        
        # If more out-of-context keywords than admission keywords
        if out_of_context_count > admission_count:
            return True, "out_of_context_keywords"
        
        # If very low relevance score
        if relevance_score < confidence_threshold and total_keywords_found > 0:
            return True, "low_relevance_score"
        
        return False, "in_context"
    
    def get_apology_message(self) -> str:
        """
        Get the apology message for out-of-context queries.
        
        Returns:
            The apology message string
        """
        try:
            messages = self.knowledge_base.get("messages", {})
            apology = messages.get("out_of_context_apology", 
                                  "I appreciate your question, but I'm specifically designed to help with university admissions inquiries. "
                                  "Could you please ask me about application deadlines, eligibility requirements, tuition, programs, "
                                  "campus facilities, or other admission-related topics? I'm here to assist!")
            return apology
        except:
            return "I apologize, but I can only assist with university admission-related questions. Please feel free to ask about applications, requirements, programs, or campus life!"
