"""
Nexa App Launcher - Comprehensive app opening system
Ported from VocalPA AppLauncher.kt with desktop equivalents and Android APK support
"""

import platform
import subprocess
import webbrowser
import logging
from typing import Dict, List, Optional, Tuple
import os

logger = logging.getLogger(__name__)


class AppLauncher:
    """Comprehensive app launcher with 100+ apps support including Android APKs"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self._app_mappings = self._build_app_mappings()
        self._website_fallback = True  # Open website if app not found
    
    def _build_app_mappings(self) -> Dict[str, Dict]:
        """Build comprehensive app mappings for all platforms including Android APKs"""
        return {
            # Social Media Apps
            "whatsapp": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.whatsapp", "com.whatsapp.w4b"],  # WhatsApp & WhatsApp Business
                "website": "https://web.whatsapp.com",
                "aliases": ["whats app", "whatsapp web", "whatsapp business"]
            },
            "instagram": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.instagram.android", "com.instagram.lite"],  # Instagram & Instagram Lite
                "website": "https://instagram.com",
                "aliases": ["insta", "ig"]
            },
            "facebook": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.facebook.katana", "com.facebook.lite"],  # Facebook & Facebook Lite
                "website": "https://facebook.com",
                "aliases": ["fb"]
            },
            "twitter": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.twitter.android", "com.twitter.android.lite"],  # Twitter & Twitter Lite
                "website": "https://twitter.com",
                "aliases": ["x"]
            },
            "snapchat": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.snapchat.android"],
                "website": "https://snapchat.com",
                "aliases": ["snap"]
            },
            "telegram": {
                "windows": "telegram",
                "linux": "telegram",
                "darwin": "telegram",
                "android": ["org.telegram.messenger"],
                "website": "https://web.telegram.org",
                "aliases": []
            },
            "discord": {
                "windows": "discord",
                "linux": "discord",
                "darwin": "discord",
                "android": ["com.discord"],
                "website": "https://discord.com",
                "aliases": []
            },
            "linkedin": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.linkedin.android"],
                "website": "https://linkedin.com",
                "aliases": []
            },
            "tiktok": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.zhiliaoapp.musically"],
                "website": "https://tiktok.com",
                "aliases": ["tik tok"]
            },
            "reddit": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.reddit.frontpage"],
                "website": "https://reddit.com",
                "aliases": []
            },
            
            # Entertainment Apps
            "youtube": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.youtube", "com.google.android.apps.youtube.mango"],
                "website": "https://youtube.com",
                "aliases": ["yt"]
            },
            "netflix": {
                "windows": "netflix",
                "linux": None,
                "darwin": "netflix",
                "android": ["com.netflix.mediaclient", "com.netflix.ninja"],
                "website": "https://netflix.com",
                "aliases": []
            },
            "spotify": {
                "windows": "spotify",
                "linux": "spotify",
                "darwin": "spotify",
                "android": ["com.spotify.music", "com.spotify.lite"],
                "website": "https://spotify.com",
                "aliases": []
            },
            "amazon prime": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.amazon.avod.thirdpartyclient"],
                "website": "https://primevideo.com",
                "aliases": ["prime video", "prime"]
            },
            "disney plus": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["in.startv.hotstar"],
                "website": "https://disneyplus.com",
                "aliases": ["disney", "hotstar", "disney+ hotstar"]
            },
            "twitch": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["tv.twitch.android.app"],
                "website": "https://twitch.tv",
                "aliases": []
            },
            "youtube music": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.youtube.music"],
                "website": "https://music.youtube.com",
                "aliases": ["yt music"]
            },
            
            # Google Apps
            "gmail": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.gm"],
                "website": "https://gmail.com",
                "aliases": []
            },
            "google maps": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.maps"],
                "website": "https://maps.google.com",
                "aliases": ["maps"]
            },
            "google drive": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.docs"],
                "website": "https://drive.google.com",
                "aliases": ["drive"]
            },
            "google photos": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.photos"],
                "website": "https://photos.google.com",
                "aliases": ["photos"]
            },
            "chrome": {
                "windows": "chrome",
                "linux": "google-chrome",
                "darwin": "google chrome",
                "android": ["com.android.chrome"],
                "website": "https://google.com",
                "aliases": ["google chrome", "browser"]
            },
            "google": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.googlequicksearchbox"],
                "website": "https://google.com",
                "aliases": ["google search"]
            },
            "google pay": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.nbu.paisa.user"],
                "website": "https://pay.google.com",
                "aliases": ["gpay"]
            },
            "google meet": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.google.android.apps.tachyon"],
                "website": "https://meet.google.com",
                "aliases": ["meet"]
            },
            
            # Shopping & Food Apps
            "amazon": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["in.amazon.mShop.android.shopping"],
                "website": "https://amazon.com",
                "aliases": []
            },
            "flipkart": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.flipkart.android"],
                "website": "https://flipkart.com",
                "aliases": []
            },
            "myntra": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.myntra.android"],
                "website": "https://myntra.com",
                "aliases": []
            },
            "paytm": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["net.one97.paytm"],
                "website": "https://paytm.com",
                "aliases": []
            },
            "phonepe": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.phonepe.app"],
                "website": "https://phonepe.com",
                "aliases": ["phone pe"]
            },
            "swiggy": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["in.swiggy.android"],
                "website": "https://swiggy.com",
                "aliases": []
            },
            "zomato": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.application.zomato"],
                "website": "https://zomato.com",
                "aliases": []
            },
            "uber": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.ubercab"],
                "website": "https://uber.com",
                "aliases": []
            },
            "ola": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.olacabs.customer"],
                "website": "https://olacabs.com",
                "aliases": []
            },
            
            # Banking & Finance Apps
            "sbi": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.sbi.SBIFreedomPlus"],
                "website": "https://onlinesbi.sbi",
                "aliases": ["state bank", "sbi yono"]
            },
            "hdfc": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.snapwork.hdfc"],
                "website": "https://hdfcbank.com",
                "aliases": ["hdfc bank"]
            },
            "icici": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.csam.icici.bank.imobile"],
                "website": "https://icicibank.com",
                "aliases": ["icici bank", "imobile"]
            },
            "axis": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.axis.mobile"],
                "website": "https://axisbank.com",
                "aliases": ["axis bank"]
            },
            
            # Productivity Apps
            "microsoft office": {
                "windows": "winword",
                "linux": "libreoffice",
                "darwin": "microsoft word",
                "android": ["com.microsoft.office.officehubrow"],
                "website": "https://office.com",
                "aliases": ["office", "ms office"]
            },
            "microsoft word": {
                "windows": "winword",
                "linux": "libreoffice --writer",
                "darwin": "microsoft word",
                "android": ["com.microsoft.office.word"],
                "website": "https://office.com/launch/word",
                "aliases": ["word", "ms word"]
            },
            "microsoft excel": {
                "windows": "excel",
                "linux": "libreoffice --calc",
                "darwin": "microsoft excel",
                "android": ["com.microsoft.office.excel"],
                "website": "https://office.com/launch/excel",
                "aliases": ["excel", "ms excel"]
            },
            "microsoft powerpoint": {
                "windows": "powerpnt",
                "linux": "libreoffice --impress",
                "darwin": "microsoft powerpoint",
                "android": ["com.microsoft.office.powerpoint"],
                "website": "https://office.com/launch/powerpoint",
                "aliases": ["powerpoint", "ms powerpoint"]
            },
            "microsoft teams": {
                "windows": "teams",
                "linux": "teams",
                "darwin": "microsoft teams",
                "android": ["com.microsoft.teams"],
                "website": "https://teams.microsoft.com",
                "aliases": ["teams", "ms teams"]
            },
            "zoom": {
                "windows": "zoom",
                "linux": "zoom",
                "darwin": "zoom",
                "android": ["us.zoom.videomeetings"],
                "website": "https://zoom.us",
                "aliases": []
            },
            "skype": {
                "windows": "skype",
                "linux": "skype",
                "darwin": "skype",
                "android": ["com.skype.raider"],
                "website": "https://skype.com",
                "aliases": []
            },
            
            # System Apps (Android)
            "settings": {
                "windows": "ms-settings:",
                "linux": "gnome-control-center",
                "darwin": "system preferences",
                "android": ["com.android.settings"],
                "website": None,
                "aliases": ["system settings"]
            },
            "camera": {
                "windows": "microsoft.windows.camera:",
                "linux": "cheese",
                "darwin": "photo booth",
                "android": ["com.android.camera", "com.android.camera2"],
                "website": None,
                "aliases": []
            },
            "gallery": {
                "windows": "ms-photos:",
                "linux": "eog",
                "darwin": "photos",
                "android": ["com.android.gallery3d", "com.google.android.apps.photos"],
                "website": None,
                "aliases": ["photos"]
            },
            "calculator": {
                "windows": "calc",
                "linux": "gnome-calculator",
                "darwin": "calculator",
                "android": ["com.android.calculator2"],
                "website": None,
                "aliases": ["calc"]
            },
            "clock": {
                "windows": "ms-clock:",
                "linux": "gnome-clocks",
                "darwin": "clock mini",
                "android": ["com.android.deskclock"],
                "website": None,
                "aliases": ["timer", "alarm"]
            },
            "calendar": {
                "windows": "outlookcal:",
                "linux": "gnome-calendar",
                "darwin": "calendar",
                "android": ["com.android.calendar", "com.google.android.calendar"],
                "website": None,
                "aliases": []
            },
            "contacts": {
                "windows": "ms-people:",
                "linux": "gnome-contacts",
                "darwin": "contacts",
                "android": ["com.android.contacts"],
                "website": None,
                "aliases": []
            },
            "phone": {
                "windows": None,
                "linux": None,
                "darwin": None,
                "android": ["com.android.dialer", "com.google.android.dialer"],
                "website": None,
                "aliases": ["dialer"]
            },
            "messages": {
                "windows": None,
                "linux": None,
                "darwin": "messages",
                "android": ["com.android.messaging", "com.google.android.apps.messaging"],
                "website": None,
                "aliases": ["sms", "text"]
            },
            
            # Basic Desktop Apps
            "notepad": {
                "windows": "notepad",
                "linux": "gedit",
                "darwin": "textedit",
                "android": None,
                "website": None,
                "aliases": ["text editor"]
            },
            "file manager": {
                "windows": "explorer",
                "linux": "nautilus",
                "darwin": "finder",
                "android": ["com.android.documentsui"],
                "website": None,
                "aliases": ["files", "explorer", "finder"]
            },
            "terminal": {
                "windows": "cmd",
                "linux": "gnome-terminal",
                "darwin": "terminal",
                "android": ["com.termux"],
                "website": None,
                "aliases": ["command prompt", "cmd"]
            },
            "browser": {
                "windows": "msedge",
                "linux": "firefox",
                "darwin": "safari",
                "android": ["com.android.chrome", "com.android.browser"],
                "website": "https://google.com",
                "aliases": ["web browser", "internet"]
            }
        }

    def find_app(self, query: str) -> Optional[Tuple[str, Dict, float]]:
        """Find the best matching app for a query"""
        if not query:
            return None
            
        query = query.lower().strip()
        
        # Remove common prefixes
        query = query.replace("open ", "").replace("launch ", "").replace("start ", "").replace("run ", "")
        
        # Direct exact match
        if query in self._app_mappings:
            return (query, self._app_mappings[query], 1.0)
        
        # Check aliases
        for app_name, app_info in self._app_mappings.items():
            if query in app_info.get("aliases", []):
                return (app_name, app_info, 1.0)
        
        # Fuzzy matching
        matches = []
        for app_name, app_info in self._app_mappings.items():
            # Check if query is contained in app name
            if query in app_name:
                score = len(query) / len(app_name)  # Longer matches get higher scores
                matches.append((app_name, app_info, score))
            
            # Check aliases
            for alias in app_info.get("aliases", []):
                if query in alias:
                    score = len(query) / len(alias)
                    matches.append((app_name, app_info, score))
        
        # Return best match
        if matches:
            matches.sort(key=lambda x: x[2], reverse=True)
            return matches[0]
        
        return None

    def launch_app(self, query: str) -> Dict:
        """Launch an app based on query"""
        try:
            result = self.find_app(query)
            
            if not result:
                return {
                    'success': False,
                    'message': f"Sorry, I couldn't find an app matching '{query}'. Try being more specific.",
                    'suggestions': self._get_suggestions(query)
                }
            
            app_name, app_info, confidence = result
            
            # Try to launch the app for current platform
            platform_key = self.system
            if platform_key == "darwin":
                platform_key = "darwin"  # macOS
            
            # Check if we're on Android (this would need to be detected differently in real implementation)
            is_android = False  # Placeholder - would need proper Android detection
            
            if is_android and "android" in app_info:
                # Android app launching (would need Android-specific implementation)
                return self._launch_android_app(app_info["android"], app_name)
            elif platform_key in app_info and app_info[platform_key]:
                # Desktop app launching
                return self._launch_desktop_app(app_info[platform_key], app_name)
            elif self._website_fallback and app_info.get("website"):
                # Fallback to website
                webbrowser.open(app_info["website"])
                return {
                    'success': True,
                    'message': f"Opened {app_name} website",
                    'app_name': app_name,
                    'method': 'website_fallback',
                    'url': app_info["website"]
                }
            else:
                return {
                    'success': False,
                    'message': f"{app_name} is not available on this platform",
                    'app_name': app_name,
                    'available_platforms': [k for k, v in app_info.items() if v and k != 'aliases']
                }
                
        except Exception as e:
            logger.error(f"Error launching app for query '{query}': {str(e)}")
            return {
                'success': False,
                'message': f"Error launching app: {str(e)}"
            }

    def _launch_desktop_app(self, command: str, app_name: str) -> Dict:
        """Launch a desktop application"""
        try:
            if self.system == "windows":
                # Handle Windows-specific commands
                if command.startswith("ms-") or command.endswith(":"):
                    # Windows URI scheme
                    subprocess.run(["start", command], shell=True, check=True)
                else:
                    # Regular executable
                    subprocess.Popen(command, shell=True)
            else:
                # Linux/macOS
                if self.system == "darwin":
                    # macOS - use 'open' command
                    subprocess.run(["open", "-a", command], check=True)
                else:
                    # Linux - direct command
                    subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return {
                'success': True,
                'message': f"Launching {app_name}",
                'app_name': app_name,
                'command': command,
                'method': 'desktop_app'
            }
            
        except Exception as e:
            logger.error(f"Failed to launch {app_name}: {str(e)}")
            return {
                'success': False,
                'message': f"Failed to launch {app_name}: {str(e)}",
                'app_name': app_name
            }

    def _launch_android_app(self, packages: List[str], app_name: str) -> Dict:
        """Launch an Android app (placeholder for Android implementation)"""
        # This would need Android-specific implementation using Android APIs
        # For now, return a placeholder response
        return {
            'success': False,
            'message': f"Android app launching not implemented yet for {app_name}",
            'app_name': app_name,
            'android_packages': packages,
            'method': 'android_app'
        }

    def _get_suggestions(self, query: str) -> List[str]:
        """Get app suggestions for failed queries"""
        suggestions = []
        query_words = query.lower().split()
        
        for app_name, app_info in self._app_mappings.items():
            # Check if any query word is in app name
            if any(word in app_name for word in query_words):
                suggestions.append(app_name)
            
            # Check aliases
            for alias in app_info.get("aliases", []):
                if any(word in alias for word in query_words):
                    suggestions.append(app_name)
        
        return list(set(suggestions))[:5]  # Return top 5 unique suggestions

    def list_apps_by_category(self) -> Dict[str, List[str]]:
        """List apps organized by category"""
        categories = {
            'Social Media': ['whatsapp', 'instagram', 'facebook', 'twitter', 'snapchat', 'telegram', 'discord', 'linkedin', 'tiktok', 'reddit'],
            'Entertainment': ['youtube', 'netflix', 'spotify', 'amazon prime', 'disney plus', 'twitch', 'youtube music'],
            'Google Apps': ['gmail', 'google maps', 'google drive', 'google photos', 'chrome', 'google', 'google pay', 'google meet'],
            'Shopping & Food': ['amazon', 'flipkart', 'myntra', 'paytm', 'phonepe', 'swiggy', 'zomato', 'uber', 'ola'],
            'Banking': ['sbi', 'hdfc', 'icici', 'axis'],
            'Productivity': ['microsoft office', 'microsoft word', 'microsoft excel', 'microsoft powerpoint', 'microsoft teams', 'zoom', 'skype'],
            'System': ['settings', 'camera', 'gallery', 'calculator', 'clock', 'calendar', 'contacts', 'phone', 'messages'],
            'Basic Tools': ['notepad', 'file manager', 'terminal', 'browser']
        }
        
        return categories

    def get_android_packages(self) -> Dict[str, List[str]]:
        """Get all Android package names"""
        android_packages = {}
        
        for app_name, app_info in self._app_mappings.items():
            if "android" in app_info and app_info["android"]:
                android_packages[app_name] = app_info["android"]
        
        return android_packages


# Global instance
app_launcher = AppLauncher()

def launch_app(query: str) -> Dict:
    """Convenience function to launch an app"""
    return app_launcher.launch_app(query)

def find_app(query: str) -> Optional[Tuple[str, Dict, float]]:
    """Convenience function to find an app"""
    return app_launcher.find_app(query)

def get_app_suggestions(query: str) -> List[str]:
    """Get app suggestions for a query"""
    return app_launcher._get_suggestions(query)

def list_app_categories() -> Dict[str, List[str]]:
    """List all app categories"""
    return app_launcher.list_apps_by_category()

def get_android_packages() -> Dict[str, List[str]]:
    """Get all Android package names"""
    return app_launcher.get_android_packages()

# Example usage and testing
if __name__ == "__main__":
    print("Testing App Launcher with Android APK support:")
    print("=" * 60)
    
    # Test some apps
    test_queries = [
        "whatsapp",
        "instagram", 
        "youtube",
        "calculator",
        "chrome",
        "spotify",
        "open netflix",
        "launch gmail"
    ]
    
    for query in test_queries:
        result = launch_app(query)
        print(f"Query: '{query}'")
        print(f"Result: {result}")
        print("-" * 40)
    
    # Show Android packages
    print("\nAndroid Packages Available:")
    print("=" * 40)
    android_packages = get_android_packages()
    for app_name, packages in android_packages.items():
        print(f"{app_name}: {packages}")
