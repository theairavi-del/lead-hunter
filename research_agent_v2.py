#!/usr/bin/env python3
"""
Lead Hunter Research Agent v2.0
Real API integration for Reddit and Twitter
"""

import json
import os
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import random

# Try to import API libraries
try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
    print("⚠️  PRAW not installed. Reddit scanning disabled.")
    print("   Run: pip install praw")

try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
    print("⚠️  Tweepy not installed. Twitter scanning disabled.")
    print("   Run: pip install tweepy")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Using environment variables.")
    print("   Run: pip install python-dotenv")

# Configuration
LEADS_FILE = "leads.json"
SCAN_HISTORY_FILE = "scan_history.json"
MAX_LEADS = 100
MIN_SCORE_THRESHOLD = 5  # Minimum relevance score to include

# Subreddits to scan
TARGET_SUBREDDITS = [
    "webdev",
    "forhire",
    "slavelabour",
    "jobbit",
    "web_design",
    "Wordpress",
    "ecommerce",
    "smallbusiness",
    "Entrepreneur",
    "startups",
    "indiehackers"
]

# Twitter search queries
TWITTER_QUERIES = [
    "need a website",
    "looking for web developer",
    "need web designer",
    "website needed",
    "build a website",
    "web dev needed",
    "freelance web",
    "hire web developer",
    "website for business",
    "portfolio website needed"
]

# Keywords for scoring
HIGH_INTENT_KEYWORDS = [
    "budget", "$", "pay", "hiring", "paid", "freelance",
    "looking for", "need someone", "asap", "urgent"
]

BUDGET_PATTERNS = [
    r'\$[\d,]+(?:k)?',  # $500, $2k, $1,000
    r'\d+\s*(?:k|thousand)',  # 2k, 3 thousand
    r'budget\s*(?:of\s*)?(?:is\s*)?[\d$]+',  # budget of $500
]

@dataclass
class Lead:
    id: str
    source: str
    sourceName: str
    title: str
    description: str
    url: str
    author: str
    timestamp: str
    tags: List[str]
    intent: str  # high, medium, low
    budget: Optional[str]
    score: int
    designMockup: str
    designNotes: str
    contacted: bool = False
    notes: str = ""

