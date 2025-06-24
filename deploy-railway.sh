#!/bin/bash

# Railway Deployment Script
# This script helps set up your voting app on Railway

echo "🚂 Railway Deployment Helper"
echo "=============================="

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "📋 Setting up your project..."

# Login to Railway
echo "🔐 Please login to Railway:"
railway login

# Create new project
echo "🆕 Creating new Railway project..."
railway init

# Add Redis database
echo "🗄️  Adding Redis database..."
echo "Please go to your Railway dashboard and add a Redis database:"
echo "1. Open https://railway.app/dashboard"
echo "2. Click on your project"
echo "3. Click 'New' → 'Database' → 'Add Redis'"
echo "4. Railway will automatically set REDIS_URL environment variable"
echo ""
read -p "Press Enter after you've added Redis database..."

# Set environment variables
echo "⚙️  Setting environment variables..."
railway variables set VOTE1VALUE="Pizza"
railway variables set VOTE2VALUE="Brownie"
railway variables set TITLE="My Voting App"
railway variables set FLASK_ENV="production"

echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at the URL shown above"
echo ""
echo "💡 To update your app in the future:"
echo "   1. Make your changes"
echo "   2. Run: railway up"
echo ""
echo "📊 To view logs: railway logs"
echo "⚙️  To manage variables: railway variables"
