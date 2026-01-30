"""
Test API Connection
===================
Quick script to test if your Riot API setup is working correctly.

Run this after setting up your .env file to verify everything works.

Usage:
    python test_api_connection.py
"""

import os
import sys
from pathlib import Path

# Add src directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_imports():
    """Test that all required packages are installed."""
    print("📦 Testing imports...")
    
    required_packages = [
        ('requests', 'HTTP library'),
        ('dotenv', 'Environment variable loader'),
        ('pandas', 'Data manipulation'),
        ('numpy', 'Numerical computing'),
    ]
    
    missing_packages = []
    
    for package_name, description in required_packages:
        try:
            __import__(package_name)
            print(f"   ✅ {package_name} - {description}")
        except ImportError:
            print(f"   ❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed\n")
    return True


def test_env_file():
    """Test that .env file exists and has required variables."""
    print("📄 Testing .env file...")
    
    if not Path('.env').exists():
        print("   ❌ .env file not found")
        print("   Create one by copying .env.example:")
        print("   cp .env.example .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Check for API key
    api_key = os.getenv('RIOT_API_KEY')
    region = os.getenv('RIOT_REGION', 'na1')
    
    if not api_key:
        print("   ❌ RIOT_API_KEY not found in .env")
        return False
    
    if api_key == 'your_riot_api_key_here':
        print("   ❌ RIOT_API_KEY still has placeholder value")
        print("   Update .env with your actual API key from developer.riotgames.com")
        return False
    
    print(f"   ✅ RIOT_API_KEY configured (starts with: {api_key[:10]}...)")
    print(f"   ✅ RIOT_REGION set to: {region}\n")
    
    return True


def test_api_connection():
    """Test actual API connection."""
    print("🌐 Testing Riot API connection...")
    
    try:
        # Import our RiotAPI wrapper
        # Assume riot_api.py is in src/data_collection/
        from src.data_collection.riot_api import RiotAPI, RiotAPIError
        
        api_key = os.getenv('RIOT_API_KEY')
        region = os.getenv('RIOT_REGION', 'na1')
        
        api = RiotAPI(api_key=api_key, region=region)
        
        # Try to get a well-known player using Riot ID
        print("   🔍 Attempting to fetch account data...")
        account = api.get_account_by_riot_id("Doublelift", "NA1")
        
        print(f"   ✅ Successfully fetched account: {account['gameName']}#{account['tagLine']}")
        print(f"   ✅ PUUID: {account['puuid'][:20]}...")
        
        # Now get summoner details using the PUUID
        print("   🔍 Fetching summoner details...")
        summoner = api.get_summoner_by_puuid(account['puuid'])
        print(f"   ✅ Level: {summoner['summonerLevel']}")
        
        # Try to get match IDs
        print("\n   🔍 Attempting to fetch match history...")
        match_ids = api.get_match_ids(account['puuid'], count=5)
        print(f"   ✅ Found {len(match_ids)} recent matches")
        
        if match_ids:
            print(f"   ✅ Latest match ID: {match_ids[0]}")
        
        print("\n✅ API connection successful!\n")
        return True
        
    except ImportError as e:
        print(f"   ❌ Failed to import RiotAPI: {e}")
        print("   Make sure riot_api.py is in src/data_collection/")
        return False
    
    except RiotAPIError as e:
        print(f"   ❌ API Error: {e}")
        return False
    
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False


def test_directory_structure():
    """Test that directory structure is correct."""
    print("📁 Testing directory structure...")
    
    required_dirs = [
        'src',
        'src/data_collection',
        'src/preprocessing',
        'src/models',
        'src/utils',
        'data',
        'data/raw',
        'data/processed',
        'data/models',
        'tests',
        'notebooks',
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - MISSING")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️  Missing directories: {', '.join(missing_dirs)}")
        print("Run setup_project.py to create them")
        return False
    
    print("✅ All directories present\n")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 RIOT API SETUP VERIFICATION")
    print("="*70 + "\n")
    
    tests = [
        ("Package Installation", test_imports),
        ("Environment Configuration", test_env_file),
        ("Directory Structure", test_directory_structure),
        ("API Connection", test_api_connection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"   ❌ Test crashed: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70 + "\n")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Score: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! You're ready to start collecting data!\n")
        print("Next steps:")
        print("   1. Run: python scripts/collect_data.py")
        print("   2. Or create a Jupyter notebook to explore the API")
        print("   3. Check out notebooks/01_eda.ipynb for examples\n")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)