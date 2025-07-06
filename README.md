# Podcast2News

A full-stack web application that converts podcast content from YouTube URLs into engaging news articles using AI.

## Features

- **YouTube Transcript Extraction**: Automatically extracts transcripts from YouTube podcast URLs
- **Fallback Audio Processing**: Uses yt-dlp + Deepgram for speech-to-text when transcripts aren't available
- **AI-Powered News Generation**: Creates 3 distinct news articles from podcast content using OpenAI GPT
- **Clean UI**: Simple, modern interface built with Next.js and Tailwind CSS
- **Article Download**: Download generated articles as .txt files

## Tech Stack

### Backend
- FastAPI (Python)
- YouTube Transcript API
- yt-dlp for audio extraction
- Deepgram API for speech-to-text
- OpenAI API for news generation

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- OpenAI API key
- Deepgram API key (optional, for fallback)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```bash
# Copy from the sample file
cp ../env.sample .env

# Edit the .env file with your actual API keys
OPENAI_API_KEY=your_openai_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://podcast2news.vercel.app
```

4. Run the FastAPI server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment configuration:
```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# For production deployment, use your backend URL:
# echo "NEXT_PUBLIC_API_URL=https://your-backend-url.com" > .env.local
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### POST /generate-news
Generate news articles from a YouTube podcast URL.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "unique_session_id",
  "articles": [
    {
      "title": "Article Title",
      "content": "Article content...",
      "key_quote": "Quote from podcast"
    }
  ],
  "url": "original_url"
}
```

### GET /download-article/{session_id}/{article_index}
Download a specific article as a .txt file.

## How It Works

1. **URL Input**: User pastes a YouTube podcast URL
2. **Transcript Extraction**: 
   - First tries YouTube Transcript API
   - Falls back to yt-dlp + Deepgram if transcripts aren't available
3. **AI Processing**: OpenAI GPT analyzes the transcript and generates 3 news articles
4. **Display**: Articles are displayed in a clean, readable format
5. **Download**: Users can download articles as .txt files

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://podcast2news.vercel.app
ENVIRONMENT=development
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Features

- **URL Validation**: Only accepts valid YouTube URLs
- **CORS Protection**: Configurable allowed origins for production
- **Input Sanitization**: Prevents malicious file names and inputs
- **Temporary File Cleanup**: Automatically removes generated files after download
- **Environment-based Configuration**: Separates development and production settings

## Docker Deployment

### Local Development with Docker

1. **Using Docker Compose (Recommended)**:
```bash
# Build and start both frontend and backend
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

2. **Backend Only**:
```bash
# Build and run backend container
./deploy-backend.sh

# Or manually:
cd backend
docker build -t podcast2news-backend .
docker run -d -p 8000:8000 --env-file .env podcast2news-backend
```

### Production Deployment

1. **Cloud Deployment (Railway, Heroku, etc.)**:
```bash
# Use the production docker-compose file
docker-compose -f docker-compose.prod.yml up -d

# Or deploy backend only
cd backend
docker build -t podcast2news-backend .
docker run -d -p 8000:8000 --env-file .env podcast2news-backend
```

2. **Frontend Deployment to Vercel**:
   - Connect your GitHub repository to Vercel
   - Set environment variable: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`
   - Deploy automatically on push

### Docker Commands

```bash
# View running containers
docker ps

# View logs
docker logs podcast2news-backend-container

# Stop containers
docker-compose down

# Rebuild after changes
docker-compose up --build
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **YouTube Transcript API fails**: The app automatically falls back to audio extraction + Deepgram
2. **OpenAI API errors**: Check that your API key is valid and has sufficient credits
3. **CORS issues**: Ensure the frontend URL is included in the backend CORS settings

### Dependencies

If you encounter issues with audio processing, ensure you have ffmpeg installed:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
``` 