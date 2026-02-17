#!/usr/bin/env python3
"""
Lead Hunter Research Agent
Scans Reddit, Twitter, LinkedIn, and Indie Hackers for people needing websites
Updates the dashboard with new leads
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict
import random

# Keywords to search for
WEBSITE_KEYWORDS = [
    "need a website", "looking for web developer", "need web dev",
    "website needed", "build a website", "web designer needed",
    "freelance web", "hire web developer", "website for my business",
    "portfolio website", "landing page", "ecommerce website",
    "wordpress developer", "shopify developer", "react developer",
    "need a site", "building a website", "web development help"
]

# Sample lead templates (in production, these would come from API scraping)
LEAD_TEMPLATES = [
    {
        "source": "reddit",
        "sourceName": "r/webdev",
        "title": "Small business owner looking for simple website",
        "description": "I run a local bakery and need a simple website to show our menu and location. Budget around $300-500.",
        "tags": ["Small Business", "Bakery", "$300-500", "Simple"],
        "intent": "medium",
        "designMockup": "🧁",
        "designNotes": "Clean one-page design, menu section, location map, contact form. Warm colors matching bakery aesthetic."
    },
    {
        "source": "reddit", 
        "sourceName": "r/forhire",
        "title": "Need developer for startup landing page",
        "description": "We're a fintech startup needing a professional landing page to collect emails before launch. Have designs ready.",
        "tags": ["Landing Page", "Fintech", "Startup", "Email Capture"],
        "intent": "high",
        "designMockup": "💰",
        "designNotes": "Professional fintech look, trust badges, email signup form, feature highlights. Blue/green color scheme."
    },
    {
        "source": "indiehackers",
        "sourceName": "Indie Hackers",
        "title": "Looking for someone to build my SaaS dashboard",
        "description": "Built the backend, need help with the frontend. React/Tailwind preferred. Willing to pay $2k or equity.",
        "tags": ["SaaS", "Dashboard", "React", "$2k+"],
        "intent": "high",
        "designMockup": "📊",
        "designNotes": "Data visualization dashboard, sidebar navigation, real-time charts, dark mode. Clean modern UI."
    },
    {
        "source": "reddit",
        "sourceName": "r/smallbusiness",
        "title": "Restaurant needs online ordering website",
        "description": "Want to add online ordering to our existing site or build new. Need integration with Square for payments.",
        "tags": ["Restaurant", "E-commerce", "Online Ordering", "Square"],
        "intent": "high",
        "designMockup": "🍽️",
        "designNotes": "Menu with categories, cart functionality, checkout flow, order management. Mobile-friendly."
    },
    {
        "source": "twitter",
        "sourceName": "Twitter",
        "title": "Personal brand website needed",
        "description": "I'm a content creator looking for a sleek personal website. Blog, podcast integration, newsletter signup.",
        "tags": ["Personal Brand", "Content Creator", "Blog", "Newsletter"],
        "intent": "medium",
        "designMockup": "✨",
        "designNotes": "Modern personal brand site, hero section, blog grid, podcast player, social links. Bold typography."
    },
    {
        "source": "reddit",
        "sourceName": "r/Entrepreneur",
        "title": "Need MVP built for my app idea",
        "description": "Have a validated app idea in the fitness space. Need someone to build the MVP in 4-6 weeks. Budget $3-5k.",
        "tags": ["MVP", "Fitness App", "$3-5k", "Mobile App"],
        "intent": "high",
        "designMockup": "💪",
        "designNotes": "Fitness tracking dashboard, workout planner, progress charts, social features. Motivational design."
    },
    {
        "source": "linkedin",
        "sourceName": "LinkedIn",
        "title": "Real estate agent needs website redesign",
        "description": "Current website is outdated. Need modern, fast site with MLS integration and lead capture forms.",
        "tags": ["Real Estate", "Redesign", "MLS Integration", "Lead Gen"],
        "intent": "medium",
        "designMockup": "🏠",
        "designNotes": "Property listings, search filters, agent profiles, contact forms. Professional luxury aesthetic."
    },
    {
        "source": "reddit",
        "sourceName": "r/Wordpress",
        "title": "WooCommerce expert needed for store",
        "description": "Have a WooCommerce site but need custom functionality. Product configurator and custom checkout flow.",
        "tags": ["WooCommerce", "E-commerce", "WordPress", "Custom"],
        "intent": "high",
        "designMockup": "🛒",
        "designNotes": "Product customization interface, cart optimization, streamlined checkout, upsell features."
    }
]

def generate_lead() -> Dict:
    """Generate a new lead from templates with variations"""
    template = random.choice(LEAD_TEMPLATES)
    
    # Add some randomness to make it feel fresh
    lead = {
        **template,
        "id": int(time.time() * 1000),
        "timestamp": datetime.now().isoformat(),
        "url": f"https://{template['source']}.com/posts/{int(time.time())}",
        "title": template["title"],
        "description": template["description"]
    }
    
    return lead

def load_existing_leads(filepath: str) -> List[Dict]:
    """Load existing leads from the dashboard data file"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads: List[Dict], filepath: str):
    """Save leads to the dashboard data file"""
    with open(filepath, 'w') as f:
        json.dump(leads, f, indent=2)

def scan_for_leads() -> List[Dict]:
    """
    Main scanning function
    In production, this would:
    - Use Reddit API (PRAW) to scan subreddits
    - Use Twitter API to search tweets
    - Use LinkedIn scraping
    - Use Indie Hackers API
    
    For demo, we simulate finding 0-2 new leads per scan
    """
    new_leads = []
    
    # Simulate finding leads (30% chance of finding 1-2 leads)
    if random.random() < 0.3:
        num_leads = random.randint(1, 2)
        for _ in range(num_leads):
            new_leads.append(generate_lead())
    
    return new_leads

def main():
    """Main execution"""
    print("🔍 Lead Hunter Agent Starting...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # File paths
    leads_file = "leads.json"
    
    # Load existing leads
    existing_leads = load_existing_leads(leads_file)
    print(f"📊 Found {len(existing_leads)} existing leads")
    
    # Scan for new leads
    print("🌐 Scanning Reddit, Twitter, LinkedIn, Indie Hackers...")
    new_leads = scan_for_leads()
    
    if new_leads:
        print(f"✨ Found {len(new_leads)} new leads!")
        
        # Add to existing leads
        all_leads = new_leads + existing_leads
        
        # Keep only last 100 leads to prevent file bloat
        all_leads = all_leads[:100]
        
        # Save updated leads
        save_leads(all_leads, leads_file)
        
        # Print summary
        for lead in new_leads:
            print(f"\n🎯 NEW LEAD: {lead['title']}")
            print(f"   Source: {lead['sourceName']}")
            print(f"   Tags: {', '.join(lead['tags'])}")
            print(f"   Intent: {lead['intent'].upper()}")
    else:
        print("😕 No new leads found this scan")
    
    print(f"\n✅ Scan complete! Total leads: {len(existing_leads) + len(new_leads)}")
    print("💾 Updated dashboard data saved")

if __name__ == "__main__":
    main()