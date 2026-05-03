# Test Files & Questions Summary

## Overview
Your chatbot project now includes comprehensive testing resources with **40 diverse test questions** covering all admission categories and difficulty levels.

---

## Test Files Created

### 1. **test_queries.json** (Enhanced)
**Location:** `/chatbot/test_queries.json`
**Size:** 40 test questions

**Contents:**
- 40 diverse test questions organized by category
- Each question includes:
  - Query text
  - Expected intent classification
  - Category assignment
  - Difficulty level (simple/moderate/complex)
  - Description of what's being tested

**Difficulty Breakdown:**
- Simple: 17 questions (45%)
- Moderate: 17 questions (45%)
- Complex: 6 questions (10%)

**Category Breakdown:**
- Application Process: 9 questions
- Admission Requirements: 4 questions
- Tuition & Financial Aid: 8 questions
- Programs & Courses: 5 questions
- Campus Life & Facilities: 3 questions
- Special Cases: 4 questions
- Support & Contact: 2 questions
- Greetings: 4 questions

**Usage:**
```bash
python test_chatbot.py
```
This automatically runs all 40 questions through all three methods.

---

### 2. **TESTING_GUIDE.md** (New)
**Location:** `/chatbot/TESTING_GUIDE.md`
**Size:** 424 lines of comprehensive documentation

**Contents:**
- Quick start testing instructions
- Automated vs. manual testing methodology
- All 40 questions organized by category
- Each question includes:
  - Expected intent
  - Expected response type
  - Difficulty level
  - Special notes
  - Test methodology and tips
- Performance benchmarks for each method
- Expected results table
- Troubleshooting guide
- Performance optimization tips

**Key Sections:**
1. Overview & Quick Start
2. Test Questions by Category (detailed)
3. Testing Methodology (3 approaches)
4. Expected Results & Benchmarks
5. Sample Test Results Table
6. Performance Tips
7. Troubleshooting Guide
8. Next Steps

**Perfect For:**
- Understanding what each test question tests
- Learning expected results and performance
- Troubleshooting low accuracy issues
- Optimizing chatbot performance

---

### 3. **QUICK_TEST_REFERENCE.txt** (New)
**Location:** `/chatbot/QUICK_TEST_REFERENCE.txt`
**Size:** 237 lines

**Contents:**
- All 40 test questions in easy copy-paste format
- Organized by category and difficulty level
- Testing statistics
- How-to test guide
- Performance benchmarks
- Quick debug checklist
- Expected accuracy by method

**Key Features:**
- Copy & paste questions directly into chatbot
- No extra formatting needed
- Perfect for quick manual testing
- Includes testing workflow
- Debug checklist for verification

**Perfect For:**
- Quick manual testing in the web UI
- Copy-paste testing without scrolling
- Quick reference during testing
- Team testing sessions

---

### 4. **test_chatbot.py** (Already Created)
**Location:** `/chatbot/test_chatbot.py`
**Function:** Automated test runner

**What It Does:**
```bash
python test_chatbot.py
```

**Outputs:**
- Runs all 40 questions through all 3 methods
- Generates accuracy metrics
- Creates detailed test report
- Calculates response times
- Saves results to `logs/test_results_*.json`
- Displays summary statistics

**Metrics Provided:**
- Intent classification accuracy
- Method comparison
- Response time per method
- Confidence score analysis
- Category-wise performance

---

## How to Use the Test Files

### Option 1: Automated Testing (Recommended for First Run)
```bash
cd chatbot
python test_chatbot.py
```

**This will:**
1. Load all 40 test questions from `test_queries.json`
2. Run them through all 3 response methods
3. Generate comprehensive metrics
4. Show results in console and save to logs
5. Create `test_results_*.json` with detailed data

**Expected Output:**
```
Testing all 40 queries with 3 methods...
Rule-Based Accuracy: 68.5%
Intent Classifier Accuracy: 79.2%
NLP Similarity Accuracy: 74.8%
Ensemble Accuracy: 86.3%

Results saved to logs/test_results_2024-01-15_14-32-45.json
```

---

### Option 2: Manual Testing Using Web UI
```bash
cd chatbot
python app.py
# Visit http://localhost:5000
```

**Workflow:**
1. Keep `QUICK_TEST_REFERENCE.txt` open
2. Copy a question from the reference file
3. Paste into chatbot chat box
4. Select response method (or use Ensemble)
5. Review response quality and confidence
6. Check statistics in sidebar
7. Repeat with next question

**Best Practice:**
- Start with simple questions (1-5 per category)
- Move to moderate questions
- Challenge with complex questions
- Use Ensemble method for best results

---

### Option 3: Programmatic Testing
```python
from chatbot import UniversityChatbot
import json

bot = UniversityChatbot()

# Load test queries
with open('test_queries.json') as f:
    test_data = json.load(f)

# Test each query
for q in test_data['test_queries'][:10]:  # First 10
    response = bot.get_response(q['query'])
    print(f"Q: {q['query']}")
    print(f"A: {response['response']}")
    print(f"Confidence: {response['confidence']}\n")
```

