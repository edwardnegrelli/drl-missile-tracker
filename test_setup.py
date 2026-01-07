#!/usr/bin/env python3
"""Test that all packages installed correctly"""

import os
from dotenv import load_dotenv

def test_imports():
    """Test all required packages"""
    packages = [
        'pandas',
        'numpy', 
        'requests',
        'feedparser',
        'networkx',
        'plotly',
        'streamlit',
        'anthropic',
        'sqlalchemy',
        'arxiv'
    ]
    
    print("Testing package imports...\n")
    failed = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package} - FAILED: {e}")
            failed.append(package)
    
    print("\n" + "="*50)
    if not failed:
        print(f"✅ SUCCESS! All {len(packages)} packages imported correctly")
        return True
    else:
        print(f"❌ {len(failed)} packages failed")
        print(f"Failed: {', '.join(failed)}")
        return False

def test_api():
    """Test API key is configured"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if api_key and api_key.startswith("sk-ant-"):
        print("✅ API key configured correctly")
        return True
    else:
        print("❌ API key not found or invalid")
        print("Make sure .env file exists with ANTHROPIC_API_KEY")
        return False

if __name__ == '__main__':
    print("="*50)
    print("DRL Missile Tracker - Setup Test")
    print("="*50 + "\n")
    
    imports_ok = test_imports()
    print()
    api_ok = test_api()
    
    print("\n" + "="*50)
    if imports_ok and api_ok:
        print("🎉 Setup complete! You're ready to start.")
    else:
        print("⚠️  Some issues need attention (see above)")
    print("="*50)