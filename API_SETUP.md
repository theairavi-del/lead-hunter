# Lead Hunter v2.0 - API Setup Guide

This guide will walk you through setting up real API integrations for Reddit and Twitter.

## Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Reddit API Setup

### Step 1: Create a Reddit App
1. Go to https://www.reddit.com/prefs/apps
2. Scroll down and click **"create another app..."**
3. Fill in the form:
   - **Name**: Lead Hunter
   - **App type**: Script
   - **Description**: Lead generation for web development
   - **About URL**: (your website or GitHub)
   - **Redirect URI**: http://localhost:8080
4. Click **"create app"**

### Step 2: Get Your Credentials
After creating the app, you'll see:
- **client_id**: The string under "personal use script"
- **client_secret**: The secret string

### Step 3: Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

Add your Reddit credentials:
```
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_client_secret
REDDIT_USER_AGENT=LeadHunter/1.0 by YourRedditUsername
```

## Twitter API Setup

### Step 1: Apply for Developer Account
1. Go to https://developer.twitter.com/en/apply-for-access
2. Apply for **Elevated** access (needed for search)
3. Fill out the application explaining your use case
4. Wait for approval (usually instant for Elevated)

### Step 2: Create a Project & App
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a **New Project**
3. Create an **App** within the project
4. Go to **Keys and Tokens** tab

### Step 3: Get Bearer Token
1. In your app's "Keys and Tokens" section
2. Find **"Bearer Token"**
3. Click **"Regenerate"** if needed
4. Copy the token

### Step 4: Configure
Add to your `.env` file:
```
TWITTER_BEARER_TOKEN=your_actual_bearer_token
```

## Test Your Setup

```bash
# Run the research agent
python research_agent_v2.py
```

You should see output like:
```
============================================================
🔍 LEAD HUNTER v2.0 - Real API Integration
============================================================
⏰ Started: 2024-01-15 14:30:00

✅ Reddit API connected
✅ Twitter API connected

🌐 Scanning Reddit...
  🔍 Scanning r/webdev...
  🔍 Scanning r/forhire...
  ✅ Found 3 leads, 2 new

🐦 Scanning Twitter...
  🔍 Searching Twitter: 'need a website'...
  ✅ Found 1 leads, 1 new

============================================================
📊 SCAN COMPLETE
   New leads today: 3
   Total leads: 15
   Last update: 14:35:22
============================================================
```

## Setting Up Automation

### Option 1: Cron Job (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add this line to run every hour
0 * * * * cd /path/to/lead-hunter && /usr/bin/python3 research_agent_v2.py >> scan.log 2>&1

# View logs
tail -f scan.log
```

### Option 2: GitHub Actions (Recommended - Cloud)

Create `.github/workflows/scan.yml`:

```yaml
name: Hourly Lead Scan

on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:  # Allow manual trigger

jobs:
  scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repo
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: pip install -r requirements.txt
      
    - name: Run scanner
      env:
        REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
        REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
        REDDIT_USER_AGENT: ${{ secrets.REDDIT_USER_AGENT }}
        TWITTER_BEARER_TOKEN: ${{ secrets.TWITTER_BEARER_TOKEN }}
      run: python research_agent_v2.py
      
    - name: Commit and push if changes
      run: |
        git config user.name "Lead Hunter Bot"
        git config user.email "bot@example.com"
        git add leads.json scan_history.json
        git diff --staged --quiet || git commit -m "Update leads - $(date)"
        git push
```

Then add your secrets to GitHub:
1. Go to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT`
   - `TWITTER_BEARER_TOKEN`

### Option 3: PythonAnywhere (Free Cloud Hosting)

1. Sign up at https://www.pythonanywhere.com
2. Upload your code
3. Set environment variables in dashboard
4. Create a scheduled task (daily limit on free tier)

## Customization

### Adjust Scan Frequency
Edit the cron expression:
- Every 30 minutes: `*/30 * * * *`
- Every 2 hours: `0 */2 * * *`
- Every 6 hours: `0 */6 * * *`

### Change Subreddits
Edit `TARGET_SUBREDDITS` in `research_agent_v2.py`:
```python
TARGET_SUBREDDITS = [
    "webdev",
    "forhire",
    "your_custom_subreddit",
    # Add more...
]
```

### Modify Search Queries
Edit `TWITTER_QUERIES`:
```python
TWITTER_QUERIES = [
    "need a website",
    "looking for web developer",
    "your custom query",
    # Add more...
]
```

### Filter by Budget
Edit `BUDGET_PATTERNS` to catch different formats:
```python
BUDGET_PATTERNS = [
    r'\$[\d,]+(?:k)?',  # $500, $2k
    r'\d+\s*(?:k|thousand)',  # 2k, 3 thousand
    r'budget\s*[:\-]?\s*\$?\d+',  # budget: 500
]
```

## Troubleshooting

### "Reddit API connection failed"
- Check your credentials in `.env`
- Make sure your Reddit app is set to "Script" type
- Verify your user agent format: `AppName/1.0 by Username`

### "Twitter API connection failed"
- Ensure you have Elevated access (not just Essential)
- Check bearer token is correct
- Verify token hasn't expired (regenerate if needed)

### "No leads found"
- This is normal! Real leads are sporadic
- Try extending `hours_back` to scan further in time
- Check that subreddits/queries match your target market

### "Rate limit exceeded"
- Reddit: 60 requests/minute (built-in delays help)
- Twitter: 450 requests/15 minutes
- Increase sleep times in scanner if needed

## Rate Limits & Ethics

### Reddit
- 60 requests/minute for OAuth
- Be respectful - don't spam
- Follow subreddit rules
- Consider adding `time.sleep(2)` between requests

### Twitter
- 450 requests/15 min for search (Elevated)
- 100 requests/24 hours for some endpoints
- Follow Twitter's automation rules
- Don't auto-reply or DM without consent

### Best Practices
- Only contact people who explicitly asked for help
- Personalize each outreach message
- Don't spam the same subreddit
- Be transparent that you're a developer

## Next Steps

1. ✅ Set up API credentials
2. ✅ Test the scanner
3. ✅ Set up automation (cron/GitHub Actions)
4. ✅ Check dashboard for new leads
5. 💰 Start reaching out to leads!

## Support

If you run into issues:
1. Check the logs: `tail -f scan.log`
2. Verify API credentials work independently
3. Test with smaller subreddit list first
4. Check rate limit status

Happy hunting! 🎯