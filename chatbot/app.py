"""
Flask Web Application for University Admission Chatbot
Provides REST API endpoints for the chatbot service.
"""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
from chatbot import UniversityAdmissionChatbot

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Get the directory where this file is located
BASE_DIR = Path(__file__).parent

# Initialize chatbot
try:
    chatbot = UniversityAdmissionChatbot(
        intents_path=str(BASE_DIR / 'intents.json'),
        knowledge_base_path=str(BASE_DIR / 'knowledge_base.json'),
        logs_dir=str(BASE_DIR / 'logs')
    )
except Exception as e:
    print(f"Error initializing chatbot: {str(e)}")
    chatbot = None


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatbot interaction.
    
    Expected JSON:
    {
        "message": "User message",
        "method": "rule_based|intent_classifier|nlp_similarity|ensemble" (optional, defaults to ensemble)
    }
    
    Returns:
        JSON with chatbot response and metadata
    """
    if chatbot is None:
        return jsonify({
            'error': 'Chatbot not initialized',
            'status': 'error'
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message field',
                'status': 'error'
            }), 400
        
        user_message = data.get('message', '').strip()
        method = data.get('method', 'ensemble')
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty',
                'status': 'error'
            }), 400
        
        # Process the query
        result = chatbot.process_query(user_message, method=method)
        
        # Save the interaction
        chatbot.save_interaction(
            user_input=user_message,
            response=result['final_response'],
            method=method,
            confidence=result['confidence']
        )
        
        return jsonify({
            'status': 'success',
            'response': result['final_response'],
            'confidence': round(result['confidence'], 3),
            'method': method,
            'intent': result['responses'].get(method, {}).get('intent') if method != 'ensemble' else result['responses'].get(result.get('ensemble_method'), {}).get('intent'),
            'timestamp': result['timestamp']
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/api/methods', methods=['GET'])
def get_methods():
    """Get available chatbot methods."""
    return jsonify({
        'methods': [
            {
                'name': 'rule_based',
                'description': 'Rule-based keyword matching'
            },
            {
                'name': 'intent_classifier',
                'description': 'Intent classification using scikit-learn'
            },
            {
                'name': 'nlp_similarity',
                'description': 'NLP similarity using TF-IDF and cosine similarity'
            },
            {
                'name': 'ensemble',
                'description': 'Ensemble of all three methods'
            }
        ]
    }), 200


@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get all available intents."""
    if chatbot is None:
        return jsonify({'error': 'Chatbot not initialized', 'status': 'error'}), 500
    
    try:
        intents = chatbot.rule_based.get_all_intents()
        return jsonify({
            'intents': intents,
            'count': len(intents)
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving intents: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get chatbot usage statistics."""
    if chatbot is None:
        return jsonify({'error': 'Chatbot not initialized', 'status': 'error'}), 500
    
    try:
        stats = chatbot.get_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving statistics: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify API is working."""
    return jsonify({
        'status': 'ok',
        'message': 'Chatbot API is running',
        'chatbot_initialized': chatbot is not None
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500


if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting University Admission Chatbot on {host}:{port}")
    print(f"Chatbot initialized: {chatbot is not None}")
    
    app.run(host=host, port=port, debug=debug)
