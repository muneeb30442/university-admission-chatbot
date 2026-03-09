# University Admission Chatbot - Complete Setup Guide

This guide will walk you through setting up and running the University Admission Chatbot from scratch.

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd chatbot
pip install -r requirements.txt
```

### 2. Run the Flask Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to `http://localhost:5000`

## Detailed Setup Instructions

### Step 1: Environment Setup

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify Project Structure

Ensure your project has this structure:
```
chatbot/
├── app.py
├── chatbot.py
├── knowledge_base.json
├── intents.json
├── test_queries.json
├── test_chatbot.py
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md
│
├── modules/
│   ├── __init__.py
│   ├── rule_based.py
│   ├── intent_classifier.py
│   └── nlp_similarity.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── (CSS, JS files if any)
│
└── logs/
    └── (logs will be created here)
```

### Step 3: Running the Chatbot

#### Option A: Web Interface (Recommended)
```bash
python app.py
```
Then visit `http://localhost:5000`

#### Option B: Command Line Testing
```bash
python test_chatbot.py
```

#### Option C: Programmatic Usage
```python
from chatbot import UniversityAdmissionChatbot

chatbot = UniversityAdmissionChatbot()
result = chatbot.process_query("What is the application deadline?")
print(result['final_response'])
```

## Configuration

### Changing Port
Edit `app.py` or use environment variables:
```bash
# Windows
set FLASK_PORT=8080
python app.py

# macOS/Linux
export FLASK_PORT=8080
python app.py
```

### Enable Debug Mode
```bash
# Windows
set FLASK_DEBUG=True
python app.py

# macOS/Linux
export FLASK_DEBUG=True
python app.py
```

### Customize Method Weights
In `chatbot.py`, find the `__init__` method and modify:
```python
self.method_weights = {
    'rule_based': 0.2,        # Change these values
    'intent_classifier': 0.4,
    'nlp_similarity': 0.4
}
```
(Must sum to 1.0)

## Using the Web Interface

### Chatting with the Bot
1. Type your question in the input field
2. Click "Send" or press Enter
3. Select a method from the dropdown (Ensemble is recommended)
4. View the response with confidence score and intent

### Available Methods
- **Ensemble**: Combines all three approaches for best results
- **Rule-Based**: Fast keyword matching
- **Intent Classifier**: ML-based classification
- **NLP Similarity**: Semantic similarity matching

### Real-time Statistics
The sidebar shows:
- Total messages sent
- Average confidence score
- Last detected intent
- Method descriptions

## Running Tests

### Quick Test
```bash
python test_chatbot.py
```

### What the Tests Do
1. Tests 40 predefined queries across all categories
2. Tests all 4 methods (rule-based, intent classifier, NLP similarity, ensemble)
3. Calculates accuracy, confidence, and category breakdowns
4. Exports detailed results to `logs/test_results.json`

### Understanding Test Output

**Example Output:**
```
[1/40] Query: What is the application deadline?
Expected Intent: application_deadline
  rule_based           -> ✓ Intent: application_deadline (Confidence: 0.500)
  intent_classifier    -> ✓ Intent: application_deadline (Confidence: 0.850)
  nlp_similarity       -> ✓ Intent: application_deadline (Confidence: 0.920)
  ensemble             -> ✓ Intent: application_deadline (Confidence: 0.857)
```

## API Reference

