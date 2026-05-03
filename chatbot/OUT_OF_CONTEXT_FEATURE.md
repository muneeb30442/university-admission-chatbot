# Out-of-Context Query Detection Feature

## Overview

The Out-of-Context Detection Feature automatically identifies when users ask questions that are unrelated to university admissions and responds with a polite apology message instead of attempting to answer irrelevant queries.

## How It Works

### 1. **Automatic Detection**

When a user submits a query, the system:
- Analyzes the input for admission-related keywords (eligibility, tuition, programs, etc.)
- Checks for out-of-context keywords (weather, recipes, sports, etc.)
- Calculates a relevance score based on keyword presence
- Determines if the query is in-scope or out-of-scope

### 2. **Detection Methods**

The detector uses multiple strategies:

#### Keyword-Based Detection
- Maintains a list of **50+ admission-related keywords**
- Maintains a list of **60+ out-of-context keywords**
- Compares user input against these lists

#### Relevance Scoring
- Calculates: `relevance_score = admission_keywords_found / total_keywords_found`
- Default threshold: 30% relevance required for in-context classification
- Configurable threshold for custom sensitivity

#### Detection Reasons

The system returns specific reasons for out-of-context classification:

| Reason | Description |
|--------|-------------|
| `no_relevant_keywords` | No admission or out-of-context keywords detected |
| `out_of_context_keywords` | More out-of-context keywords than admission keywords |
| `low_relevance_score` | Relevance score below threshold |
| `in_context` | Query is relevant to admissions |

### 3. **Response Behavior**

#### When Query is IN-CONTEXT:
- Processes normally through all three methods
- Returns admission-related answer
- Logs as normal interaction

#### When Query is OUT-OF-CONTEXT:
- Immediately returns apology message
- Skips processing through response methods
- Sets response method to `out_of_context_detection`
- Sets confidence to 1.0 (certain detection)
- Logs reason for out-of-context classification

## Examples

### IN-CONTEXT Queries (Will Process)
```
- "What is the application deadline?"
- "What GPA do I need?"
- "Tell me about your engineering program"
- "Is housing available on campus?"
- "Do you offer scholarships?"
```

### OUT-OF-CONTEXT Queries (Will Get Apology)
```
- "What's the weather today?"
- "Can you help me cook pizza?"
- "Tell me a joke"
- "How do I code in Python?"
- "What's the stock market doing?"
- "Can you recommend a movie?"
```

### BORDERLINE Queries (May Be Detected as Out-of-Context)
```
- "Why is education important?" - Out-of-context (philosophical question)
- "Do you have a sports team?" - In-context (campus life question)
- "What programming language do you teach?" - Could be in-context if interpreted as program info
```

## Default Apology Message

```
I appreciate your question, but I'm specifically designed to help with university admissions inquiries. 
Could you please ask me about application deadlines, eligibility requirements, tuition, programs, 
campus facilities, or other admission-related topics? I'm here to assist!
```

### Customizing the Apology Message

Edit the message in `knowledge_base.json`:

```json
{
  "messages": {
    "out_of_context_apology": "YOUR CUSTOM MESSAGE HERE"
  }
}
```

## Configuration

### Adjusting Detection Sensitivity

Edit the threshold in `out_of_context_detector.py`:

```python
# Current default: 30% relevance required
def is_out_of_context(self, user_input: str, confidence_threshold: float = 0.3):
```

**Change threshold to:**
- **0.1** - More lenient (fewer queries marked as out-of-context)
- **0.3** - Default (balanced)
- **0.5** - Stricter (more queries marked as out-of-context)

### Adding Custom Keywords

Edit the keyword sets in `out_of_context_detector.py`:

```python
# Add to admission keywords
self.admission_keywords = {
    'existing_keywords...',
    'your_new_keyword'
}

# Add to out-of-context keywords
self.out_of_context_keywords = {
    'existing_keywords...',
    'your_new_keyword'
}
```

## Integration with Response Methods

### Processing Flow

```
User Input
    ↓
Out-of-Context Check
    ├─→ OUT-OF-CONTEXT → Apology Message → Response
    │
    └─→ IN-CONTEXT → Process through 3 methods → Response
                      ├─ Rule-Based
                      ├─ Intent Classifier
                      └─ NLP Similarity (Ensemble)
```

