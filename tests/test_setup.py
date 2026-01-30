# test_setup.py
import sys
print(f"Python version: {sys.version}")

try:
    import pandas as pd
    import numpy as np
    import sklearn
    print("✅ Core libraries installed")
except ImportError as e:
    print(f"❌ Missing library: {e}")

try:
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv('RIOT_API_KEY')
    
    if api_key and api_key != 'your_riot_api_key_here':
        print(f"✅ API key configured (first 10 chars: {api_key[:10]}...)")
    else:
        print("⚠️  API key not configured in .env")
except Exception as e:
    print(f"❌ Config error: {e}")

print("\n🎉 Setup complete! Ready to start coding.")