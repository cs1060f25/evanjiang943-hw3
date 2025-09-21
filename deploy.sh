#!/bin/bash

# AI-Assisted Grading Platform - Vercel Deployment Script
# This script helps deploy the frontend to Vercel

echo "🚀 Starting Vercel deployment for AI-Assisted Grading Platform..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Build the project
echo "🔨 Building the project..."
npm run build

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "📝 Note: Backend needs to be deployed separately (Flask/Python)"
echo "💡 Consider using Railway, Heroku, or Render for the backend"