### API Response Format

When out-of-context is detected, the response includes:

```python
{
    'user_input': 'What is the weather?',
    'final_response': 'I appreciate your question...',
    'confidence': 1.0,
    'method': 'out_of_context_detection',
    'is_out_of_context': True,
    'out_of_context_reason': 'out_of_context_keywords',
    'timestamp': '2024-01-15T10:30:00.000000'
}
```

### Comparison with Normal Response

**IN-CONTEXT Response:**
```python
{
    'method': 'ensemble',
    'is_out_of_context': False,
    'out_of_context_reason': None,
    'responses': {
        'rule_based': {...},
        'intent_classifier': {...},
        'nlp_similarity': {...}
    }
}
```

**OUT-OF-CONTEXT Response:**
```python
{
    'method': 'out_of_context_detection',
    'is_out_of_context': True,
    'out_of_context_reason': 'low_relevance_score',
    'responses': {}  # Empty - no processing done
}
```

## Testing the Feature

### Manual Testing

1. **Test IN-CONTEXT query:**
   ```python
   result = chatbot.process_query("What are the application requirements?")
   # Should process normally
   ```

2. **Test OUT-OF-CONTEXT query:**
   ```python
   result = chatbot.process_query("Tell me a joke")
   # Should return apology message
   ```

3. **Check detection details:**
   ```python
   is_out, reason = detector.is_out_of_context("How do I cook pasta?")
   print(reason)  # Outputs: 'out_of_context_keywords'
   ```

### Automated Testing

Run the test suite:
```bash
python test_chatbot.py
```

## Performance Impact

- **Detection Time**: ~2-5ms per query (negligible)
- **No Additional Dependencies**: Uses only built-in Python
- **No External API Calls**: Fully local processing
- **Early Exit**: Out-of-context queries skip all three response methods

## Logging

Out-of-context detections are logged with full details:

```
2024-01-15 10:30:45,123 - __main__ - INFO - User Query: Tell me a joke
2024-01-15 10:30:45,125 - __main__ - INFO - Out-of-Context Query Detected (Reason: out_of_context_keywords). Apology Message Sent.
```

Check logs in: `logs/chatbot_YYYYMMDD.log`

## Limitations and Edge Cases

### Known Limitations

1. **Ambiguous Queries**: Queries that could be interpreted multiple ways may be misclassified
2. **Slang/Informal Language**: May not catch all colloquial out-of-context references
3. **New Topics**: Keywords for newly emerging topics may not be in the lists
4. **Domain-Specific Terms**: Some academic domains might have overlapping terminology

### Examples of Edge Cases

```python
# May be IN-CONTEXT (program name contains word)
"Do you have a course on environmental science?" # 'science' in out-of-context keywords

# May be OUT-OF-CONTEXT (admission-related but phrased differently)
"How much does it cost per year?" # Could be tuition or general pricing

# Truly ambiguous
"Can you help me with computer science?" # Programming vs academic program
```

### Adjusting for Edge Cases

If specific queries are misclassified, adjust:
1. **Keyword lists** - Add/remove keywords
2. **Confidence threshold** - Increase/decrease sensitivity
3. **Custom logic** - Add specific rules in `is_out_of_context()` method

## Future Enhancements

Potential improvements to the feature:

1. **Machine Learning Classification**: Train on conversation data
2. **Semantic Similarity**: Use sentence embeddings instead of keywords
3. **User Preferences**: Allow customization per chatbot instance
4. **Feedback Loop**: Learn from user feedback on classifications
5. **Intent-Based Detection**: Integrate with intent classification confidence scores
6. **Context History**: Consider conversation history in classification
7. **Multi-Language Support**: Handle non-English queries

## File Structure

```
chatbot/
├── modules/
│   └── out_of_context_detector.py    # Detection logic
├── knowledge_base.json                # Contains apology message
├── chatbot.py                         # Integration point
└── logs/                              # Detection logs
```

## Summary

The Out-of-Context Detection Feature:
- ✅ Automatically identifies irrelevant queries
- ✅ Responds with polite apology message
- ✅ Improves user experience
- ✅ Reduces irrelevant response attempts
- ✅ Fully configurable and extensible
- ✅ Minimal performance overhead
- ✅ Detailed logging for monitoring
