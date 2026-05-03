#!/usr/bin/env python3
"""
Project setup script to create the chatbot directory structure
"""
import os
import json

# Define the project root
PROJECT_ROOT = "/vercel/share/v0-project"
CHATBOT_DIR = os.path.join(PROJECT_ROOT, "chatbot")

# Create directories
directories = [
    os.path.join(CHATBOT_DIR, "modules"),
    os.path.join(CHATBOT_DIR, "logs"),
    os.path.join(CHATBOT_DIR, "static"),
    os.path.join(CHATBOT_DIR, "templates"),
]

for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

print("Project structure created successfully!")
