#!/bin/bash
# Lead Hunter Setup Script
# Run this when you have GitHub access

echo "🎯 Setting up Lead Hunter on GitHub..."

# Step 1: Create GitHub repo
echo "1. Create repo on GitHub..."
echo "   Go to: https://github.com/new"
echo "   Name: lead-hunter"
echo "   Visibility: Public"
echo "   ✅ Click 'Create repository'"
echo ""
read -p "Press Enter after creating the repo..."

# Step 2: Set remote and push
echo "2. Pushing code to GitHub..."
cd /Users/raviclaw/.openclaw/workspace/lead-hunter

# Remove existing remote if any
git remote remove origin 2>/dev/null

# Add new remote (update with your username)
echo "Enter your GitHub username:"
read USERNAME
git remote add origin https://github.com/$USERNAME/lead-hunter.git

# Push
git branch -M main
git push -u origin main

echo "✅ Code pushed to GitHub!"
echo ""

# Step 3: Enable GitHub Pages
echo "3. Enable GitHub Pages:"
echo "   Go to: https://github.com/$USERNAME/lead-hunter/settings/pages"
echo "   Source: Deploy from a branch"
echo "   Branch: main / (root)"
echo "   ✅ Click 'Save'"
echo ""
read -p "Press Enter after enabling Pages..."

echo ""
echo "🎉 Lead Hunter is now live at:"
echo "   https://$USERNAME.github.io/lead-hunter/"
echo ""

# Step 4: API Keys setup
echo "4. Next: Get API keys (see API_SETUP.md)"
echo "   - Reddit: https://www.reddit.com/prefs/apps"
echo "   - Twitter: https://developer.twitter.com/en/apply-for-access"
echo ""

echo "Done! Check API_SETUP.md for full instructions."