class RedditScanner:
    def __init__(self):
        self.reddit = None
        if REDDIT_AVAILABLE:
            try:
                self.reddit = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                    user_agent=os.getenv('REDDIT_USER_AGENT', 'LeadHunter/1.0')
                )
                print("✅ Reddit API connected")
            except Exception as e:
                print(f"❌ Reddit connection failed: {e}")
                self.reddit = None
    
    def scan(self, hours_back: int = 1) -> List[Lead]:
        """Scan Reddit for web dev leads"""
        if not self.reddit:
            return []
        
        leads = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        for subreddit_name in TARGET_SUBREDDITS:
            try:
                print(f"  🔍 Scanning r/{subreddit_name}...")
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get new posts
                for post in subreddit.new(limit=25):
                    post_time = datetime.utcfromtimestamp(post.created_utc)
                    if post_time < cutoff_time:
                        continue
                    
                    # Check if post matches our criteria
                    score = self._score_post(post)
                    if score >= MIN_SCORE_THRESHOLD:
                        lead = self._create_lead_from_post(post, score)
                        if lead:
                            leads.append(lead)
                
                # Rate limiting - be nice to Reddit
                time.sleep(2)
                
            except Exception as e:
                print(f"  ⚠️  Error scanning r/{subreddit_name}: {e}")
                continue
        
        return leads
    
    def _score_post(self, post) -> int:
        """Score a post based on relevance"""
        score = 0
        text = f"{post.title} {post.selftext}".lower()
        
        # Check for website-related keywords
        website_keywords = ['website', 'web dev', 'web design', 'landing page', 
                          'portfolio', 'ecommerce', 'wordpress', 'shopify']
        for keyword in website_keywords:
            if keyword in text:
                score += 2
        
        # Check for intent keywords
        for keyword in HIGH_INTENT_KEYWORDS:
            if keyword in text:
                score += 3
        
        # Check for budget mentions
        for pattern in BUDGET_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                score += 5
        
        return score
    
    def _create_lead_from_post(self, post, score: int) -> Optional[Lead]:
        """Convert a Reddit post to a Lead object"""
        # Extract budget
        budget = self._extract_budget(post.selftext or post.title)
        
        # Determine intent
        intent = "low"
        if score >= 15:
            intent = "high"
        elif score >= 10:
            intent = "medium"
        
        # Generate tags
        tags = self._generate_tags(post.selftext or post.title)
        
        # Generate design concept
        design_mockup, design_notes = self._generate_design_concept(post.title, post.selftext)
        
        return Lead(
            id=f"reddit_{post.id}",
            source="reddit",
            sourceName=f"r/{post.subreddit.display_name}",
            title=post.title[:100],
            description=(post.selftext[:300] + "...") if len(post.selftext) > 300 else post.selftext,
            url=f"https://reddit.com{post.permalink}",
            author=str(post.author),
            timestamp=datetime.utcfromtimestamp(post.created_utc).isoformat(),
            tags=tags,
            intent=intent,
            budget=budget,
            score=score,
            designMockup=design_mockup,
            designNotes=design_notes
        )
    
    def _extract_budget(self, text: str) -> Optional[str]:
        """Extract budget from text"""
        for pattern in BUDGET_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _generate_tags(self, text: str) -> List[str]:
        """Generate tags from post content"""
        tags = []
        text_lower = text.lower()
        
        # Project type tags
        if 'portfolio' in text_lower:
            tags.append('Portfolio')
        if 'ecommerce' in text_lower or 'shopify' in text_lower:
            tags.append('E-commerce')
        if 'landing page' in text_lower:
            tags.append('Landing Page')
        if 'wordpress' in text_lower:
            tags.append('WordPress')
        if 'react' in text_lower:
            tags.append('React')
        if 'saas' in text_lower:
            tags.append('SaaS')
        
        # If no specific tags, add general
        if not tags:
            tags.append('Website')
        
        return tags[:4]  # Max 4 tags
    
    def _generate_design_concept(self, title: str, text: str) -> tuple:
        """Generate a design mockup emoji and notes based on content"""
        full_text = f"{title} {text}".lower()
        
        # Portfolio sites
        if 'portfolio' in full_text or 'photography' in full_text or 'designer' in full_text:
            return ("📸", "Gallery-focused layout, lightbox for images, about section, contact form. Clean typography, image-first design.")
        
        # E-commerce
        if 'ecommerce' in full_text or 'shop' in full_text or 'store' in full_text:
            return ("🛒", "Product grid layout, shopping cart, checkout flow, payment integration. Mobile-optimized, trust badges.")
        
        # SaaS/Landing page
        if 'saas' in full_text or 'landing page' in full_text or 'startup' in full_text:
            return ("🚀", "Hero with product demo, feature sections, pricing cards, testimonials. CTA-focused, conversion optimized.")
        
        # Business/Corporate
        if 'business' in full_text or 'company' in full_text:
            return ("🏢", "Professional corporate design, services section, team profiles, contact forms. Trust-building elements.")
        
        # Personal/Portfolio
        if 'personal' in full_text or 'blog' in full_text:
            return ("✨", "Personal brand focus, blog layout, newsletter signup, social links. Bold typography, unique personality.")
        
        # Restaurant/Food
        if 'restaurant' in full_text or 'food' in full_text:
            return ("🍽️", "Menu display, reservation system, location map, online ordering. Appetizing imagery, easy navigation.")
        
        # Real Estate
        if 'real estate' in full_text or 'property' in full_text:
            return ("🏠", "Property listings, search filters, map integration, agent profiles. Professional, trustworthy design.")
        
        # Default
        return ("💻", "Modern responsive design, clear navigation, strong CTAs, fast loading. Mobile-first approach.")

class TwitterScanner:
    def __init__(self):
        self.client = None
        if TWITTER_AVAILABLE:
            try:
                bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
                if bearer_token:
                    self.client = tweepy.Client(bearer_token=bearer_token)
                    print("✅ Twitter API connected")
                else:
                    print("⚠️  No Twitter Bearer Token found")
            except Exception as e:
                print(f"❌ Twitter connection failed: {e}")
                self.client = None
    
    def scan(self, hours_back: int = 1) -> List[Lead]:
        """Scan Twitter for web dev leads"""
        if not self.client:
            return []
        
        leads = []
        start_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        for query in TWITTER_QUERIES:
            try:
                print(f"  🔍 Searching Twitter: '{query}'...")
                
                # Search recent tweets
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    start_time=start_time,
                    tweet_fields=['created_at', 'author_id', 'public_metrics']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        score = self._score_tweet(tweet)
                        if score >= MIN_SCORE_THRESHOLD:
                            lead = self._create_lead_from_tweet(tweet, score)
                            if lead:
                                leads.append(lead)
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"  ⚠️  Error searching Twitter: {e}")
                continue
        
        return leads
    
    def _score_tweet(self, tweet) -> int:
        """Score a tweet based on relevance"""
        score = 0
        text = tweet.text.lower()
        
        # Has engagement
        if hasattr(tweet, 'public_metrics'):
            metrics = tweet.public_metrics
            if metrics.get('retweet_count', 0) > 0:
                score += 2
            if metrics.get('like_count', 0) > 5:
                score += 2
        
        # Contains intent keywords
        for keyword in HIGH_INTENT_KEYWORDS:
            if keyword in text:
                score += 3
        
        # Not a retweet
        if not text.startswith('rt @'):
            score += 2
        
        return score
    
    def _create_lead_from_tweet(self, tweet, score: int) -> Optional[Lead]:
        """Convert a tweet to a Lead object"""
        budget = None
        for pattern in BUDGET_PATTERNS:
            match = re.search(pattern, tweet.text, re.IGNORECASE)
            if match:
                budget = match.group(0)
                break
        
        intent = "low"
        if score >= 12:
            intent = "high"
        elif score >= 8:
            intent = "medium"
        
        design_mockup, design_notes = RedditScanner()._generate_design_concept(tweet.text, "")
        
        return Lead(
            id=f"twitter_{tweet.id}",
            source="twitter",
            sourceName="Twitter",
            title=tweet.text[:100] + ("..." if len(tweet.text) > 100 else ""),
            description=tweet.text[:280],
            url=f"https://twitter.com/i/web/status/{tweet.id}",
            author=str(tweet.author_id),
            timestamp=tweet.created_at.isoformat() if hasattr(tweet, 'created_at') else datetime.utcnow().isoformat(),
            tags=["Twitter Lead"],
            intent=intent,
            budget=budget,
            score=score,
            designMockup=design_mockup,
            designNotes=design_notes
        )

