import os
from openai import OpenAI
from typing import List
from models.response_models import NewsArticle

class NewsGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.openai_api_key)
    
    async def generate_articles(self, transcript: str) -> List[NewsArticle]:
        """Generate 3 news articles from podcast transcript"""
        try:
            # Create the prompt for OpenAI
            prompt = f"""
            You are a journalist. Analyze the following podcast transcript and generate 3 distinct news articles based on the most relevant, controversial, or high-stakes points discussed.

            Each article should:
            - Be approximately 200 words
            - Focus on a different key insight or topic from the podcast
            - Include at least one direct quote from the podcast
            - Have a compelling headline
            - Be written in a professional news style

            Format your response as a JSON array with this structure:
            [
                {{
                    "title": "Article Title",
                    "content": "Article content with quote...",
                    "key_quote": "Direct quote from podcast"
                }},
                ...
            ]

            Podcast Transcript:
            {transcript}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini-2025-04-14",  
                messages=[
                    {"role": "system", "content": "You are a professional journalist who writes compelling news articles based on podcast content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=28000,
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON array in the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                articles_data = json.loads(json_str)
            else:
                # Fallback parsing if JSON is not properly formatted
                articles_data = self._parse_fallback_response(content)
            
            # Convert to NewsArticle objects
            articles = []
            for i, article_data in enumerate(articles_data):
                article = NewsArticle(
                    title=article_data.get("title", f"Tech Insight #{i+1}"),
                    content=article_data.get("content", ""),
                    key_quote=article_data.get("key_quote", "")
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            raise Exception(f"Failed to generate news articles: {str(e)}")
    
    def _parse_fallback_response(self, content: str) -> List[dict]:
        """Fallback method to parse response if JSON extraction fails"""
        # Simple fallback - split by likely separators and create basic articles
        articles = []
        
        # Split content into sections
        sections = content.split('\n\n')
        current_article = {}
        
        for section in sections:
            if section.strip():
                if any(keyword in section.lower() for keyword in ['title:', 'headline:']):
                    if current_article:
                        articles.append(current_article)
                    current_article = {"title": section.replace('Title:', '').replace('Headline:', '').strip()}
                elif 'content:' in section.lower():
                    current_article["content"] = section.replace('Content:', '').strip()
                elif 'quote:' in section.lower():
                    current_article["key_quote"] = section.replace('Quote:', '').strip()
                else:
                    # If we have a title but no content yet, treat this as content
                    if current_article.get("title") and not current_article.get("content"):
                        current_article["content"] = section.strip()
        
        if current_article:
            articles.append(current_article)
        
        # Ensure we have at least 3 articles
        while len(articles) < 3:
            articles.append({
                "title": f"Tech Insight #{len(articles) + 1}",
                "content": "Unable to generate this article due to parsing issues. Please try again.",
                "key_quote": ""
            })
        
        return articles[:3]  # Return only first 3 articles 