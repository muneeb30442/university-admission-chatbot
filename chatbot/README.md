# University Admission Chatbot

A comprehensive chatbot system for answering university admission-related questions using three different response generation methods: rule-based keyword matching, intent classification, and NLP similarity.

## Project Overview

This project implements a multi-method chatbot that combines three different approaches to understand and respond to user queries:

1. **Rule-Based Keyword Matching** - Simple but fast keyword-based matching
2. **Intent Classification** - Machine learning-based intent detection using scikit-learn
3. **NLP Similarity** - TF-IDF based semantic similarity matching
4. **Ensemble** - Combines all three methods for improved accuracy

## Project Structure

```
university-admission-chatbot/
│
├── app.py                      # Flask web application
├── chatbot.py                  # Main chatbot orchestrator
├── knowledge_base.json         # University admission knowledge base
├── intents.json               # Intent definitions and patterns
├── test_queries.json          # Test dataset for evaluation
├── test_chatbot.py            # Test evaluation script
├── requirements.txt           # Python dependencies
│
├── modules/
│   ├── rule_based.py          # Rule-based keyword matching module
│   ├── intent_classifier.py   # ML-based intent classification
│   └── nlp_similarity.py      # NLP similarity matching module
│
├── static/                    # Static files (CSS, JS, images)
│
├── templates/
│   └── index.html            # Web chat interface
│
├── logs/                      # Chat logs and interaction records
│   ├── chatbot_YYYYMMDD.log  # Daily chat logs
│   └── interactions.jsonl    # Detailed interaction records
│
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd university-admission-chatbot
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Web Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Select a chatbot method and start chatting:**
   - **Ensemble (Best)** - Recommended for most use cases
   - **Rule-Based** - Fast, keyword-based responses
   - **Intent Classifier** - ML-based classification
   - **NLP Similarity** - Semantic similarity matching

### Running Tests

1. **Execute the test evaluation script:**
   ```bash
   python test_chatbot.py
   ```

2. **The script will:**
   - Run all test queries against all methods
   - Display real-time results with accuracy metrics
   - Generate detailed reports by intent and category
   - Export results to `logs/test_results.json`

### Using the Chatbot Programmatically

```python
from chatbot import UniversityAdmissionChatbot

# Initialize the chatbot
chatbot = UniversityAdmissionChatbot(
    intents_path='intents.json',
    knowledge_base_path='knowledge_base.json',
    logs_dir='logs'
)

# Process a query using ensemble method
result = chatbot.process_query(
    "What is the application deadline?",
    method="ensemble"
)

print(f"Response: {result['final_response']}")
print(f"Confidence: {result['confidence']:.3f}")
print(f"Intent: {result['responses']['intent_classifier']['intent']}")

