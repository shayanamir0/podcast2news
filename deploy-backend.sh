#!/bin/bash

# Build and Deploy Backend Script

echo "🚀 Building and deploying Podcast2News backend..."

# Navigate to backend directory
cd backend

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t podcast2news-backend .

# Stop and remove existing container if running
echo "🛑 Stopping existing container if running..."
docker stop podcast2news-backend-container 2>/dev/null || true
docker rm podcast2news-backend-container 2>/dev/null || true

# Run the container
echo "🏃 Running the container..."
docker run -d \
  --name podcast2news-backend-container \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  podcast2news-backend

echo "✅ Backend deployed successfully!"
echo "📡 Backend is running on http://localhost:8000"
echo "🔍 Check status with: docker ps"
echo "📋 View logs with: docker logs podcast2news-backend-container" 