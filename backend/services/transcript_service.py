import asyncio
import os
import tempfile
import io
from typing import Optional
from urllib.parse import urlparse, parse_qs
import re

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_AVAILABLE = False
    print("Warning: youtube-transcript-api not installed. Will use fallback method.")

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("Warning: yt-dlp not installed. Fallback audio extraction won't work.")

try:
    from deepgram import DeepgramClient, PrerecordedOptions
    DEEPGRAM_AVAILABLE = True
except ImportError:
    DEEPGRAM_AVAILABLE = False
    print("Warning: deepgram-sdk not installed. Speech-to-text fallback won't work.")

class TranscriptService:
    def __init__(self):
        self.deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        if DEEPGRAM_AVAILABLE and self.deepgram_api_key:
            self.deepgram_client = DeepgramClient(self.deepgram_api_key)
        else:
            self.deepgram_client = None
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("Invalid YouTube URL")
    
    async def get_transcript_from_api(self, video_id: str) -> str:
        """Get transcript using YouTube Transcript API"""
        if not YOUTUBE_TRANSCRIPT_AVAILABLE:
            raise Exception("YouTube Transcript API not available")
        
        try:
            # Try to get transcript in English first
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            
            # Combine all transcript segments
            full_transcript = ""
            for segment in transcript_list:
                full_transcript += segment['text'] + " "
            
            return full_transcript.strip()
        except Exception as e:
            raise Exception(f"Failed to get transcript from YouTube API: {str(e)}")
    
    async def get_transcript_from_audio(self, url: str) -> str:
        """Fallback: Extract audio and use Deepgram for speech-to-text"""
        if not (YT_DLP_AVAILABLE and DEEPGRAM_AVAILABLE and self.deepgram_client):
            raise Exception("Fallback dependencies not available")
        
        try:
            # Extract audio using yt-dlp
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, "audio.mp3")
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Read audio file
                with open(audio_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                
                # Deepgram for speech-to-text
                options = PrerecordedOptions(
                    model="nova-2",
                    language="en",
                    punctuate=True,
                    paragraphs=True,
                )
                
                response = self.deepgram_client.listen.rest.v("1").transcribe_file(
                    {"buffer": audio_data, "mimetype": "audio/mp3"}, options
                )
                
                transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
                return transcript
                
        except Exception as e:
            raise Exception(f"Failed to get transcript from audio: {str(e)}")
    
    async def get_transcript(self, url: str) -> str:
        """Get transcript from YouTube URL with fallback"""
        try:
            video_id = self.extract_video_id(url)
            
            # Try YouTube Transcript API first
            if YOUTUBE_TRANSCRIPT_AVAILABLE:
                try:
                    transcript = await self.get_transcript_from_api(video_id)
                    return transcript
                except Exception as e:
                    print(f"YouTube Transcript API failed: {str(e)}")
            
            # Fallback to audio extraction + Deepgram
            print("Falling back to audio extraction + Deepgram")
            transcript = await self.get_transcript_from_audio(url)
            return transcript
            
        except Exception as e:
            raise Exception(f"Failed to get transcript: {str(e)}") 