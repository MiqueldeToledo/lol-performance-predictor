"""
Configuration Module
====================
Loads configuration from environment variables (.env file).

Usage:
    >>> from src.utils.config import Config
    >>> print(Config.RIOT_API_KEY)
    >>> print(Config.RIOT_REGION)
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from project root
# This will look for .env in the current directory and parent directories
load_dotenv()


class Config:
    """
    Configuration class that loads all settings from environment variables.
    
    All values are loaded from the .env file.
    See .env.example for required variables.
    """
    
    # ==================== RIOT API SETTINGS ====================
    RIOT_API_KEY = os.getenv('RIOT_API_KEY')
    RIOT_API_BASE_URL = os.getenv('RIOT_API_BASE_URL', 'https://americas.api.riotgames.com')
    RIOT_REGION = os.getenv('RIOT_REGION', 'na1')
    
    # ==================== DATA COLLECTION SETTINGS ====================
    MAX_MATCHES_PER_RUN = int(os.getenv('MAX_MATCHES_PER_RUN', 1000))
    MATCHES_PER_PLAYER = int(os.getenv('MATCHES_PER_PLAYER', 20))
    TARGET_RANK = os.getenv('TARGET_RANK', 'DIAMOND')
    
    # Valid ranks: IRON, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER, GRANDMASTER, CHALLENGER
    VALID_RANKS = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 
                   'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    
    # ==================== RATE LIMITING ====================
    REQUESTS_PER_SECOND = int(os.getenv('REQUESTS_PER_SECOND', 20))
    REQUESTS_PER_2_MINUTES = int(os.getenv('REQUESTS_PER_2_MINUTES', 100))
    
    # ==================== MODEL SETTINGS ====================
    MODEL_PATH = os.getenv('MODEL_PATH', 'data/models/')
    RANDOM_STATE = int(os.getenv('RANDOM_STATE', 42))
    TEST_SIZE = float(os.getenv('TEST_SIZE', 0.2))
    
    # ==================== API SERVER SETTINGS ====================
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # ==================== LOGGING SETTINGS ====================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # ==================== PATH SETTINGS ====================
    # Get the project root directory
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    MODELS_DIR = DATA_DIR / 'models'
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            True if all required config is valid, False otherwise
        """
        errors = []
        
        # Check API key
        if not cls.RIOT_API_KEY:
            errors.append("RIOT_API_KEY is not set in .env file")
        elif cls.RIOT_API_KEY == 'your_riot_api_key_here':
            errors.append("RIOT_API_KEY still has placeholder value. Please update .env")
        
        # Check region
        valid_regions = ['na1', 'euw1', 'eun1', 'kr', 'br1', 'jp1', 'la1', 'la2', 'oc1', 'tr1', 'ru']
        if cls.RIOT_REGION not in valid_regions:
            errors.append(f"RIOT_REGION must be one of {valid_regions}")
        
        # Check target rank
        if cls.TARGET_RANK not in cls.VALID_RANKS:
            errors.append(f"TARGET_RANK must be one of {cls.VALID_RANKS}")
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        print("✅ Configuration validated successfully")
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (without exposing full API key)."""
        print("\n" + "="*60)
        print("CURRENT CONFIGURATION")
        print("="*60)
        
        # Display API settings (mask the key)
        api_key_display = cls.RIOT_API_KEY[:10] + "..." if cls.RIOT_API_KEY else "NOT SET"
        print(f"\n🔑 API Settings:")
        print(f"   API Key: {api_key_display}")
        print(f"   Region: {cls.RIOT_REGION}")
        
        print(f"\n📊 Data Collection:")
        print(f"   Max Matches: {cls.MAX_MATCHES_PER_RUN}")
        print(f"   Matches per Player: {cls.MATCHES_PER_PLAYER}")
        print(f"   Target Rank: {cls.TARGET_RANK}")
        
        print(f"\n⚙️  Rate Limiting:")
        print(f"   Requests/second: {cls.REQUESTS_PER_SECOND}")
        print(f"   Requests/2min: {cls.REQUESTS_PER_2_MINUTES}")
        
        print(f"\n🤖 Model Settings:")
        print(f"   Random State: {cls.RANDOM_STATE}")
        print(f"   Test Size: {cls.TEST_SIZE}")
        print(f"   Model Path: {cls.MODEL_PATH}")
        
        print(f"\n📁 Paths:")
        print(f"   Project Root: {cls.PROJECT_ROOT}")
        print(f"   Raw Data: {cls.RAW_DATA_DIR}")
        print(f"   Processed Data: {cls.PROCESSED_DATA_DIR}")
        
        print("\n" + "="*60 + "\n")


# Validate configuration on import (optional - can comment out if annoying)
# Config.validate()


if __name__ == "__main__":
    """Test configuration loading."""
    print("🔧 Testing configuration...\n")
    
    # Display current config
    Config.display()
    
    # Validate
    if Config.validate():
        print("\n✅ Configuration is ready to use!")
    else:
        print("\n❌ Please fix configuration errors in .env file")