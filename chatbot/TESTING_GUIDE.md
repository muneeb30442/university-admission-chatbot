# University Admission Chatbot - Testing Guide

## Overview
This comprehensive testing guide provides 40 test questions across all categories with varying difficulty levels. Test the chatbot using all three response generation methods: Rule-Based, Intent Classification, and NLP Similarity.

---

## Quick Start Testing

### Automated Testing
Run all 40 test cases automatically:
```bash
python test_chatbot.py
```

This will:
- Test all 40 queries against all three methods
- Generate accuracy metrics
- Create a detailed test report
- Save results to `logs/test_results.json`

### Manual Testing
Open the web interface:
```bash
python app.py
```
Then visit: `http://localhost:5000` and type questions directly.

---

## Test Questions by Category

### CATEGORY 1: Application Process (9 Questions)

#### Simple Questions (Direct matching expected)
1. **"What is the application deadline?"**
   - Expected Intent: `application_deadline`
   - Expected Response: Information about submission deadlines
   - Difficulty: SIMPLE

2. **"By when do I need to apply?"**
   - Expected Intent: `application_deadline`
   - Expected Response: Should mention deadline dates
   - Difficulty: SIMPLE

3. **"What documents do I need to submit?"**
   - Expected Intent: `required_documents`
   - Expected Response: List of required documents (transcript, SAT scores, essays, recommendations)
   - Difficulty: SIMPLE

4. **"Is a recommendation letter required?"**
   - Expected Intent: `required_documents`
   - Expected Response: Confirmation and details about recommendation letters
   - Difficulty: SIMPLE

5. **"How long does it take to hear back from admissions?"**
   - Expected Intent: `admission_timeline`
   - Expected Response: Timeline for admission decisions
   - Difficulty: SIMPLE

#### Moderate Questions (Paraphrasing, semantic understanding)
6. **"I need to know the submission deadline - can you help?"**
   - Expected Intent: `application_deadline`
   - Expected Response: Deadline information despite conversational phrasing
   - Difficulty: MODERATE

7. **"Which files and certificates should I include in my application?"**
   - Expected Intent: `required_documents`
   - Expected Response: List of documents needed
   - Difficulty: MODERATE

8. **"When should I expect to receive my admission decision?"**
   - Expected Intent: `admission_timeline`
   - Expected Response: Decision timeline information
   - Difficulty: MODERATE

#### Complex Questions (Multi-part, contextual understanding)
9. **"I'm confused about the application process, can you explain it step by step?"**
   - Expected Intent: `application_process`
   - Expected Response: Comprehensive explanation of the entire application workflow
   - Difficulty: COMPLEX
   - Note: Requires holistic understanding of application process

---

### CATEGORY 2: Admission Requirements (4 Questions)

#### Simple Questions
1. **"What are the eligibility requirements?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: Minimum GPA, test scores, and other requirements
   - Difficulty: SIMPLE

2. **"What's the minimum GPA required?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: Specific GPA threshold (e.g., 3.0 or higher)
   - Difficulty: SIMPLE

3. **"What SAT score do I need?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: SAT score requirements
   - Difficulty: SIMPLE

#### Moderate Questions
4. **"Am I eligible to apply if I have a 3.2 GPA?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: Confirmation of eligibility with explanation
   - Difficulty: MODERATE
   - Note: Requires understanding of threshold comparison

#### Complex Questions
5. **"What's the minimum GPA and SAT score needed to get in?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: Combined requirements information
   - Difficulty: COMPLEX

6. **"Can I apply if I don't have perfect test scores?"**
   - Expected Intent: `eligibility_requirements`
   - Expected Response: Clarification that perfection isn't required
   - Difficulty: COMPLEX

---

### CATEGORY 3: Tuition & Financial Aid (8 Questions)

#### Simple Questions
1. **"What is the application fee?"**
   - Expected Intent: `application_fee`
   - Expected Response: Application fee amount ($50-75 typical)
   - Difficulty: SIMPLE

2. **"Do you charge for applications? How much?"**
   - Expected Intent: `application_fee`
   - Expected Response: Fee information
   - Difficulty: SIMPLE

3. **"What is the tuition cost per semester?"**
   - Expected Intent: `tuition_costs`
   - Expected Response: Per-semester or annual tuition amount
   - Difficulty: SIMPLE

4. **"What financial aid options are available?"**
   - Expected Intent: `financial_aid`
   - Expected Response: Overview of scholarships, grants, loans
   - Difficulty: SIMPLE

