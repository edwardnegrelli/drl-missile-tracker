#!/usr/bin/env python3
"""Test API connection"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

def test_api():
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        print("Make sure .env file exists with ANTHROPIC_API_KEY")
        return False
    
    print(f"✓ API key loaded")
    print(f"  Starts with: {api_key[:20]}...")
    print(f"  Length: {len(api_key)} characters")
    
    print("\nTesting API connection...")
    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Reply with exactly: API test successful"}
            ]
        )
        
        response = message.content[0].text
        print(f"✓ API Response: {response}")
        print(f"\n✅ API connection working!")
        print(f"✓ Used {message.usage.input_tokens} input tokens, {message.usage.output_tokens} output tokens")
        print(f"✓ Cost: ~$0.0001")
        return True
        
    except Exception as e:
        print(f"\n❌ API call failed:")
        print(f"   {e}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Testing Anthropic API Connection")
    print("="*60 + "\n")
    test_api()
    print("\n" + "="*60)