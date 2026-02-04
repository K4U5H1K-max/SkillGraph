#!/usr/bin/env python3
"""
Flask API Server for Personalized Learning Roadmap
Handles roadmap loading, conversation, and personalization
"""

import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add modules to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "llm"))
sys.path.insert(0, str(project_root / "personalizer"))
sys.path.insert(0, str(project_root / "roadmap_updater"))

from conversation_engine import GeminiConversationEngine
from role_guides import ROLE_GUIDES
from service import personalize
from updater import update_roadmap

app = Flask(__name__)
CORS(app)

# Store active conversation engines
conversations = {}

# Mapping from role keys to preset roadmap files
PRESET_ROADMAPS = {
    "ai_data_scientist": "fake frontend/ai-ds",
    "full_stack": "fake frontend/fs",
    "machine_learning": "fake frontend/ml",
    "game_developer": "fake frontend/gd",
    "software_architect": "fake frontend/sa"
}

# Store user profiles and personalized data
user_data = {}


@app.route('/api/roadmap/preset/<role_key>', methods=['GET'])
def get_preset_roadmap(role_key):
    """Get the preset roadmap for a role"""
    try:
        roadmap_file = PRESET_ROADMAPS.get(role_key)
        if not roadmap_file:
            return jsonify({'error': 'Role not found'}), 404
        
        roadmap_path = project_root / roadmap_file
        with open(roadmap_path, 'r', encoding='utf-8') as f:
            roadmap_text = f.read()
        
        return jsonify({
            'role': role_key,
            'role_name': ROLE_GUIDES[role_key],
            'roadmap': roadmap_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """Start a new conversation for a role"""
    try:
        data = request.json
        role_key = data.get('role')
        
        print(f"\n=== Starting conversation for role: {role_key} ===")
        
        if not role_key:
            return jsonify({'error': 'Role required'}), 400
        
        # Check if role exists
        if role_key not in ROLE_GUIDES:
            print(f"ERROR: Role {role_key} not found in ROLE_GUIDES")
            print(f"Available roles: {list(ROLE_GUIDES.keys())}")
            return jsonify({'error': f'Unknown role: {role_key}'}), 400
        
        print(f"Creating GeminiConversationEngine for {role_key}...")
        
        # Create new conversation engine
        engine = GeminiConversationEngine(role_key)
        print("✓ Engine created")
        
        # Store in active conversations (use session ID in production)
        session_id = role_key  # Simplified for demo
        conversations[session_id] = engine
        print(f"✓ Stored in conversations dict")
        
        # Get first message
        print("Getting first message from engine...")
        first_message = engine.step("")
        print(f"✓ First message received: {first_message[:100]}...")
        
        print("=== Conversation started successfully ===")
        
        return jsonify({
            'session_id': session_id,
            'message': first_message
        })
    except Exception as e:
        import traceback
        print("\n=== ERROR in start_conversation ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        traceback.print_exc()
        print("===================================\n")
        return jsonify({'error': f'{type(e).__name__}: {str(e)}'}), 500


@app.route('/api/conversation/message', methods=['POST'])
def send_message():
    """Send a message in the conversation"""
    try:
        data = request.json
        role_key = data.get('role')
        message = data.get('message')
        
        print(f"\n=== Processing message for role: {role_key} ===")
        print(f"Message: {message[:100] if message else 'None'}...")
        
        if not role_key or not message:
            return jsonify({'error': 'Role and message required'}), 400
        
        # Get conversation engine
        session_id = role_key  # Simplified for demo
        engine = conversations.get(session_id)
        
        if not engine:
            print(f"ERROR: No active conversation found for {session_id}")
            print(f"Active conversations: {list(conversations.keys())}")
            return jsonify({'error': 'No active conversation. Please start over.'}), 404
        
        print("Processing message through engine...")
        # Process message
        response = engine.step(message)
        print(f"✓ Response received: {response[:100]}...")
        
        print("=== Message processed successfully ===")
        
        return jsonify({
            'message': response
        })
    except Exception as e:
        import traceback
        print("\n=== ERROR in send_message ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        traceback.print_exc()
        print("===========================\n")
        return jsonify({'error': f'{type(e).__name__}: {str(e)}'}), 500


@app.route('/api/roadmap/personalize', methods=['POST'])
def personalize_roadmap():
    """Generate personalized roadmap"""
    try:
        data = request.json
        role_key = data.get('role')
        
        print(f"\n=== Personalizing roadmap for role: {role_key} ===")
        
        if not role_key:
            return jsonify({'error': 'Role required'}), 400
        
        # Get conversation engine and profile
        session_id = role_key
        engine = conversations.get(session_id)
        
        if not engine:
            print(f"ERROR: No active conversation found for {session_id}")
            print(f"Active conversations: {list(conversations.keys())}")
            return jsonify({'error': 'No active conversation. Please start over.'}), 404
        
        print("✓ Got conversation engine")
        user_profile = engine.get_profile()
        print(f"✓ User profile: {user_profile}")
        
        # Run personalizer
        print("Running personalizer...")
        personalized_data = personalize(role_key, user_profile)
        print(f"✓ Personalized {len(personalized_data.get('skills', []))} skills")
        
        # Load preset roadmap
        roadmap_file = PRESET_ROADMAPS.get(role_key)
        roadmap_path = project_root / roadmap_file
        print(f"Loading preset roadmap from: {roadmap_path}")
        
        with open(roadmap_path, 'r', encoding='utf-8') as f:
            preset_roadmap = f.read()
        print(f"✓ Loaded preset roadmap ({len(preset_roadmap)} chars)")
        
        # Generate updated roadmap
        print("Generating updated roadmap with LLM...")
        updated_roadmap = update_roadmap(preset_roadmap, personalized_data, user_profile)
        print(f"✓ Generated updated roadmap ({len(updated_roadmap)} chars)")
        
        # Store data
        user_data[session_id] = {
            'profile': user_profile,
            'personalized': personalized_data,
            'roadmap': updated_roadmap
        }
        print(f"✓ Stored data for session {session_id}")
        
        # Clean up conversation
        if session_id in conversations:
            del conversations[session_id]
            print("✓ Cleaned up conversation")
        
        print("=== Personalization complete! ===")
        
        return jsonify({
            'roadmap': updated_roadmap,
            'profile': user_profile
        })
    except Exception as e:
        import traceback
        print("\n=== ERROR in personalize_roadmap ===")
        traceback.print_exc()
        print("=================================\n")
        return jsonify({'error': f'{type(e).__name__}: {str(e)}'}), 500


@app.route('/api/roadmap/download/<role_key>', methods=['GET'])
def download_roadmap(role_key):
    """Download personalized roadmap"""
    try:
        session_id = role_key
        data = user_data.get(session_id)
        
        if not data:
            return jsonify({'error': 'No roadmap found'}), 404
        
        # Save to temp file
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        roadmap_path = output_dir / f"{role_key}_roadmap.txt"
        with open(roadmap_path, 'w', encoding='utf-8') as f:
            f.write(data['roadmap'])
        
        return send_file(
            roadmap_path,
            as_attachment=True,
            download_name=f"{role_key}_roadmap.txt"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("\n🚀 Starting Personalized Learning Roadmap API Server")
    print("📍 Server running at: http://localhost:5000")
    print("🌐 Frontend should be served separately\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