5. **"Do you have on-campus housing and dining facilities?"**
   - Expected Intent: `campus_facilities`
   - Expected Response: Information about housing and dining
   - Difficulty: SIMPLE

#### Moderate Questions
6. **"Are there fee waivers available for underprivileged students?"**
   - Expected Intent: `application_fee`
   - Expected Response: Information about fee waiver programs
   - Difficulty: MODERATE

7. **"How much will my degree cost in total?"**
   - Expected Intent: `tuition_costs`
   - Expected Response: Total cost calculation (tuition × years + fees)
   - Difficulty: MODERATE

8. **"Do you have scholarships or grants for merit students?"**
   - Expected Intent: `financial_aid`
   - Expected Response: Merit-based financial aid information
   - Difficulty: MODERATE

#### Complex Questions
9. **"Can I get financial assistance if my family has low income?"**
   - Expected Intent: `financial_aid`
   - Expected Response: Need-based financial aid options
   - Difficulty: COMPLEX

10. **"Do you have any information about scholarships for minorities or women?"**
    - Expected Intent: `financial_aid`
    - Expected Response: Diversity scholarships and special programs
    - Difficulty: COMPLEX

---

### CATEGORY 4: Programs & Courses (5 Questions)

#### Simple Questions
1. **"What majors and programs do you offer?"**
   - Expected Intent: `course_programs`
   - Expected Response: List of available programs (Engineering, Business, Liberal Arts, etc.)
   - Difficulty: SIMPLE

2. **"Can I study engineering or computer science?"**
   - Expected Intent: `course_programs`
   - Expected Response: Confirmation of program availability
   - Difficulty: SIMPLE

3. **"Is your program a 3-year or 4-year program?"**
   - Expected Intent: `program_duration`
   - Expected Response: Duration information
   - Difficulty: SIMPLE

#### Moderate Questions
4. **"What specializations are available within your business program?"**
   - Expected Intent: `course_programs`
   - Expected Response: List of business program specializations
   - Difficulty: MODERATE

5. **"How long does it take to complete a degree program?"**
   - Expected Intent: `program_duration`
   - Expected Response: Typical program duration (3-4 years)
   - Difficulty: MODERATE

---

### CATEGORY 5: Campus Life & Facilities (3 Questions)

#### Moderate Questions
1. **"What is the campus like? Tell me about student life."**
   - Expected Intent: `campus_facilities`
   - Expected Response: Comprehensive description of campus and student experience
   - Difficulty: MODERATE

2. **"What clubs and student organizations are available?"**
   - Expected Intent: `campus_facilities`
   - Expected Response: Information about student organizations and clubs
   - Difficulty: MODERATE

#### Simple Questions
3. **"Do you have on-campus housing?"**
   - Expected Intent: `campus_facilities`
   - Expected Response: Confirmation and details about housing
   - Difficulty: SIMPLE

---

### CATEGORY 6: Special Cases (4 Questions)

#### Simple Questions
1. **"Can international students apply?"**
   - Expected Intent: `international_students`
   - Expected Response: Yes, with information about international application process
   - Difficulty: SIMPLE

2. **"Can I transfer from another university to yours?"**
   - Expected Intent: `transfer_admission`
   - Expected Response: Yes, with transfer requirements information
   - Difficulty: SIMPLE

#### Moderate Questions
3. **"What English proficiency test scores do you require for international applicants?"**
   - Expected Intent: `international_students`
   - Expected Response: TOEFL or IELTS score requirements
   - Difficulty: MODERATE

#### Complex Questions
4. **"What are the requirements for transferring as an international student?"**
   - Expected Intent: `transfer_admission`
   - Expected Response: Combined international + transfer requirements
   - Difficulty: COMPLEX

---

### CATEGORY 7: Support & Contact (2 Questions)

#### Simple Questions
1. **"How can I contact the admissions office?"**
   - Expected Intent: `contact_info`
   - Expected Response: Phone number, email, address
   - Difficulty: SIMPLE

2. **"What is the phone number and email for admissions?"**
   - Expected Intent: `contact_info`
   - Expected Response: Specific contact details
   - Difficulty: SIMPLE

---

### CATEGORY 8: Greetings (4 Questions)

#### Simple Questions
1. **"Hello!"**
   - Expected Intent: `greeting`
   - Expected Response: Friendly greeting and offer to help
   - Difficulty: SIMPLE

