"""
Riot Games API Wrapper
======================
A comprehensive wrapper for the Riot Games API with rate limiting,
error handling, and common endpoints for League of Legends data.

Author: Miquel de Toledo Mestres
Date: January 2026
"""

import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter to respect Riot API limits.
    
    Riot Development API Limits:
    - 20 requests per second
    - 100 requests per 2 minutes
    """
    
    def __init__(self, requests_per_second: int = 20, requests_per_2min: int = 100):
        self.requests_per_second = requests_per_second
        self.requests_per_2min = requests_per_2min
        
        # Track request timestamps
        self.second_requests = []
        self.two_min_requests = []
        
    def wait_if_needed(self):
        """Wait if we're about to exceed rate limits."""
        now = datetime.now()
        
        # Clean old timestamps (older than 2 minutes)
        cutoff_2min = now - timedelta(minutes=2)
        self.two_min_requests = [ts for ts in self.two_min_requests if ts > cutoff_2min]
        
        # Clean old timestamps (older than 1 second)
        cutoff_1sec = now - timedelta(seconds=1)
        self.second_requests = [ts for ts in self.second_requests if ts > cutoff_1sec]
        
        # Check if we need to wait
        if len(self.second_requests) >= self.requests_per_second:
            sleep_time = 1.0 - (now - self.second_requests[0]).total_seconds()
            if sleep_time > 0:
                logger.debug(f"Rate limit: sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)
        
        if len(self.two_min_requests) >= self.requests_per_2min:
            sleep_time = 120 - (now - self.two_min_requests[0]).total_seconds()
            if sleep_time > 0:
                logger.warning(f"2-minute rate limit: sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)
        
        # Record this request
        now = datetime.now()
        self.second_requests.append(now)
        self.two_min_requests.append(now)


class RiotAPIError(Exception):
    """Custom exception for Riot API errors."""
    pass


class RiotAPI:
    """
    Wrapper for Riot Games API.
    
    Provides methods to fetch:
    - Summoner information
    - Match history
    - Match details
    - Champion information
    - Ranked data
    
    Usage:
        >>> from riot_api import RiotAPI
        >>> api = RiotAPI(api_key="YOUR_KEY", region="na1")
        >>> summoner = api.get_summoner_by_name("Doublelift")
        >>> print(summoner['name'], summoner['summonerLevel'])
    """
    
    # Base URLs for different API endpoints
    PLATFORM_URLS = {
        'na1': 'https://na1.api.riotgames.com',
        'euw1': 'https://euw1.api.riotgames.com',
        'kr': 'https://kr.api.riotgames.com',
        'br1': 'https://br1.api.riotgames.com',
        'eun1': 'https://eun1.api.riotgames.com',
        'jp1': 'https://jp1.api.riotgames.com',
        'la1': 'https://la1.api.riotgames.com',
        'la2': 'https://la2.api.riotgames.com',
        'oc1': 'https://oc1.api.riotgames.com',
        'tr1': 'https://tr1.api.riotgames.com',
        'ru': 'https://ru.api.riotgames.com',
    }
    
    REGIONAL_URLS = {
        'americas': 'https://americas.api.riotgames.com',
        'europe': 'https://europe.api.riotgames.com',
        'asia': 'https://asia.api.riotgames.com',
    }
    
    # Map platform to regional routing
    PLATFORM_TO_REGION = {
        'na1': 'americas', 'br1': 'americas', 'la1': 'americas', 'la2': 'americas',
        'euw1': 'europe', 'eun1': 'europe', 'tr1': 'europe', 'ru': 'europe',
        'kr': 'asia', 'jp1': 'asia', 'oc1': 'asia',
    }
    
    def __init__(self, api_key: str, region: str = 'na1', 
                 rate_limit: bool = True, max_retries: int = 3):
        """
        Initialize the Riot API wrapper.
        
        Args:
            api_key: Your Riot API key from developer.riotgames.com
            region: Server region (na1, euw1, kr, etc.)
            rate_limit: Whether to enforce rate limiting
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.api_key = api_key
        self.region = region.lower()
        self.max_retries = max_retries
        
        # Validate region
        if self.region not in self.PLATFORM_URLS:
            raise ValueError(f"Invalid region: {region}. Must be one of {list(self.PLATFORM_URLS.keys())}")
        
        # Set base URLs
        self.platform_url = self.PLATFORM_URLS[self.region]
        self.regional_url = self.REGIONAL_URLS[self.PLATFORM_TO_REGION[self.region]]
        
        # Set up rate limiter
        self.rate_limiter = RateLimiter() if rate_limit else None
        
        # Request headers
        self.headers = {
            'X-Riot-Token': self.api_key,
            'Accept': 'application/json',
        }
        
        logger.info(f"RiotAPI initialized for region: {self.region}")
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the Riot API with retry logic and rate limiting.
        
        Args:
            url: Full URL to request
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            RiotAPIError: If request fails after all retries
        """
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                
                # Handle different status codes
                if response.status_code == 200:
                    return response.json()
                
                elif response.status_code == 404:
                    raise RiotAPIError(f"Resource not found: {url}")
                
                elif response.status_code == 403:
                    logger.error(
                        "API request failed: Invalid API key or forbidden access",
                        extra={
                            'url': url,
                            'api_key': self.api_key[:10],
                            'status_code': response.status_code,
                            'response': response.text
                        }
                    )
                    raise RiotAPIError(f"Invalid API key or forbidden access. Response: {response.text}")
                
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                elif response.status_code >= 500:
                    # Server error - retry
                    logger.warning(f"Server error {response.status_code}. Attempt {attempt + 1}/{self.max_retries}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                
                else:
                    raise RiotAPIError(f"Unexpected status code {response.status_code}: {response.text}")
            
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout. Attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RiotAPIError("Request timed out after all retries")
            
            except requests.exceptions.RequestException as e:
                raise RiotAPIError(f"Request failed: {str(e)}")
        
        raise RiotAPIError(f"Failed after {self.max_retries} attempts")
    
    # ==================== SUMMONER ENDPOINTS ====================
    
    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Dict[str, Any]:
        """
        Get account information by Riot ID (game name + tag line).
        This is the new recommended way to look up players.
        
        Args:
            game_name: The game name (e.g., "Doublelift")
            tag_line: The tag line (e.g., "NA1")
            
        Returns:
            Dictionary with account info including puuid
        """
        import urllib.parse
        game_name_encoded = urllib.parse.quote(game_name)
        tag_line_encoded = urllib.parse.quote(tag_line)
        url = f"{self.regional_url}/riot/account/v1/accounts/by-riot-id/{game_name_encoded}/{tag_line_encoded}"
        logger.info(f"Fetching account: {game_name}#{tag_line}")
        return self._make_request(url)
    
    def get_summoner_by_name(self, summoner_name: str) -> Dict[str, Any]:
        """
        Get summoner information by summoner name.
        
        DEPRECATED: This endpoint may not work for all accounts.
        Use get_account_by_riot_id() instead with game_name#tag_line format.
        
        Args:
            summoner_name: In-game summoner name
            
        Returns:
            Dictionary with summoner info (id, accountId, puuid, name, summonerLevel, etc.)
        """
        import urllib.parse
        summoner_name_encoded = urllib.parse.quote(summoner_name)
        url = f"{self.platform_url}/lol/summoner/v4/summoners/by-name/{summoner_name_encoded}"
        logger.info(f"Fetching summoner: {summoner_name}")
        return self._make_request(url)
    
    def get_summoner_by_puuid(self, puuid: str) -> Dict[str, Any]:
        """Get summoner information by PUUID."""
        url = f"{self.platform_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        return self._make_request(url)
    
    # ==================== MATCH ENDPOINTS ====================
    
    def get_match_ids(self, puuid: str, start: int = 0, count: int = 20,
                     queue: Optional[int] = None, type: Optional[int] = None) -> List[str]:
        """
        Get list of match IDs for a summoner.
        
        Args:
            puuid: Player UUID
            start: Start index (for pagination)
            count: Number of matches to return (max 100)
            queue: Queue ID filter (420 = ranked solo, 440 = ranked flex)
            type: Match type filter (integer value)
            
        Returns:
            List of match IDs
        """
        url = f"{self.regional_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        
        params = {
            'start': start,
            'count': min(count, 100),  # API max is 100
        }
        
        if queue:
            params['queue'] = queue
        if type is not None:
            params['type'] = type
        
        logger.info(f"Fetching match IDs for PUUID: {puuid[:8]}... (start={start}, count={count})")
        result = self._make_request(url, params)
        if not isinstance(result, list):
            raise RiotAPIError(f"Expected a list of match IDs, got: {__builtins__.type(result)}")
        return result
    
    def get_match(self, match_id: str) -> Dict[str, Any]:
        """
        Get detailed match information.
        
        Args:
            match_id: Match ID (format: REGION_MATCHID, e.g., 'NA1_1234567890')
            
        Returns:
            Detailed match data including timeline, participants, and stats
        """
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}"
        logger.info(f"Fetching match: {match_id}")
        return self._make_request(url)
    
    def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        """
        Get match timeline (detailed events by minute).
        
        Args:
            match_id: Match ID
            
        Returns:
            Timeline data with frame-by-frame events
        """
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}/timeline"
        return self._make_request(url)
    
    # ==================== RANKED ENDPOINTS ====================
    
    def get_ranked_entries(self, summoner_id: str) -> List[Dict[str, Any]]:
        """
        Get ranked information for a summoner.
        
        Args:
            summoner_id: Summoner ID (not PUUID)
            
        Returns:
            List of ranked entries (one per queue type)
        """
        url = f"{self.platform_url}/lol/league/v4/entries/by-summoner/{summoner_id}"
        result = self._make_request(url)
        if isinstance(result, list):
            return result
        elif isinstance(result, dict):
            # If the API returns a dict (e.g., error), return an empty list or handle as needed
            logger.warning(f"Expected a list for ranked entries, got dict: {result}")
            return []
        else:
            logger.warning(f"Unexpected response type for ranked entries: {type(result)}")
            return []
    
    def get_challenger_league(self, queue: str = 'RANKED_SOLO_5x5') -> Dict[str, Any]:
        """
        Get the Challenger league for a queue.
        
        Args:
            queue: Queue type ('RANKED_SOLO_5x5' or 'RANKED_FLEX_SR')
            
        Returns:
            Challenger league data
        """
        url = f"{self.platform_url}/lol/league/v4/challengerleagues/by-queue/{queue}"
        return self._make_request(url)
    
    # ==================== UTILITY METHODS ====================
    
    def get_player_recent_matches(self, summoner_name: str, count: int = 20) -> List[Dict[str, Any]]:
        """
        Convenience method to get recent matches for a summoner by name.
        
        Args:
            summoner_name: Summoner name
            count: Number of matches to fetch
            
        Returns:
            List of detailed match data
        """
        # Get summoner info
        summoner = self.get_summoner_by_name(summoner_name)
        puuid = summoner['puuid']
        
        # Get match IDs
        match_ids = self.get_match_ids(puuid, count=count)
        
        # Get match details
        matches = []
        for i, match_id in enumerate(match_ids, 1):
            logger.info(f"Fetching match {i}/{len(match_ids)}")
            try:
                match_data = self.get_match(match_id)
                matches.append(match_data)
            except RiotAPIError as e:
                logger.error(f"Failed to fetch match {match_id}: {e}")
                continue
        
        return matches
    
    def test_connection(self) -> bool:
        """
        Test if API key is valid and connection works.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get a well-known account using Riot ID
            self.get_account_by_riot_id("Doublelift", "NA1")
            logger.info("✅ API connection test successful")
            return True
        except RiotAPIError as e:
            logger.error(f"❌ API connection test failed: {e}")
            return False


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    """
    Example usage of the RiotAPI wrapper.
    Run this file directly to test your API connection.
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('RIOT_API_KEY')
    region = os.getenv('RIOT_REGION', 'na1')
    
    if not api_key:
        print("❌ Error: RIOT_API_KEY not found in .env file")
        print("Please add your API key to .env file")
        exit(1)
    
    # Initialize API
    print(f"🔧 Initializing Riot API for region: {region}")
    api = RiotAPI(api_key=api_key, region=region)
    
    # Example 1: Get account by Riot ID
    print("\n📊 Fetching account: Doublelift#NA1")
    try:
        account = api.get_account_by_riot_id("Doublelift", "NA1")
        print(f"   Account: {account['gameName']}#{account['tagLine']}")
        print(f"   PUUID: {account['puuid'][:20]}...")
        
        # Get summoner details
        print(f"\n🔍 Fetching summoner details...")
        summoner = api.get_summoner_by_puuid(account['puuid'])
        print(f"   Level: {summoner['summonerLevel']}")
        
        # Example 2: Get recent matches
        print(f"\n📜 Fetching last 5 matches...")
        match_ids = api.get_match_ids(account['puuid'], count=5)
        print(f"   Found {len(match_ids)} matches")
        
        # Example 3: Get detailed match info
        if match_ids:
            print(f"\n🎮 Fetching details for first match...")
            match = api.get_match(match_ids[0])
            print(f"   Match ID: {match['metadata']['matchId']}")
            print(f"   Game Mode: {match['info']['gameMode']}")
            print(f"   Duration: {match['info']['gameDuration'] // 60} minutes")
            print(f"   Participants: {len(match['info']['participants'])}")
        
        print("\n✅ All tests passed!")
        
    except RiotAPIError as e:
        print(f"❌ Error: {e}")