# 🎮 Riot API Wrapper - Usage Guide

## 📦 What You Got

I created **3 essential files** for you:

1. **`riot_api.py`** - The main API wrapper class
2. **`config.py`** - Configuration loader
3. **`test_api_connection.py`** - Test script

## 📍 Where to Put These Files

```
lol-performance-predictor/
├── src/
│   ├── data_collection/
│   │   └── riot_api.py        ← PUT THIS HERE
│   └── utils/
│       └── config.py          ← PUT THIS HERE
└── test_api_connection.py     ← PUT THIS HERE (project root)
```

## 🚀 Quick Setup (5 Steps)

### Step 1: Place the Files
```bash
# From where you downloaded the files:
mv riot_api.py lol-performance-predictor/src/data_collection/
mv config.py lol-performance-predictor/src/utils/
mv test_api_connection.py lol-performance-predictor/
```

### Step 2: Verify Your .env File
Make sure your `.env` looks like this:
```bash
RIOT_API_KEY=RGAPI-12345678-abcd-1234-abcd-123456789abc  # Your actual key
RIOT_REGION=na1
MAX_MATCHES_PER_RUN=1000
TARGET_RANK=DIAMOND
```

### Step 3: Create `__init__.py` Files
```bash
# Make sure these exist (should already be there):
touch src/__init__.py
touch src/data_collection/__init__.py
touch src/utils/__init__.py
```

### Step 4: Test Configuration
```bash
cd lol-performance-predictor
python src/utils/config.py
```

You should see:
```
✅ Configuration validated successfully
```

### Step 5: Test API Connection
```bash
python test_api_connection.py
```

Expected output:
```
🧪 RIOT API SETUP VERIFICATION
===============================

📦 Testing imports...
   ✅ requests - HTTP library
   ✅ dotenv - Environment variable loader
   ...

📄 Testing .env file...
   ✅ .env file exists
   ✅ RIOT_API_KEY configured
   ...

🌐 Testing Riot API connection...
   ✅ Successfully fetched summoner: Doublelift
   ✅ API connection successful!

🎉 All tests passed! You're ready to start collecting data!
```

## 📖 How to Use the API Wrapper

### Basic Usage

```python
from src.data_collection.riot_api import RiotAPI
from src.utils.config import Config

# Initialize API
api = RiotAPI(api_key=Config.RIOT_API_KEY, region=Config.RIOT_REGION)

# Get summoner info
summoner = api.get_summoner_by_name("Doublelift")
print(f"Summoner: {summoner['name']}, Level: {summoner['summonerLevel']}")

# Get match history
match_ids = api.get_match_ids(summoner['puuid'], count=20)
print(f"Found {len(match_ids)} matches")

# Get detailed match data
match = api.get_match(match_ids[0])
print(f"Game duration: {match['info']['gameDuration']} seconds")
```

### Advanced Examples

#### Example 1: Collect 100 Matches for Analysis

```python
from src.data_collection.riot_api import RiotAPI
from src.utils.config import Config
import json
from pathlib import Path

# Initialize
api = RiotAPI(api_key=Config.RIOT_API_KEY, region=Config.RIOT_REGION)

# Get a high-level player
summoner = api.get_summoner_by_name("Faker")
puuid = summoner['puuid']

# Get last 100 match IDs
print("Fetching match IDs...")
match_ids = api.get_match_ids(puuid, count=100)

# Collect detailed data
matches = []
for i, match_id in enumerate(match_ids, 1):
    print(f"Fetching match {i}/{len(match_ids)}: {match_id}")
    try:
        match_data = api.get_match(match_id)
        matches.append(match_data)
    except Exception as e:
        print(f"Error: {e}")
        continue

# Save to file
output_file = Path(Config.RAW_DATA_DIR) / "faker_matches.json"
with open(output_file, 'w') as f:
    json.dump(matches, f, indent=2)

print(f"✅ Saved {len(matches)} matches to {output_file}")
```

#### Example 2: Get Player Stats from Match

```python
from src.data_collection.riot_api import RiotAPI
from src.utils.config import Config

api = RiotAPI(api_key=Config.RIOT_API_KEY, region=Config.RIOT_REGION)

# Get summoner
summoner = api.get_summoner_by_name("Doublelift")

# Get recent match
match_ids = api.get_match_ids(summoner['puuid'], count=1)
match = api.get_match(match_ids[0])

# Find this player's stats in the match
for participant in match['info']['participants']:
    if participant['puuid'] == summoner['puuid']:
        print(f"Champion: {participant['championName']}")
        print(f"KDA: {participant['kills']}/{participant['deaths']}/{participant['assists']}")
        print(f"Win: {participant['win']}")
        print(f"Gold earned: {participant['goldEarned']}")
        print(f"Damage dealt: {participant['totalDamageDealtToChampions']}")
        break
```

#### Example 3: Get Ranked Information

```python
from src.data_collection.riot_api import RiotAPI
from src.utils.config import Config

api = RiotAPI(api_key=Config.RIOT_API_KEY, region=Config.RIOT_REGION)

summoner = api.get_summoner_by_name("Doublelift")

# Get ranked stats
ranked_data = api.get_ranked_entries(summoner['id'])

for queue in ranked_data:
    print(f"Queue: {queue['queueType']}")
    print(f"Tier: {queue['tier']} {queue['rank']}")
    print(f"LP: {queue['leaguePoints']}")
    print(f"Wins: {queue['wins']}, Losses: {queue['losses']}")
    print(f"Win rate: {queue['wins'] / (queue['wins'] + queue['losses']) * 100:.1f}%")
    print()
```

