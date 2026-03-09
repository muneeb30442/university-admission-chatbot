"""
Test Evaluation Script for University Admission Chatbot
Tests all three response generation methods against a test dataset.
"""

import json
import sys
from pathlib import Path
from chatbot import UniversityAdmissionChatbot
from tabulate import tabulate


class ChatbotTester:
    """Test suite for the chatbot."""
    
    def __init__(self, chatbot: UniversityAdmissionChatbot, test_file: str):
        """
        Initialize the tester.
        
        Args:
            chatbot: UniversityAdmissionChatbot instance
            test_file: Path to test queries JSON file
        """
        self.chatbot = chatbot
        self.test_file = test_file
        self.test_queries = self._load_test_queries()
        self.results = {
            'rule_based': [],
            'intent_classifier': [],
            'nlp_similarity': [],
            'ensemble': []
        }
    
    def _load_test_queries(self) -> list:
        """Load test queries from JSON file."""
        try:
            with open(self.test_file, 'r') as f:
                data = json.load(f)
                return data.get('test_queries', [])
        except FileNotFoundError:
            print(f"Error: Test file not found at {self.test_file}")
            return []
    
    def run_tests(self) -> None:
        """Run tests on all methods."""
        if not self.test_queries:
            print("No test queries available.")
            return
        
        print(f"\n{'='*80}")
        print("Testing University Admission Chatbot")
        print(f"Total test queries: {len(self.test_queries)}")
        print(f"{'='*80}\n")
        
        for i, test in enumerate(self.test_queries, 1):
            query = test.get('query')
            expected_intent = test.get('expected_intent')
            
            print(f"[{i}/{len(self.test_queries)}] Query: {query}")
            print(f"Expected Intent: {expected_intent}")
            
            # Test each method
            for method in ['rule_based', 'intent_classifier', 'nlp_similarity', 'ensemble']:
                result = self.chatbot.process_query(query, method=method)
                
                # Extract the actual intent from the result
                if method == 'ensemble':
                    actual_intent = result['responses'].get(result.get('ensemble_method'), {}).get('intent')
                else:
                    actual_intent = result['responses'].get(method, {}).get('intent')
                
                confidence = result['confidence']
                is_correct = actual_intent == expected_intent
                
                self.results[method].append({
                    'query': query,
                    'expected': expected_intent,
                    'actual': actual_intent,
                    'confidence': confidence,
                    'correct': is_correct
                })
                
                status = "✓" if is_correct else "✗"
                print(f"  {method:20} -> {status} Intent: {actual_intent} (Confidence: {confidence:.3f})")
            
            print()
    
    def print_summary(self) -> None:
        """Print test summary and accuracy metrics."""
        print(f"\n{'='*80}")
        print("Test Summary")
        print(f"{'='*80}\n")
        
        summary_data = []
        
        for method, results in self.results.items():
            if not results:
                continue
            
            correct = sum(1 for r in results if r['correct'])
            total = len(results)
            accuracy = (correct / total) * 100 if total > 0 else 0
            avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
            
            summary_data.append([
                method,
                f"{correct}/{total}",
                f"{accuracy:.1f}%",
                f"{avg_confidence:.3f}"
            ])
        
        print(tabulate(
            summary_data,
            headers=['Method', 'Correct', 'Accuracy', 'Avg Confidence'],
            tablefmt='grid'
        ))
        
        print()
    
    def print_detailed_results(self) -> None:
        """Print detailed results for each method."""
        print(f"\n{'='*80}")
        print("Detailed Results")
        print(f"{'='*80}\n")
        
        for method, results in self.results.items():
            if not results:
                continue
            
            print(f"\n{method.upper()}")
            print("-" * 80)
            
            detailed_data = []
            for r in results:
                status = "✓" if r['correct'] else "✗"
                detailed_data.append([
                    status,
                    r['query'][:30] + "..." if len(r['query']) > 30 else r['query'],
                    r['expected'],
                    r['actual'],
                    f"{r['confidence']:.3f}"
                ])
            
            print(tabulate(
                detailed_data,
                headers=['Status', 'Query', 'Expected', 'Actual', 'Confidence'],
                tablefmt='grid'
            ))
            print()
    
    def print_category_analysis(self) -> None:
        """Analyze results by query category."""
        print(f"\n{'='*80}")
        print("Category Analysis")
        print(f"{'='*80}\n")
        
        categories = {}
        
        # Group queries by category
        for test in self.test_queries:
            category = test.get('category', 'unknown')
            if category not in categories:
                categories[category] = []
            categories[category].append(test)
        
        # Calculate accuracy for each category
        category_data = []
        
        for method in ['rule_based', 'intent_classifier', 'nlp_similarity', 'ensemble']:
            print(f"\n{method.upper()}")
            print("-" * 80)
            
            method_results = self.results[method]
            
            for category, tests in sorted(categories.items()):
                category_results = [r for r in method_results if any(t['query'] == r['query'] for t in tests)]
                
                if category_results:
                    correct = sum(1 for r in category_results if r['correct'])
                    total = len(category_results)
                    accuracy = (correct / total) * 100 if total > 0 else 0
                    
                    print(f"  {category:25} {correct}/{total:2} ({accuracy:5.1f}%)")
    
    def export_results(self, output_file: str) -> None:
        """Export results to JSON file."""
        export_data = {
            'summary': {},
            'detailed_results': {}
        }
        
        for method, results in self.results.items():
            if results:
                correct = sum(1 for r in results if r['correct'])
                total = len(results)
                accuracy = (correct / total) * 100 if total > 0 else 0
                avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
                
                export_data['summary'][method] = {
                    'correct': correct,
                    'total': total,
                    'accuracy': round(accuracy, 2),
                    'average_confidence': round(avg_confidence, 3)
                }
                
                export_data['detailed_results'][method] = results
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\nResults exported to {output_file}")


def main():
    """Main function to run tests."""
    # Get paths
    base_dir = Path(__file__).parent
    intents_file = base_dir / 'intents.json'
    knowledge_base_file = base_dir / 'knowledge_base.json'
    test_file = base_dir / 'test_queries.json'
    output_file = base_dir / 'logs' / 'test_results.json'
    
    # Ensure logs directory exists
    (base_dir / 'logs').mkdir(exist_ok=True)
    
    print("Initializing University Admission Chatbot...")
    
    try:
        # Initialize chatbot
        chatbot = UniversityAdmissionChatbot(
            intents_path=str(intents_file),
            knowledge_base_path=str(knowledge_base_file),
            logs_dir=str(base_dir / 'logs')
        )
        
        # Create tester
        tester = ChatbotTester(chatbot, str(test_file))
        
        # Run tests
        tester.run_tests()
        
        # Print results
        tester.print_summary()
        tester.print_detailed_results()
        tester.print_category_analysis()
        
        # Export results
        tester.export_results(str(output_file))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