---

## Test Question Examples

### Simple Question (Copy & Test)
```
"What is the application deadline?"
Expected: Information about submission deadlines
Method: Rule-Based will likely get this
Difficulty: SIMPLE
```

### Moderate Question (Copy & Test)
```
"Which files and certificates should I include in my application?"
Expected: List of required documents
Method: Intent Classifier should handle paraphrasing
Difficulty: MODERATE
```

### Complex Question (Copy & Test)
```
"What are the requirements for transferring as an international student?"
Expected: Combined transfer + international requirements
Method: Ensemble recommended for accuracy
Difficulty: COMPLEX
```

---

## Performance Expectations

### By Method:

**Rule-Based Keyword Matching:**
- Accuracy: 65-75%
- Speed: 1-2ms
- Best for: Simple, keyword-exact questions
- Struggles with: Paraphrasing, complex queries

**Intent Classification (ML):**
- Accuracy: 75-85%
- Speed: 5-10ms
- Best for: Intent variations, medium complexity
- Struggles with: Completely new phrasings

**NLP Similarity (TF-IDF):**
- Accuracy: 70-80%
- Speed: 10-20ms
- Best for: Semantic understanding
- Struggles with: Very different phrasings

**Ensemble (All Three):**
- Accuracy: 80-90% ⭐ RECOMMENDED
- Speed: 25-40ms
- Best for: Production use, reliability
- Benefits: Combines strengths of all methods

---

## Expected Test Results

Here's what you should see when testing:

### Question 1: "What is the application deadline?"
```
Rule-Based:   HIGH confidence (matches keywords)
Intent:       HIGH confidence (clear intent)
NLP:          HIGH confidence (similarity match)
Ensemble:     HIGH confidence (unanimous)
Expected:     "The application deadline is [DATE]"
```

### Question 9: "Tell me about campus life"
```
Rule-Based:   MEDIUM-LOW confidence (vague keywords)
Intent:       MEDIUM confidence (camping facility intent detected)
NLP:          MEDIUM confidence (semantic similarity)
Ensemble:     MEDIUM-HIGH confidence (weighted average)
Expected:     General campus life information with facilities
```

### Question 39: "I'm confused about the application process..."
```
Rule-Based:   LOW confidence (no exact keywords)
Intent:       MEDIUM confidence (process intent recognized)
NLP:          MEDIUM confidence (some similarity)
Ensemble:     MEDIUM-HIGH confidence (fallback to process guide)
Expected:     Comprehensive application process explanation
```

---

## After Testing

### If Accuracy is High (>80%):
- ✅ Chatbot is performing well
- Consider deploying to production
- Continue monitoring user feedback

### If Accuracy is Medium (70-80%):
- Review failed test cases
- Add missing Q&A pairs to `knowledge_base.json`
- Enhance intents in `intents.json`
- Re-run tests to verify improvements

### If Accuracy is Low (<70%):
- Check logs for common failure patterns
- Expand knowledge base significantly
- Add more intent patterns
- Verify chatbot models loaded correctly
- Check for JSON syntax errors

---

## Files & Locations

```
chatbot/
├── test_queries.json              ← Updated with 40 questions
├── test_chatbot.py                ← Automated test runner
├── TESTING_GUIDE.md               ← Comprehensive testing guide
├── QUICK_TEST_REFERENCE.txt       ← Copy-paste quick reference
├── knowledge_base.json            ← Q&A data to improve
├── intents.json                   ← Intents to enhance
└── logs/
    └── test_results_*.json        ← Test results (auto-generated)
```

---

## Quick Testing Commands

```bash
# Run all 40 automated tests
python test_chatbot.py

# Start web interface for manual testing
python app.py

# View test results (after running tests)
cat logs/test_results_*.json

# Run tests and save detailed report
python test_chatbot.py > test_report.txt
```

---

## Next Steps

1. **Run Automated Tests**
   ```bash
   python test_chatbot.py
   ```

2. **Review Results**
   - Check console output
   - Review `logs/test_results_*.json`
   - Note which questions failed

3. **Manual Testing** (Optional)
   ```bash
   python app.py
   # Visit http://localhost:5000
   # Use QUICK_TEST_REFERENCE.txt
   ```

4. **Improve Performance**
   - Edit `knowledge_base.json` to add more Q&A
   - Edit `intents.json` to add pattern variations
   - Rerun tests: `python test_chatbot.py`

5. **Deploy When Ready**
   - See SETUP_GUIDE.md for deployment options
   - Use Ensemble method in production
   - Monitor performance with logs

---

## Support

For detailed information:
- **General Info:** `README.md`
- **Setup Instructions:** `SETUP_GUIDE.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`
- **Testing Details:** `TESTING_GUIDE.md`
- **Quick Reference:** `QUICK_TEST_REFERENCE.txt`

Good luck with testing! 🚀
