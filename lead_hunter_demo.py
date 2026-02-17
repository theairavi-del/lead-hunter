#!/usr/bin/env python3
"""
Lead Hunter - Demo Mode (No API Required)
Generates realistic sample leads every 30 minutes
Updates leads.json and pushes to GitHub
"""

import json
import os
import random
import subprocess
from datetime import datetime, timedelta

LEADS_FILE = "leads.json"
MAX_LEADS = 50

SAMPLE_LEADS = [
    {
        "source": "reddit",
        "sourceName": "r/webdev",
        "title": "Need a portfolio website for my photography business",
        "description": "Looking for someone to build a clean, minimalist portfolio site. Budget is $500-800. Need it within 2 weeks. Based in NYC.",
        "tags": ["Portfolio", "Photography", "$500-800", "2 weeks"],
        "intent": "high",
        "budget": "$500-800",
        "designMockup": "📸",
        "designNotes": "Minimalist gallery layout, lightbox feature, contact form, about section. Mobile-first approach with emphasis on image quality."
    },
    {
        "source": "reddit",
        "sourceName": "r/forhire",
        "title": "Startup needs landing page for SaaS product launch",
        "description": "We're launching a new productivity tool and need a converting landing page. Have copy ready, need design + dev. Budget $2k-3k.",
        "url": "#",
        "tags": ["Landing Page", "SaaS", "$2k-3k", "Startup"],
        "intent": "high",
        "budget": "$2k-3k",
        "designMockup": "🚀",
        "designNotes": "Hero with product screenshot, feature grid, pricing section, CTA buttons. Dark mode option. Conversion-focused design."
    },
    {
        "source": "reddit",
        "sourceName": "r/smallbusiness",
        "title": "Restaurant needs online ordering website",
        "description": "Family restaurant wants to add online ordering to our site. Need menu display and Square integration. Budget around $1,500.",
        "tags": ["Restaurant", "E-commerce", "$1,500", "Square"],
        "intent": "high",
        "budget": "$1,500",
        "designMockup": "🍽️",
        "designNotes": "Menu with categories, cart functionality, checkout flow, order management. Mobile-friendly with appetizing imagery."
    },
    {
        "source": "reddit",
        "sourceName": "r/Entrepreneur",
        "title": "Looking for web dev to build MVP for fitness app",
        "description": "Have validated my fitness tracking idea, now need someone to build the MVP. React preferred. Budget $3-5k, timeline 6 weeks.",
        "tags": ["MVP", "Fitness", "$3-5k", "React"],
        "intent": "high",
        "budget": "$3-5k",
        "designMockup": "💪",
        "designNotes": "Dashboard interface, workout tracking, progress charts, user profiles. Motivational design with gamification elements."
    },
    {
        "source": "reddit",
        "sourceName": "r/Wordpress",
        "title": "Real estate agent needs website redesign",
        "description": "Current website is outdated and slow. Need modern site with MLS integration and lead capture forms. Budget $2k.",
        "tags": ["Real Estate", "Redesign", "$2k", "MLS"],
        "intent": "medium",
        "budget": "$2k",
        "designMockup": "🏠",
        "designNotes": "Property listings with search, agent profiles, contact forms. Professional luxury aesthetic with map integration."
    },
    {
        "source": "reddit",
        "sourceName": "r/web_design",
        "title": "Personal brand website for content creator",
        "description": "YouTuber looking for sleek personal website. Need blog, video embeds, newsletter signup. Budget $800-1200.",
        "tags": ["Personal Brand", "Content", "$800-1200", "Blog"],
        "intent": "medium",
        "budget": "$800-1200",
        "designMockup": "✨",
        "designNotes": "Modern personal brand site, video integration, blog grid, newsletter capture. Bold typography and social links."
    },
    {
        "source": "reddit",
        "sourceName": "r/ecommerce",
        "title": "WooCommerce expert needed for custom features",
        "description": "Have WooCommerce site but need product configurator and custom checkout. Budget flexible, around $2k-4k.",
        "tags": ["WooCommerce", "E-commerce", "$2k-4k", "Custom"],
        "intent": "high",
        "budget": "$2k-4k",
        "designMockup": "🛒",
        "designNotes": "Product customization interface, optimized cart, streamlined checkout, upsell features. Conversion optimized."
    },
    {
        "source": "reddit",
        "sourceName": "r/indiehackers",
        "title": "Need developer for marketplace MVP",
        "description": "Building a niche marketplace platform. Need help with frontend. Budget $5k or equity split. Remote OK.",
        "tags": ["Marketplace", "MVP", "$5k", "Equity"],
        "intent": "medium",
        "budget": "$5k + equity",
        "designMockup": "🛍️",
        "designNotes": "Two-sided marketplace, user profiles, listing pages, messaging system. Clean trust-building design."
    },
    {
        "source": "reddit",
        "sourceName": "r/webdev",
        "title": "Law firm needs professional website",
        "description": "Small law practice needs modern, trustworthy website. 5-6 pages, contact forms, blog. Budget $1,500-2,500.",
        "tags": ["Law Firm", "Professional", "$1,500-2,500"],
        "intent": "high",
        "budget": "$1,500-2,500",
        "designMockup": "⚖️",
        "designNotes": "Professional, trustworthy design with attorney profiles, practice areas, contact forms. Conservative color palette."
    },
    {
        "source": "reddit",
        "sourceName": "r/forhire",
        "title": "E-commerce site for handmade jewelry brand",
        "description": "Looking for Shopify or custom e-commerce solution. 50-100 products, Instagram integration. Budget $1,000-1,800.",
        "tags": ["E-commerce", "Jewelry", "$1,000-1,800", "Shopify"],
        "intent": "medium",
        "budget": "$1,000-1,800",
        "designMockup": "💎",
        "designNotes": "Elegant product showcase, zoom features, Instagram feed integration, simple checkout. Feminine aesthetic."
    }
]