# Get statistics
stats = chatbot.get_statistics()
print(f"Total interactions: {stats['total_interactions']}")
print(f"Average confidence: {stats['average_confidence']}")
```

## API Endpoints

### Chat Endpoint
**POST** `/api/chat`

Request body:
```json
{
  "message": "What is the application deadline?",
  "method": "ensemble"
}
```

Response:
```json
{
  "status": "success",
  "response": "The regular admission deadline is March 15th...",
  "confidence": 0.95,
  "method": "ensemble",
  "intent": "application_deadline",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Get Available Methods
**GET** `/api/methods`

Returns list of available chatbot methods.

### Get Intents
**GET** `/api/intents`

Returns list of all available intents.

### Get Statistics
**GET** `/api/statistics`

Returns chatbot usage statistics.

### Test Endpoint
**GET** `/api/test`

Verifies API is running and chatbot is initialized.

## Response Generation Methods

### 1. Rule-Based Keyword Matching
- **File:** `modules/rule_based.py`
- **Method:** Matches user input against predefined keywords
- **Pros:** Fast, deterministic, no training required
- **Cons:** Limited flexibility, cannot handle synonyms well
- **Use case:** Quick initial responses, fast processing

### 2. Intent Classification
- **File:** `modules/intent_classifier.py`
- **Method:** Uses TF-IDF vectorization and Multinomial Naive Bayes
- **Pros:** Handles variations better, learns from data
- **Cons:** Requires training data, slower than rule-based
- **Use case:** Better accuracy with diverse queries

### 3. NLP Similarity Matching
- **File:** `modules/nlp_similarity.py`
- **Method:** TF-IDF vectorization with cosine similarity
- **Pros:** Semantic understanding, flexible pattern matching
- **Cons:** Slightly slower, requires vector computation
- **Use case:** Finding most similar patterns to user input

### 4. Ensemble Method
- **Combines** all three methods with weighted scores
- **Default weights:** Rule-based (0.2), Intent Classifier (0.4), NLP Similarity (0.4)
- **Result:** Best of all three methods with ensemble confidence

## Knowledge Base

The `knowledge_base.json` file contains:
- **admission_info**: Application deadlines, eligibility, documents, fees, etc.
- **contact_info**: Phone, email, office hours
- **faqs**: Frequently asked questions and answers

Modify this file to update the chatbot's knowledge about your institution.

## Intents Configuration

The `intents.json` file defines:
- **Intent name**: Unique identifier for the intent
- **Patterns**: Example user queries for this intent
- **Responses**: Response templates or knowledge base references
- **Keywords**: Keywords associated with the intent

Example intent:
```json
{
  "intent": "application_deadline",
  "patterns": [
    "When is the application deadline?",
    "What is the deadline for applying?",
    "By when do I need to apply?"
  ],
  "responses": ["knowledge_base.admission_info.application_deadline"],
  "keywords": ["deadline", "apply", "submission", "when"]
}
```

## Logging and Monitoring

### Chat Logs
- Daily logs stored in `logs/chatbot_YYYYMMDD.log`
- Contains user queries, responses, and timestamps

### Interaction Records
- Detailed records in `logs/interactions.jsonl`
- Each line is a JSON object with:
  - timestamp
  - user_input
  - response
  - method
  - confidence

### Statistics
- Access via `/api/statistics` endpoint
- Shows total interactions, average confidence, method distribution

## Testing

### Test Dataset
The `test_queries.json` file contains 40 test queries covering:
- Application process (deadline, documents, status)
- Requirements (eligibility, GPA, test scores)
- Costs (fees, tuition, financial aid)
- Program information (duration, majors, courses)
- Campus life (facilities, housing, activities)
- Special cases (transfers, international students)
- Support (contact information)

### Running Tests
```bash
python test_chatbot.py
```

### Expected Output
- Real-time test progress with results for each method
- Summary table with accuracy and confidence metrics
- Detailed results showing correct/incorrect predictions
- Category-based analysis

## Performance Considerations

### Method Comparison
- **Rule-Based**: ~1-2ms per query
- **Intent Classifier**: ~5-10ms per query (training: ~100ms)
- **NLP Similarity**: ~10-20ms per query (initialization: ~50ms)
- **Ensemble**: ~25-40ms per query

### Scalability
- Current setup handles ~100 concurrent users
- Knowledge base can support ~1000 Q&A pairs
- For larger deployments, consider:
  - Caching responses
  - Using a database backend
  - Implementing load balancing
  - Using a faster NLP library like spaCy

## Customization

### Adding New Intents
1. Add intent definition to `intents.json`
2. Add relevant patterns and keywords
3. Update `knowledge_base.json` if needed

### Modifying Weights
In `chatbot.py`, adjust the `method_weights`:
```python
self.method_weights = {
    'rule_based': 0.3,
    'intent_classifier': 0.4,
    'nlp_similarity': 0.3
}
```

### Changing Similarity Threshold
In `modules/rule_based.py`, modify:
```python
if best_score >= 0.3:  # Change this threshold
    return best_match_intent, best_response, best_score
```

## Troubleshooting

### Chatbot Not Initialized
- Check that `intents.json` and `knowledge_base.json` exist
- Verify file paths in `app.py`
- Check console for error messages

### Low Confidence Scores
- Add more patterns to intents
- Check that knowledge base references are correct
- Verify keyword coverage in intents

### Test Failures
- Ensure test_queries.json is properly formatted
- Check that expected intents match those in intents.json
- Review chatbot.log for detailed error information

## Future Enhancements

- [ ] Database backend for conversation history
- [ ] Multi-language support
- [ ] Advanced NLP using transformers (BERT)
- [ ] User feedback mechanism
- [ ] Admin dashboard for analytics
- [ ] Continuous learning from user interactions
- [ ] Integration with email/chat platforms
- [ ] Voice input/output support

## License

This project is provided as-is for educational purposes.

## Author

University Admission Chatbot - Academic Project

## Questions or Issues?

For questions or issues related to the chatbot functionality, refer to the knowledge base or contact the admissions office.

---

**Last Updated:** 2024
