#!/usr/bin/env python3
"""
Reddit Web Scraper - No API Required
Scrapes r/webdev, r/forhire, etc. for real posts
"""

import json
import os
import random
import re
import time
import subprocess
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False
    print("⚠️  Install: pip3 install --break-system-packages requests beautifulsoup4")

LEADS_FILE = "leads.json"
MAX_LEADS = 50

# Subreddits to scrape
SUBREDDITS = ["webdev", "forhire", "smallbusiness", "Entrepreneur", "web_design", "Wordpress"]

# Keywords to look for
KEYWORDS = ["website", "web developer", "web designer", "portfolio", "landing page", 
            "need a site", "build a website", "hire", "looking for"]

def scrape_subreddit(subreddit, limit=10):
    """Scrape a subreddit for posts"""
    if not SCRAPING_AVAILABLE:
        return []
    
    url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit={limit}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"  ⚠️  Error scraping r/{subreddit}: {response.status_code}")
            return []
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        leads = []
        for post in posts:
            post_data = post.get('data', {})
            
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            full_text = f"{title} {selftext}".lower()
            
            # Check if post matches our keywords
            if not any(kw in full_text for kw in KEYWORDS):
                continue
            
            # Extract budget
            budget = extract_budget(full_text)
            
            # Determine intent
            intent = determine_intent(full_text, budget)
            
            # Generate design concept
            design_mockup, design_notes = generate_design_concept(title, selftext)
            
            lead = {
                "id": f"reddit_{post_data.get('id')}",
                "source": "reddit",
                "sourceName": f"r/{subreddit}",
                "title": title[:100],
                "description": (selftext[:300] + "...") if len(selftext) > 300 else selftext,
                "url": f"https://reddit.com{post_data.get('permalink')}",
                "author": post_data.get('author', 'unknown'),
                "timestamp": datetime.now().isoformat(),
                "tags": generate_tags(full_text),
                "intent": intent,
                "budget": budget,
                "score": calculate_score(full_text, budget),
                "designMockup": design_mockup,
                "designNotes": design_notes,
                "contacted": False,
                "notes": ""
            }
            leads.append(lead)
        
        return leads
        
    except Exception as e:
        print(f"  ⚠️  Error scraping r/{subreddit}: {e}")
        return []

def extract_budget(text):
    """Extract budget mentions from text"""
    patterns = [
        r'\$[\d,]+(?:k)?',
        r'\d+\s*(?:k|thousand)',
        r'budget\s*(?:of\s*)?(?:is\s*)?\$?[\d,]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def determine_intent(text, budget):
    """Determine lead intent level"""
    high_keywords = ['budget', 'pay', 'hiring', 'asap', 'urgent', 'paid']
    score = 0
    if budget:
        score += 5
    for kw in high_keywords:
        if kw in text:
            score += 2
    
    if score >= 8:
        return "high"
    elif score >= 4:
        return "medium"
    return "low"

def generate_tags(text):
    """Generate tags from post content"""
    tags = []
    text_lower = text.lower()
    
    if 'portfolio' in text_lower:
        tags.append('Portfolio')
    if 'ecommerce' in text_lower or 'shopify' in text_lower or 'woocommerce' in text_lower:
        tags.append('E-commerce')
    if 'landing page' in text_lower:
        tags.append('Landing Page')
    if 'wordpress' in text_lower:
        tags.append('WordPress')
    if 'react' in text_lower:
        tags.append('React')
    if 'saas' in text_lower:
        tags.append('SaaS')
    if 'mvp' in text_lower:
        tags.append('MVP')
    
    if not tags:
        tags.append('Website')
    
    return tags[:4]

def generate_design_concept(title, text):
    """Generate design mockup based on content"""
    full_text = f"{title} {text}".lower()
    
    if 'portfolio' in full_text or 'photography' in full_text:
        return ("📸", "Gallery-focused layout, lightbox for images, about section, contact form. Clean typography, image-first design.")
    if 'ecommerce' in full_text or 'shop' in full_text or 'store' in full_text:
        return ("🛒", "Product grid layout, shopping cart, checkout flow, payment integration. Mobile-optimized.")
    if 'saas' in full_text or 'landing page' in full_text:
        return ("🚀", "Hero with product demo, feature sections, pricing cards. CTA-focused, conversion optimized.")
    if 'restaurant' in full_text or 'food' in full_text:
        return ("🍽️", "Menu display, reservation system, online ordering. Appetizing imagery.")
    if 'real estate' in full_text or 'property' in full_text:
        return ("🏠", "Property listings, search filters, agent profiles. Professional luxury design.")
    
    return ("💻", "Modern responsive design, clear navigation, strong CTAs, mobile-first approach.")

def calculate_score(text, budget):
    """Calculate lead score"""
    score = 5  # Base score for matching keywords
    if budget:
        score += 5
    high_intent = ['budget', 'pay', 'hiring', 'asap', 'urgent', 'paid']
    for kw in high_intent:
        if kw in text:
            score += 3
    return min(score, 25)

def load_existing_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

def push_to_github():
    try:
        subprocess.run(['git', 'add', LEADS_FILE], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update leads with real Reddit posts - {datetime.now().strftime("%H:%M")}'], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        return True
    except Exception as e:
        print(f"⚠️  Git push failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 REDDIT WEB SCRAPER - Real Posts")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not SCRAPING_AVAILABLE:
        print("❌ Install required: pip3 install --break-system-packages requests beautifulsoup4")
        return
    
    existing_leads = load_existing_leads()
    existing_urls = {lead.get('url') for lead in existing_leads}
    print(f"📊 Current leads: {len(existing_leads)}")
    
    all_new_leads = []
    
    for subreddit in SUBREDDITS:
        print(f"🌐 Scraping r/{subreddit}...")
        leads = scrape_subreddit(subreddit, limit=15)
        
        for lead in leads:
            if lead['url'] not in existing_urls:
                all_new_leads.append(lead)
                existing_urls.add(lead['url'])
        
        time.sleep(2)  # Be nice to Reddit
    
    print(f"\n✅ Found {len(all_new_leads)} new leads")
    
    # Add to existing leads
    combined = all_new_leads + existing_leads
    combined = combined[:MAX_LEADS]
    
    save_leads(combined)
    
    if all_new_leads:
        print("🚀 Pushing to GitHub...")
        if push_to_github():
            print("✅ GitHub updated!")
        
        print("\n🎯 NEW LEADS:")
        for lead in all_new_leads[:5]:
            print(f"\n   • {lead['title'][:60]}...")
            print(f"     Source: {lead['sourceName']}")
            print(f"     Budget: {lead.get('budget', 'Not specified')}")
            print(f"     URL: {lead['url']}")
    
    print()
    print("=" * 60)
    print(f"📊 TOTAL LEADS: {len(combined)}")
    print("=" * 60)

if __name__ == "__main__":
    main()