### Chat API
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the deadline?", "method": "ensemble"}'
```

### Get Intents
```bash
curl http://localhost:5000/api/intents
```

### Get Statistics
```bash
curl http://localhost:5000/api/statistics
```

### Get Available Methods
```bash
curl http://localhost:5000/api/methods
```

## Logging

### Where Logs Are Stored
- **Daily logs**: `logs/chatbot_YYYYMMDD.log`
- **Interactions**: `logs/interactions.jsonl` (JSON Lines format)
- **Test results**: `logs/test_results.json` (after running tests)

### Reading Logs

Daily logs are human-readable:
```
2024-01-15 10:30:45,123 - __main__ - INFO - User Query: What is the deadline?
2024-01-15 10:30:45,456 - __main__ - INFO - Response: March 15th... (Confidence: 0.95)
```

Interactions are JSON format:
```json
{"timestamp": "2024-01-15T10:30:45.123456", "user_input": "What is the deadline?", "response": "March 15th...", "method": "ensemble", "confidence": 0.95}
```

## Customization Guide

### Adding New Questions

1. **Edit `intents.json`** - Add a new intent object:
```json
{
  "intent": "my_new_intent",
  "patterns": [
    "Your pattern 1",
    "Your pattern 2",
    "Your pattern 3"
  ],
  "responses": ["knowledge_base.section.key"],
  "keywords": ["key1", "key2", "key3"]
}
```

2. **Edit `knowledge_base.json`** - Add the response:
```json
{
  "section": {
    "key": "Your response here"
  }
}
```

3. **Restart the application** - Changes take effect immediately

### Adding Test Queries

1. Edit `test_queries.json`
2. Add a new object in the `test_queries` array:
```json
{
  "id": 41,
  "query": "Your test question",
  "expected_intent": "my_new_intent",
  "category": "category_name"
}
```

3. Run tests to evaluate the new query

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Ensure you're in the `chatbot` directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change the port:
```bash
python app.py --port 8080
# Or set environment variable (see Configuration section)
```

### Issue: Low confidence scores
**Solutions:**
- Add more patterns to the intents
- Check that keywords match your patterns
- Ensure knowledge base references are correct

### Issue: Wrong intent detected
**Solutions:**
- Review the patterns for that intent
- Check for overlapping patterns with other intents
- Adjust method weights toward the better-performing method

### Issue: AttributeError in modules
**Solution:** Ensure all files are in the correct directories:
```bash
# Verify module files exist
ls modules/rule_based.py
ls modules/intent_classifier.py
ls modules/nlp_similarity.py
```

## Performance Optimization

### For Production Deployment

1. **Disable Flask Debug Mode:**
```python
app.run(debug=False)
```

2. **Use a Production Server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Add Caching:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

4. **Database Backend:**
Replace JSON files with a database for:
- Knowledge base
- Interaction logging
- Better scalability

## Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t admission-chatbot .
docker run -p 5000:5000 admission-chatbot
```

## Advanced Usage

### Ensemble Weight Tuning
Run tests with different weights and analyze results:
```python
weights = [
    {'rule_based': 0.2, 'intent_classifier': 0.4, 'nlp_similarity': 0.4},
    {'rule_based': 0.3, 'intent_classifier': 0.4, 'nlp_similarity': 0.3},
    {'rule_based': 0.1, 'intent_classifier': 0.5, 'nlp_similarity': 0.4},
]

for w in weights:
    chatbot.method_weights = w
    # Run tests and compare results
```

### Adding New Methods
1. Create a new file in `modules/`
2. Implement the interface (must have a method returning intent, response, confidence)
3. Add to chatbot orchestrator
4. Include in test suite

## Support and Questions

### Debugging Mode
Add debug statements in your code:
```python
print("[DEBUG] variable:", variable)
```

### Check Logs
```bash
# View today's logs
cat logs/chatbot_$(date +%Y%m%d).log

# View latest interactions
tail -n 20 logs/interactions.jsonl
```

### Verify API
```bash
curl http://localhost:5000/api/test
```

## Next Steps

1. Deploy to production using Flask with Gunicorn
2. Add database backend for scalability
3. Implement user authentication
4. Add admin dashboard for analytics
5. Integrate with chat platforms (Slack, Teams, etc.)
6. Add voice/audio capabilities
7. Implement continuous learning from user feedback

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Python Documentation](https://docs.python.org/3/)

---

**Happy Chatting! 🚀**
