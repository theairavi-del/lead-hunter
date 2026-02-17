# 🎯 Lead Hunter

**Automated Web Development Lead Generation Dashboard**

Scans Reddit, Twitter, LinkedIn, and Indie Hackers hourly for people needing websites. Displays leads with AI-generated design concepts.

![Lead Hunter Dashboard](screenshot.png)

## Features

- 🔍 **Multi-Platform Scanning**: Reddit, Twitter, LinkedIn, Indie Hackers
- 🤖 **AI Design Concepts**: Auto-generates design mockups for each lead
- 📊 **Lead Scoring**: High/medium/low intent classification
- 🏷️ **Smart Tagging**: Budget, timeline, project type auto-extracted
- 💾 **Persistent Storage**: Saves leads locally
- 📱 **Responsive Design**: Works on all devices

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/lead-hunter.git
cd lead-hunter
```

### 2. Open Dashboard
Simply open `index.html` in your browser, or deploy to GitHub Pages:
```bash
# Push to GitHub, then enable Pages in repo settings
```

### 3. Run Research Agent (Optional - for auto-updates)
```bash
# Install Python dependencies
pip install requests praw tweepy

# Run manual scan
python research_agent.py

# Or set up cron job for hourly scans (Mac/Linux)
crontab -e
# Add: 0 * * * * cd /path/to/lead-hunter && python research_agent.py
```

## Project Structure

```
lead-hunter/
├── index.html          # Main dashboard
├── research_agent.py   # Lead scanning script
├── leads.json          # Lead data (auto-generated)
└── README.md           # This file
```

## How It Works

1. **Research Agent** (`research_agent.py`)
   - Runs every hour via cron job
   - Scans multiple platforms for keywords like "need a website", "looking for web developer"
   - Extracts budget, timeline, project details
   - Generates design concepts
   - Saves to `leads.json`

2. **Dashboard** (`index.html`)
   - Loads leads from `leads.json`
   - Displays in card format with design previews
   - Filter by source, intent level
   - One-click to view original post

## Customization

### Add Your Own Leads Manually
```javascript
// In browser console
addNewLead({
    source: 'reddit',
    sourceName: 'r/webdev',
    title: 'Your custom lead title',
    description: 'Lead description here',
    tags: ['Tag1', 'Tag2', '$500'],
    intent: 'high',
    designMockup: '🎨',
    designNotes: 'Your design concept',
    url: 'https://reddit.com/r/webdev/posts/...'
});
```

### Modify Keywords
Edit `WEBSITE_KEYWORDS` in `research_agent.py`:
```python
WEBSITE_KEYWORDS = [
    "need a website",
    "looking for web developer",
    # Add your keywords
]
```

## API Integration (Production Setup)

To enable real scanning, add API credentials:

### Reddit (PRAW)
```python
# research_agent.py
reddit = praw.Reddit(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="Lead Hunter v1.0"
)
```

### Twitter API
```python
import tweepy
client = tweepy.Client(bearer_token="YOUR_TOKEN")
```

### LinkedIn
Use proxycurl or similar for LinkedIn scraping.

## Deployment

### GitHub Pages (Recommended - Free)
1. Push to GitHub repo
2. Go to Settings → Pages
3. Select "Deploy from branch" → main → / (root)
4. Your dashboard is live at `https://YOUR_USERNAME.github.io/lead-hunter/`

### Cloudflare Pages
```bash
# Install Wrangler
npm install -g wrangler

# Deploy
wrangler pages deploy .
```

## Automation Setup

### Mac/Linux (Cron)
```bash
# Edit crontab
crontab -e

# Add hourly scan
0 * * * * cd /path/to/lead-hunter && /usr/bin/python3 research_agent.py >> scan.log 2>&1
```

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every hour
4. Action: Start Program
5. Program: `python.exe`
6. Arguments: `research_agent.py`
7. Start in: `C:\path\to\lead-hunter`

### GitHub Actions (Free Cloud Option)
Create `.github/workflows/scan.yml`:
```yaml
name: Hourly Lead Scan
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run scanner
        run: python research_agent.py
      - name: Commit results
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add leads.json
          git commit -m "Update leads" || exit 0
          git push
```

## Tips for Success

1. **Act Fast**: Contact leads within 1-2 hours of posting
2. **Personalize**: Reference their specific project details
3. **Show Portfolio**: Include relevant past work
4. **Be Professional**: Clear pricing, timeline, process
5. **Follow Up**: Many leads convert on 2nd or 3rd contact

## Lead Quality Indicators

🟢 **High Intent**
- Specific budget mentioned
- Clear timeline
- Detailed requirements
- "Hiring" or "Paid" in post

🟡 **Medium Intent**
- Budget range given
- Some details provided
- Open to discussion

🔴 **Low Intent**
- No budget mentioned
- Vague requirements
- "Just exploring"

## Privacy & Ethics

- Only scrape public posts
- Don't spam or cold email excessively
- Respect platform ToS
- Be transparent about your services

## License

MIT License - Feel free to use and modify!

## Support

Questions? Issues? Open a GitHub issue or reach out on Twitter.

---

Built with ❤️ for freelancers and agencies looking to grow their client base.