class LeadManager:
    def __init__(self):
        self.leads = self._load_leads()
        self.scan_history = self._load_scan_history()
    
    def _load_leads(self) -> List[Dict]:
        """Load existing leads from file"""
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _load_scan_history(self) -> List[Dict]:
        """Load scan history"""
        if os.path.exists(SCAN_HISTORY_FILE):
            with open(SCAN_HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_leads(self):
        """Save leads to file"""
        # Keep only most recent MAX_LEADS
        sorted_leads = sorted(self.leads, key=lambda x: x.get('timestamp', ''), reverse=True)
        self.leads = sorted_leads[:MAX_LEADS]
        
        with open(LEADS_FILE, 'w') as f:
            json.dump(self.leads, f, indent=2, default=str)
    
    def add_leads(self, new_leads: List[Lead]):
        """Add new leads, avoiding duplicates"""
        existing_ids = {lead.get('id') for lead in self.leads}
        
        added_count = 0
        for lead in new_leads:
            if lead.id not in existing_ids:
                self.leads.append(asdict(lead))
                existing_ids.add(lead.id)
                added_count += 1
        
        if added_count > 0:
            self._save_leads()
        
        return added_count
    
    def record_scan(self, source: str, leads_found: int):
        """Record a scan in history"""
        self.scan_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'source': source,
            'leads_found': leads_found
        })
        
        # Keep last 100 scans
        self.scan_history = self.scan_history[-100:]
        
        with open(SCAN_HISTORY_FILE, 'w') as f:
            json.dump(self.scan_history, f, indent=2)

def main():
    """Main execution"""
    print("=" * 60)
    print("🔍 LEAD HUNTER v2.0 - Real API Integration")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize
    manager = LeadManager()
    reddit_scanner = RedditScanner()
    twitter_scanner = TwitterScanner()
    
    total_new_leads = 0
    
    # Scan Reddit
    if REDDIT_AVAILABLE and reddit_scanner.reddit:
        print("🌐 Scanning Reddit...")
        reddit_leads = reddit_scanner.scan(hours_back=1)
        added = manager.add_leads(reddit_leads)
        manager.record_scan('reddit', added)
        print(f"   ✅ Found {len(reddit_leads)} leads, {added} new")
        total_new_leads += added
    else:
        print("⚠️  Reddit scanning skipped (not configured)")
    
    print()
    
    # Scan Twitter
    if TWITTER_AVAILABLE and twitter_scanner.client:
        print("🐦 Scanning Twitter...")
        twitter_leads = twitter_scanner.scan(hours_back=1)
        added = manager.add_leads(twitter_leads)
        manager.record_scan('twitter', added)
        print(f"   ✅ Found {len(twitter_leads)} leads, {added} new")
        total_new_leads += added
    else:
        print("⚠️  Twitter scanning skipped (not configured)")
    
    print()
    print("=" * 60)
    print(f"📊 SCAN COMPLETE")
    print(f"   New leads today: {total_new_leads}")
    print(f"   Total leads: {len(manager.leads)}")
    print(f"   Last update: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Print sample of new high-intent leads
    if total_new_leads > 0:
        print("\n🎯 TOP NEW LEADS:")
        recent_leads = [l for l in manager.leads if l.get('intent') == 'high'][:3]
        for lead in recent_leads:
            print(f"\n   • {lead.get('title', 'No title')[:60]}...")
            print(f"     Source: {lead.get('sourceName', 'Unknown')}")
            print(f"     Budget: {lead.get('budget', 'Not specified')}")
            print(f"     URL: {lead.get('url', 'N/A')[:60]}...")

if __name__ == "__main__":
    main()