2. **"Hi, I have some questions about your university"**
   - Expected Intent: `greeting`
   - Expected Response: Warm greeting and readiness to help
   - Difficulty: SIMPLE

3. **"Good morning! Can you help me with admission information?"**
   - Expected Intent: `greeting`
   - Expected Response: Positive response with help offer
   - Difficulty: SIMPLE

4. **"Thanks for your help, goodbye!"**
   - Expected Intent: `goodbye`
   - Expected Response: Farewell message with good wishes
   - Difficulty: SIMPLE

---

## Testing Methodology

### Method 1: Automated Testing
```bash
cd chatbot
python test_chatbot.py
```

**Output includes:**
- Test case number and query
- Response from each method
- Intent classification accuracy
- Overall metrics (precision, recall, F1-score)

### Method 2: Manual Testing in Web UI
1. Open `http://localhost:5000`
2. Select response method from dropdown (or use Ensemble for best results)
3. Type a question from the test list
4. Verify response quality and relevance
5. Check confidence score and method information
6. View statistics sidebar for performance metrics

### Method 3: Programmatic Testing
```python
from chatbot import UniversityChatbot

bot = UniversityChatbot()

# Test a query
response = bot.get_response("What is the application deadline?")
print(response)
```

---

## Expected Results

### Rule-Based Method
- **Best for:** Simple, keyword-matching questions
- **Expected Accuracy:** 65-75%
- **Response Time:** 1-2ms
- **Confidence:** 0.7-0.9
- **Ideal Cases:** Questions 1-3, 13-15, 33-34

### Intent Classification Method
- **Best for:** Various phrasings of the same intent
- **Expected Accuracy:** 75-85%
- **Response Time:** 5-10ms
- **Confidence:** 0.6-0.95
- **Ideal Cases:** Questions 4-8, 16-20, 25-28

### NLP Similarity Method
- **Best for:** Semantic understanding, complex questions
- **Expected Accuracy:** 70-80%
- **Response Time:** 10-20ms
- **Confidence:** 0.5-0.9
- **Ideal Cases:** Questions 9, 24, 30, 39-40

### Ensemble Method (RECOMMENDED)
- **Best for:** Overall reliability and accuracy
- **Expected Accuracy:** 80-90%
- **Response Time:** 25-40ms
- **Confidence:** 0.8-0.98
- **Best Practice:** Use for production

---

## Sample Test Results

Here's what you should expect:

| Query | Rule-Based | Intent | NLP | Ensemble | Expected |
|-------|-----------|--------|-----|----------|----------|
| "What is the application deadline?" | High | High | High | High | deadline |
| "By when do I need to apply?" | Med | High | High | High | deadline |
| "Am I eligible if I have 3.2 GPA?" | Low | High | High | High | requirements |
| "Tell me about campus life" | Low | High | High | High | facilities |
| "What's transfers + international?" | None | Med | Med | High | transfer_intl |

---

## Performance Optimization Tips

1. **Pre-load Models:** Models are cached after first use (3-5 seconds slower first time)
2. **Batch Testing:** Use `test_chatbot.py` for faster batch evaluation
3. **Monitor Logs:** Check `logs/` for performance metrics
4. **Fine-tune Intents:** Add more patterns to `intents.json` for better classification

---

## Troubleshooting

### Issue: Low accuracy on similar questions
**Solution:** The similarity threshold might need adjustment in `nlp_similarity.py` (default: 0.5)

### Issue: Intent classifier not recognizing variations
**Solution:** Add more pattern examples to `intents.json` for that intent

### Issue: Rule-based method always returns fallback
**Solution:** Check `rule_based.py` keyword mappings match your knowledge base

### Issue: Slow response times
**Solution:** Use Ensemble mode intelligently - cache frequent queries

---

## Next Steps After Testing

1. **Review Results:** Check `logs/test_results_*.json` for detailed metrics
2. **Identify Weak Areas:** Look for patterns in failed queries
3. **Improve Knowledge Base:** Add more Q&A pairs to `knowledge_base.json`
4. **Enhance Intents:** Add variations to `intents.json` for better classification
5. **Deploy:** Once satisfied, deploy to production (see SETUP_GUIDE.md)

---

## Additional Resources

- Full project documentation: `README.md`
- Setup instructions: `SETUP_GUIDE.md`
- Project structure: `PROJECT_STRUCTURE.md`
- API endpoints: See `README.md` > API Documentation

Good luck with your testing!
