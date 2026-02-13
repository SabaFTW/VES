#!/bin/bash

# 🜂 GITHUB TOKEN FINAL FIX 🜂
# Enkrat za vedno reši token problem!

echo "🜂 GITHUB TOKEN - FINAL FIX 🜂"
echo "================================"

# Step 1: Store credentials permanently
echo ""
echo "📝 Step 1: Enabling credential storage..."
git config --global credential.helper store

# Step 2: Set your identity
echo ""
echo "👤 Step 2: Setting your identity..."
read -p "Enter your GitHub username: " github_user
read -p "Enter your GitHub email: " github_email

git config --global user.name "$github_user"
git config --global user.email "$github_email"

# Step 3: Go to VES repo
echo ""
echo "📂 Step 3: Going to VES repo..."
cd /home/saba/Desktop/VEZ/VES

# Step 4: Check remote URL
echo ""
echo "🔗 Step 4: Checking remote URL..."
current_url=$(git remote get-url origin)
echo "Current URL: $current_url"

# Step 5: Set correct URL format
echo ""
echo "🔧 Step 5: Setting correct URL format..."
git remote set-url origin "https://github.com/$github_user/VES.git"

echo ""
echo "✅ Configuration complete!"
echo ""
echo "🔑 NEXT STEPS:"
echo "1. Go get your GitHub token:"
echo "   https://github.com/settings/tokens"
echo ""
echo "2. Click 'Generate new token (classic)'"
echo "3. Give it a name: 'VES_Token'"
echo "4. Select scopes: 'repo' (full control)"
echo "5. Click 'Generate token'"
echo "6. COPY THE TOKEN (you'll only see it once!)"
echo ""
read -p "Press ENTER when you have your token ready..."

echo ""
echo "🚀 Now let's test it!"
echo ""
echo "Running: git add . && git commit && git push"
echo ""

# Do the push
git add .
read -p "Enter commit message: " commit_msg
git commit -m "$commit_msg"

echo ""
echo "⚠️  IMPORTANT: When asked for password, PASTE YOUR TOKEN!"
echo "   (Not your GitHub password - your TOKEN!)"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Git will remember this token forever!"
    echo "   You'll never need to enter it again!"
else
    echo ""
    echo "❌ Something went wrong. Let's try alternative method..."
    echo ""
    echo "Alternative: Set token in URL directly"
    read -p "Paste your token here: " github_token
    git remote set-url origin "https://${github_token}@github.com/${github_user}/VES.git"
    echo "✅ Token saved in URL. Try pushing again:"
    echo "   git push"
fi

echo ""
echo "🜂 SIDRO STOJI! TOKEN IS SAVED! 🜂"
