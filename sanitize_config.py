#!/usr/bin/env python3
import sys
import re

# Read the file
content = sys.stdin.read()

# Pattern to find the hardcoded token line
pattern = r'HF_API_TOKEN\s*=\s*"hf_[A-Za-z0-9]+"'

# Replacement with environment variable
replacement = '''from dotenv import load_dotenv

load_dotenv()

#models
HF_API_TOKEN = os.getenv("HF_API_TOKEN")'''

# Check if the pattern exists
if re.search(pattern, content):
    # Replace the hardcoded token with env var loading
    content = re.sub(pattern, replacement, content)
    
    # Make sure we have the import at the top if not already there
    if 'from dotenv import load_dotenv' not in content and 'import os' in content:
        # Already handled in replacement above
        pass

sys.stdout.write(content)