def load_existing_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

def generate_new_lead():
    """Generate a new lead with timestamp"""
    template = random.choice(SAMPLE_LEADS).copy()
    template['id'] = f"demo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}"
    template['timestamp'] = datetime.now().isoformat()
    template['url'] = f"https://reddit.com/r/{template['sourceName'].replace('r/', '')}/comments/demo{random.randint(10000,99999)}"
    template['author'] = f"user_{random.randint(10000,99999)}"
    template['score'] = random.randint(10, 25)
    template['contacted'] = False
    template['notes'] = ""
    return template

def push_to_github():
    """Push updates to GitHub"""
    try:
        subprocess.run(['git', 'add', LEADS_FILE], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update leads - {datetime.now().strftime("%H:%M")}'], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        return True
    except Exception as e:
        print(f"⚠️  Git push failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 LEAD HUNTER - DEMO MODE (No API Required)")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load existing leads
    leads = load_existing_leads()
    print(f"📊 Current leads: {len(leads)}")
    
    # Generate 0-2 new leads (random)
    num_new = random.randint(0, 2)
    print(f"🎲 Generating {num_new} new leads...")
    
    new_leads = []
    for _ in range(num_new):
        new_lead = generate_new_lead()
        leads.insert(0, new_lead)  # Add to beginning
        new_leads.append(new_lead)
    
    # Keep only max leads
    leads = leads[:MAX_LEADS]
    
    # Save
    save_leads(leads)
    print(f"💾 Saved {len(leads)} leads")
    
    # Push to GitHub
    if new_leads:
        print("🚀 Pushing to GitHub...")
        if push_to_github():
            print("✅ GitHub updated!")
        else:
            print("⚠️  GitHub push failed (manual push needed)")
    
    print()
    print("=" * 60)
    print(f"📊 SCAN COMPLETE")
    print(f"   New leads: {len(new_leads)}")
    print(f"   Total leads: {len(leads)}")
    print(f"   Last update: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    if new_leads:
        print("\n🎯 NEW LEADS:")
        for lead in new_leads:
            print(f"\n   • {lead['title'][:60]}...")
            print(f"     Source: {lead['sourceName']}")
            print(f"     Budget: {lead.get('budget', 'Not specified')}")

if __name__ == "__main__":
    main()