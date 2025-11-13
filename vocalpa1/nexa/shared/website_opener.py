"""
Nexa Website Opener Module
Handles opening websites with intelligent matching and fuzzy search
Ported from VocalPA config.js with 100+ websites
"""

import webbrowser
import re
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)

class WebsiteOpener:
    def __init__(self):
        # Complete website database ported from VocalPA
        self.websites = {
            # Social Media
            'youtube': 'https://youtube.com',
            'facebook': 'https://facebook.com',
            'fb': 'https://facebook.com',
            'instagram': 'https://instagram.com',
            'insta': 'https://instagram.com',
            'twitter': 'https://twitter.com',
            'x': 'https://x.com',
            'snapchat': 'https://snapchat.com',
            'tiktok': 'https://tiktok.com',
            'linkedin': 'https://linkedin.com',
            'reddit': 'https://reddit.com',
            'discord': 'https://discord.com',
            'telegram': 'https://web.telegram.org',
            'whatsapp': 'https://web.whatsapp.com',
            'pinterest': 'https://pinterest.com',
            'tumblr': 'https://tumblr.com',
            
            # Google Services
            'google': 'https://google.com',
            'gmail': 'https://gmail.com',
            'google drive': 'https://drive.google.com',
            'drive': 'https://drive.google.com',
            'google docs': 'https://docs.google.com',
            'docs': 'https://docs.google.com',
            'google sheets': 'https://sheets.google.com',
            'sheets': 'https://sheets.google.com',
            'google slides': 'https://slides.google.com',
            'slides': 'https://slides.google.com',
            'google maps': 'https://maps.google.com',
            'maps': 'https://maps.google.com',
            'google photos': 'https://photos.google.com',
            'photos': 'https://photos.google.com',
            'google calendar': 'https://calendar.google.com',
            'calendar': 'https://calendar.google.com',
            'google meet': 'https://meet.google.com',
            'meet': 'https://meet.google.com',
            'google translate': 'https://translate.google.com',
            'translate': 'https://translate.google.com',
            'google pay': 'https://pay.google.com',
            'gpay': 'https://pay.google.com',
            'youtube music': 'https://music.youtube.com',
            
            # Entertainment & Streaming
            'netflix': 'https://netflix.com',
            'amazon prime': 'https://primevideo.com',
            'prime video': 'https://primevideo.com',
            'disney plus': 'https://disneyplus.com',
            'disney': 'https://disneyplus.com',
            'hotstar': 'https://hotstar.com',
            'hulu': 'https://hulu.com',
            'hbo max': 'https://hbomax.com',
            'spotify': 'https://spotify.com',
            'apple music': 'https://music.apple.com',
            'soundcloud': 'https://soundcloud.com',
            'twitch': 'https://twitch.tv',
            'vimeo': 'https://vimeo.com',
            'dailymotion': 'https://dailymotion.com',
            'gaana': 'https://gaana.com',
            'jio saavn': 'https://jiosaavn.com',
            'saavn': 'https://jiosaavn.com',
            
            # Shopping & E-commerce
            'amazon': 'https://amazon.com',
            'flipkart': 'https://flipkart.com',
            'myntra': 'https://myntra.com',
            'ajio': 'https://ajio.com',
            'nykaa': 'https://nykaa.com',
            'ebay': 'https://ebay.com',
            'alibaba': 'https://alibaba.com',
            'aliexpress': 'https://aliexpress.com',
            'etsy': 'https://etsy.com',
            'walmart': 'https://walmart.com',
            'target': 'https://target.com',
            'bestbuy': 'https://bestbuy.com',
            'shopify': 'https://shopify.com',
            
            # Food & Delivery
            'swiggy': 'https://swiggy.com',
            'zomato': 'https://zomato.com',
            'uber eats': 'https://ubereats.com',
            'dominos': 'https://dominos.com',
            'pizza hut': 'https://pizzahut.com',
            'mcdonalds': 'https://mcdonalds.com',
            'kfc': 'https://kfc.com',
            'subway': 'https://subway.com',
            'starbucks': 'https://starbucks.com',
            
            # Banking & Finance
            'paytm': 'https://paytm.com',
            'phonepe': 'https://phonepe.com',
            'sbi': 'https://onlinesbi.sbi',
            'hdfc': 'https://hdfcbank.com',
            'icici': 'https://icicibank.com',
            'axis': 'https://axisbank.com',
            'kotak': 'https://kotak.com',
            'paypal': 'https://paypal.com',
            'razorpay': 'https://razorpay.com',
            'zerodha': 'https://zerodha.com',
            'groww': 'https://groww.in',
            'upstox': 'https://upstox.com',
            
            # Travel & Transportation
            'makemytrip': 'https://makemytrip.com',
            'cleartrip': 'https://cleartrip.com',
            'goibibo': 'https://goibibo.com',
            'booking': 'https://booking.com',
            'expedia': 'https://expedia.com',
            'airbnb': 'https://airbnb.com',
            'uber': 'https://uber.com',
            'ola': 'https://olacabs.com',
            'irctc': 'https://irctc.co.in',
            'redbus': 'https://redbus.in',
            
            # News & Media
            'times of india': 'https://timesofindia.indiatimes.com',
            'toi': 'https://timesofindia.indiatimes.com',
            'hindustan times': 'https://hindustantimes.com',
            'indian express': 'https://indianexpress.com',
            'ndtv': 'https://ndtv.com',
            'cnn': 'https://cnn.com',
            'bbc': 'https://bbc.com',
            'reuters': 'https://reuters.com',
            'bloomberg': 'https://bloomberg.com',
            'techcrunch': 'https://techcrunch.com',
            'the verge': 'https://theverge.com',
            'wired': 'https://wired.com',
            'mashable': 'https://mashable.com',
            
            # Education & Learning
            'khan academy': 'https://khanacademy.org',
            'coursera': 'https://coursera.org',
            'udemy': 'https://udemy.com',
            'edx': 'https://edx.org',
            'skillshare': 'https://skillshare.com',
            'duolingo': 'https://duolingo.com',
            'codecademy': 'https://codecademy.com',
            'freecodecamp': 'https://freecodecamp.org',
            'w3schools': 'https://w3schools.com',
            'mdn': 'https://developer.mozilla.org',
            'stackoverflow': 'https://stackoverflow.com',
            'github': 'https://github.com',
            'gitlab': 'https://gitlab.com',
            'bitbucket': 'https://bitbucket.org',
            
            # Productivity & Work
            'microsoft office': 'https://office.com',
            'office': 'https://office.com',
            'word': 'https://office.com/launch/word',
            'excel': 'https://office.com/launch/excel',
            'powerpoint': 'https://office.com/launch/powerpoint',
            'teams': 'https://teams.microsoft.com',
            'outlook': 'https://outlook.com',
            'onedrive': 'https://onedrive.com',
            'zoom': 'https://zoom.us',
            'slack': 'https://slack.com',
            'notion': 'https://notion.so',
            'trello': 'https://trello.com',
            'asana': 'https://asana.com',
            'monday': 'https://monday.com',
            'dropbox': 'https://dropbox.com',
            'canva': 'https://canva.com',
            'figma': 'https://figma.com',
            'adobe': 'https://adobe.com',
            
            # Health & Fitness
            'myfitnesspal': 'https://myfitnesspal.com',
            'fitbit': 'https://fitbit.com',
            'strava': 'https://strava.com',
            'nike': 'https://nike.com',
            'adidas': 'https://adidas.com',
            'webmd': 'https://webmd.com',
            'healthline': 'https://healthline.com',
            '1mg': 'https://1mg.com',
            'practo': 'https://practo.com',
            
            # Gaming
            'steam': 'https://store.steampowered.com',
            'epic games': 'https://epicgames.com',
            'origin': 'https://origin.com',
            'battle.net': 'https://battle.net',
            'xbox': 'https://xbox.com',
            'playstation': 'https://playstation.com',
            'nintendo': 'https://nintendo.com',
            'ign': 'https://ign.com',
            'gamespot': 'https://gamespot.com',
            
            # Reference & Information
            'wikipedia': 'https://wikipedia.org',
            'wiki': 'https://wikipedia.org',
            'dictionary': 'https://dictionary.com',
            'thesaurus': 'https://thesaurus.com',
            'imdb': 'https://imdb.com',
            'rotten tomatoes': 'https://rottentomatoes.com',
            'goodreads': 'https://goodreads.com',
            'quora': 'https://quora.com',
            'yahoo': 'https://yahoo.com',
            'bing': 'https://bing.com',
            'duckduckgo': 'https://duckduckgo.com',
            
            # Miscellaneous
            'weather': 'https://weather.com',
            'accuweather': 'https://accuweather.com',
            'cricbuzz': 'https://cricbuzz.com',
            'espn': 'https://espn.com',
            'jio': 'https://jio.com',
            'airtel': 'https://airtel.in',
            'vodafone': 'https://vodafone.in',
            'bsnl': 'https://bsnl.co.in'
        }
        
        # Create reverse mapping for faster lookups
        self.url_to_name = {url: name for name, url in self.websites.items()}
        
        # Common aliases and variations
        self.aliases = {
            'fb': 'facebook',
            'ig': 'instagram',
            'yt': 'youtube',
            'gm': 'gmail',
            'drive': 'google drive',
            'docs': 'google docs',
            'sheets': 'google sheets',
            'slides': 'google slides',
            'maps': 'google maps',
            'photos': 'google photos',
            'calendar': 'google calendar',
            'meet': 'google meet',
            'translate': 'google translate',
            'gpay': 'google pay',
            'prime': 'amazon prime',
            'disney': 'disney plus',
            'saavn': 'jio saavn',
            'toi': 'times of india',
            'wiki': 'wikipedia',
        }

    def find_website(self, query: str) -> Optional[Tuple[str, str, float]]:
        """
        Find the best matching website for a query
        Returns: (website_name, url, confidence_score) or None
        """
        if not query:
            return None
            
        query = query.lower().strip()
        
        # Remove common prefixes
        query = re.sub(r'^(open|go to|visit|launch|start)\s+', '', query)
        query = re.sub(r'^(website|site)\s+', '', query)
        
        # Direct exact match
        if query in self.websites:
            return (query, self.websites[query], 1.0)
        
        # Check aliases
        if query in self.aliases:
            alias_target = self.aliases[query]
            if alias_target in self.websites:
                return (alias_target, self.websites[alias_target], 1.0)
        
        # Fuzzy matching with scoring
        matches = []
        
        for website_name, url in self.websites.items():
            # Calculate similarity scores
            exact_score = self._calculate_exact_match_score(query, website_name)
            fuzzy_score = self._calculate_fuzzy_score(query, website_name)
            partial_score = self._calculate_partial_match_score(query, website_name)
            
            # Combined score with weights
            combined_score = (exact_score * 0.5) + (fuzzy_score * 0.3) + (partial_score * 0.2)
            
            if combined_score > 0.3:  # Minimum threshold
                matches.append((website_name, url, combined_score))
        
        # Sort by score and return best match
        if matches:
            matches.sort(key=lambda x: x[2], reverse=True)
            return matches[0]
        
        return None

    def _calculate_exact_match_score(self, query: str, website_name: str) -> float:
        """Calculate exact match score"""
        if query == website_name:
            return 1.0
        if query in website_name or website_name in query:
            return 0.8
        return 0.0

    def _calculate_fuzzy_score(self, query: str, website_name: str) -> float:
        """Calculate fuzzy similarity score using SequenceMatcher"""
        return SequenceMatcher(None, query, website_name).ratio()

    def _calculate_partial_match_score(self, query: str, website_name: str) -> float:
        """Calculate partial match score for multi-word queries"""
        query_words = query.split()
        website_words = website_name.split()
        
        if not query_words or not website_words:
            return 0.0
        
        matches = 0
        for query_word in query_words:
            for website_word in website_words:
                if query_word == website_word:
                    matches += 1
                elif query_word in website_word or website_word in query_word:
                    matches += 0.5
                elif SequenceMatcher(None, query_word, website_word).ratio() > 0.8:
                    matches += 0.7
        
        return matches / len(query_words)

    def open_website(self, query: str) -> Dict:
        """
        Open a website based on query
        Returns result dictionary with success status and details
        """
        try:
            result = self.find_website(query)
            
            if not result:
                return {
                    'success': False,
                    'message': f"Sorry, I couldn't find a website matching '{query}'. Try being more specific.",
                    'suggestions': self._get_suggestions(query)
                }
            
            website_name, url, confidence = result
            
            # Open the website
            webbrowser.open(url)
            
            logger.info(f"Opened website: {website_name} ({url}) with confidence {confidence:.2f}")
            
            return {
                'success': True,
                'message': f"Opening {website_name}",
                'website_name': website_name,
                'url': url,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error opening website for query '{query}': {str(e)}")
            return {
                'success': False,
                'message': f"Sorry, I couldn't open the website. Error: {str(e)}"
            }

    def _get_suggestions(self, query: str) -> List[str]:
        """Get website suggestions for failed queries"""
        suggestions = []
        
        # Find partial matches for suggestions
        for website_name in self.websites.keys():
            if any(word in website_name for word in query.lower().split()):
                suggestions.append(website_name)
            elif SequenceMatcher(None, query.lower(), website_name).ratio() > 0.4:
                suggestions.append(website_name)
        
        # Return top 5 suggestions
        return suggestions[:5]

    def list_categories(self) -> Dict[str, List[str]]:
        """Return websites organized by categories"""
        categories = {
            'Social Media': [
                'youtube', 'facebook', 'instagram', 'twitter', 'linkedin', 
                'reddit', 'discord', 'whatsapp', 'telegram', 'snapchat', 'tiktok'
            ],
            'Google Services': [
                'google', 'gmail', 'google drive', 'google docs', 'google sheets',
                'google maps', 'google photos', 'google calendar', 'youtube music'
            ],
            'Entertainment': [
                'netflix', 'amazon prime', 'disney plus', 'spotify', 'twitch',
                'hulu', 'hbo max', 'apple music', 'soundcloud'
            ],
            'Shopping': [
                'amazon', 'flipkart', 'ebay', 'walmart', 'target', 'bestbuy',
                'myntra', 'nykaa', 'aliexpress'
            ],
            'News & Media': [
                'cnn', 'bbc', 'reuters', 'bloomberg', 'techcrunch', 'the verge',
                'times of india', 'ndtv', 'hindustan times'
            ],
            'Education': [
                'khan academy', 'coursera', 'udemy', 'codecademy', 'github',
                'stackoverflow', 'w3schools', 'freecodecamp'
            ],
            'Productivity': [
                'microsoft office', 'google docs', 'notion', 'trello', 'slack',
                'zoom', 'teams', 'dropbox', 'canva', 'figma'
            ]
        }
        
        return categories

    def search_websites(self, category: str = None, query: str = None) -> List[Dict]:
        """Search websites by category or query"""
        results = []
        
        if category:
            categories = self.list_categories()
            if category.lower() in [cat.lower() for cat in categories.keys()]:
                for cat_name, websites in categories.items():
                    if cat_name.lower() == category.lower():
                        for website in websites:
                            if website in self.websites:
                                results.append({
                                    'name': website,
                                    'url': self.websites[website],
                                    'category': cat_name
                                })
        
        elif query:
            query = query.lower()
            for website_name, url in self.websites.items():
                if query in website_name.lower():
                    results.append({
                        'name': website_name,
                        'url': url,
                        'relevance': SequenceMatcher(None, query, website_name.lower()).ratio()
                    })
            
            # Sort by relevance
            results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return results

    def get_popular_websites(self, limit: int = 20) -> List[Dict]:
        """Get most popular websites"""
        popular = [
            'google', 'youtube', 'facebook', 'amazon', 'netflix', 'instagram',
            'twitter', 'linkedin', 'github', 'stackoverflow', 'wikipedia',
            'gmail', 'google drive', 'spotify', 'reddit', 'discord',
            'zoom', 'microsoft office', 'canva', 'figma'
        ]
        
        results = []
        for website in popular[:limit]:
            if website in self.websites:
                results.append({
                    'name': website,
                    'url': self.websites[website]
                })
        
        return results

# Global instance
website_opener = WebsiteOpener()

def open_website(query: str) -> Dict:
    """Convenience function to open a website"""
    return website_opener.open_website(query)

def find_website(query: str) -> Optional[Tuple[str, str, float]]:
    """Convenience function to find a website"""
    return website_opener.find_website(query)

def get_website_suggestions(query: str) -> List[str]:
    """Get website suggestions for a query"""
    return website_opener._get_suggestions(query)

def list_website_categories() -> Dict[str, List[str]]:
    """List all website categories"""
    return website_opener.list_categories()

# Example usage and testing
if __name__ == "__main__":
    # Test the website opener
    test_queries = [
        "youtube",
        "facebook",
        "google docs",
        "netflix",
        "amazon",
        "github",
        "stackoverflow",
        "open youtube",
        "go to facebook",
        "visit google",
        "launch netflix"
    ]
    
    print("Testing Website Opener:")
    print("=" * 50)
    
    for query in test_queries:
        result = open_website(query)
        print(f"Query: '{query}'")
        print(f"Result: {result}")
        print("-" * 30)