## 🔍 Understanding the API Response

### Summoner Object
```python
{
    'id': 'summoner_encrypted_id',
    'accountId': 'account_encrypted_id', 
    'puuid': 'player_uuid',           # ← Use this for match history
    'name': 'Doublelift',
    'profileIconId': 4568,
    'revisionDate': 1234567890,
    'summonerLevel': 450
}
```

### Match Object (Simplified)
```python
{
    'metadata': {
        'matchId': 'NA1_1234567890',
        'participants': ['puuid1', 'puuid2', ...]  # 10 players
    },
    'info': {
        'gameMode': 'CLASSIC',
        'gameDuration': 1800,  # seconds
        'gameCreation': 1234567890,
        'participants': [
            {
                'puuid': 'player_uuid',
                'championName': 'Jinx',
                'teamId': 100,  # Blue side = 100, Red side = 200
                'win': True,
                'kills': 12,
                'deaths': 3,
                'assists': 8,
                'totalDamageDealtToChampions': 25000,
                'goldEarned': 15000,
                # ... 100+ more stats
            },
            # ... 9 more participants
        ]
    }
}
```

## 🎯 Common Queue IDs

Use these for filtering matches:

```python
QUEUE_IDS = {
    420: 'Ranked Solo/Duo',
    440: 'Ranked Flex',
    400: 'Normal Draft',
    430: 'Normal Blind',
    450: 'ARAM',
    700: 'Clash',
}

# Example: Get only ranked solo matches
match_ids = api.get_match_ids(puuid, count=20, queue=420)
```

## ⚡ Features of the Wrapper

### ✅ Automatic Rate Limiting
- Respects 20 requests/second limit
- Respects 100 requests/2-minute limit
- Automatically waits when needed

### ✅ Retry Logic
- Retries on server errors (500s)
- Exponential backoff
- Handles timeout errors

### ✅ Error Handling
- Custom `RiotAPIError` exceptions
- Clear error messages
- Logging of all requests

### ✅ Convenience Methods
```python
# Get player's recent matches in one call
matches = api.get_player_recent_matches("Doublelift", count=20)

# Test if API key works
if api.test_connection():
    print("API is working!")
```

## 🐛 Troubleshooting

### Error: "Resource not found: ..."
**Cause**: Summoner name doesn't exist or region is wrong  
**Fix**: Check spelling and region setting

### Error: "Invalid API key or forbidden access"
**Cause**: API key is wrong or expired  
**Fix**: 
- Development keys expire every 24 hours
- Get a new key from developer.riotgames.com
- Update .env file

### Error: "Rate limit exceeded"
**Cause**: Too many requests too fast  
**Fix**: The wrapper handles this automatically, but if you see this:
- Wait a few seconds
- Reduce concurrent requests

### Error: "Request timed out"
**Cause**: Riot servers slow or network issues  
**Fix**: The wrapper retries automatically (3 times)

### Error: "ModuleNotFoundError: No module named 'src'"
**Cause**: Python can't find your modules  
**Fix**: Make sure you're running from project root:
```bash
cd lol-performance-predictor
python test_api_connection.py
```

## 📊 Next Steps: Build a Data Collection Script

Now that you have the API wrapper, create your first data collection script!

Create `scripts/collect_data.py`:
```python
from src.data_collection.riot_api import RiotAPI
from src.utils.config import Config
import json
from pathlib import Path
from datetime import datetime

def main():
    # Initialize API
    api = RiotAPI(api_key=Config.RIOT_API_KEY, region=Config.RIOT_REGION)
    
    # Get high-level players (Diamond+)
    challenger = api.get_challenger_league()
    
    # Collect matches from top 10 players
    all_matches = []
    
    for entry in challenger['entries'][:10]:
        summoner = api.get_summoner_by_puuid(entry['puuid'])
        match_ids = api.get_match_ids(summoner['puuid'], count=20)
        
        for match_id in match_ids:
            match = api.get_match(match_id)
            all_matches.append(match)
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Config.RAW_DATA_DIR / f"matches_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(all_matches, f)
    
    print(f"✅ Collected {len(all_matches)} matches!")
    print(f"💾 Saved to {output_file}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python scripts/collect_data.py
```

## 🎓 What You've Learned

By using this API wrapper, you're learning:
- ✅ REST API integration
- ✅ Rate limiting strategies
- ✅ Error handling and retries
- ✅ Object-oriented programming
- ✅ Configuration management
- ✅ Logging and debugging

## 💡 Pro Tips

1. **Save Raw Data**: Always save raw API responses before processing
2. **Use PUUID**: It's more stable than summoner names (which can change)
3. **Filter by Queue**: Focus on ranked games (queue 420) for better data quality
4. **Respect Rate Limits**: Even though wrapper handles it, don't abuse the API
5. **Cache Results**: Don't fetch the same match twice

## 🚀 Ready to Code?

You now have a **production-ready API wrapper**! 

**What to build next?**
- Data collection script
- Jupyter notebook for exploration
- Database to store matches
- Analysis pipeline

Need help with any of these? Just ask! 🎉