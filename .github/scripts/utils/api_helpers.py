"""
API Helper Utilities for AI Creative Workflow
"""
import os
import time
import json
import logging
from typing import Dict, List, Optional, Any
from functools import wraps
import anthropic
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retry_with_exponential_backoff(max_retries: int = 3, initial_delay: float = 1.0):
    """Decorator for retrying API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(f"All {max_retries} attempts failed.")
            
            raise last_exception
        return wrapper
    return decorator


class AnthropicClient:
    """Wrapper for Anthropic Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    @retry_with_exponential_backoff()
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """Generate text using Claude API"""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            kwargs = {
                "model": "claude-3-5-sonnet-20241022",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error in Anthropic API call: {str(e)}")
            raise
    
    def analyze_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        """Generate and parse JSON response"""
        json_prompt = f"{prompt}\n\nPlease respond with valid JSON only, no other text."
        response = self.generate(json_prompt, system_prompt, temperature=0.3)
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # If no JSON found, try parsing the entire response
                return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response[:500]}")
            raise


class GeminiClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    @retry_with_exponential_backoff()
    def search_web(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """Perform web search using Gemini"""
        try:
            prompt = f"""
            Please search the web for information about: {query}
            
            Return the top {num_results} most relevant results in JSON format:
            {{
                "results": [
                    {{
                        "title": "Result title",
                        "url": "URL",
                        "snippet": "Brief description"
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('results', [])
            return []
        except Exception as e:
            logger.error(f"Error in Gemini web search: {str(e)}")
            return []
    
    @retry_with_exponential_backoff()
    def summarize_content(self, content: str, max_length: int = 500) -> str:
        """Summarize content using Gemini"""
        try:
            prompt = f"""
            Please summarize the following content in approximately {max_length} characters:
            
            {content}
            
            Focus on key points and actionable insights.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error in Gemini summarization: {str(e)}")
            raise


class GoogleSheetsClient:
    """Wrapper for Google Sheets API"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        else:
            # Use API key as fallback
            api_key = os.environ.get('GOOGLE_SHEETS_API_KEY')
            if api_key:
                self.service = build('sheets', 'v4', developerKey=api_key)
            else:
                raise ValueError("Google Sheets credentials not provided")
    
    @retry_with_exponential_backoff()
    def get_sheet_data(self, spreadsheet_id: str, range_name: str) -> List[List[str]]:
        """Fetch data from Google Sheets"""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except Exception as e:
            logger.error(f"Error fetching Google Sheets data: {str(e)}")
            raise
    
    def get_sheet_as_dict(self, spreadsheet_id: str, range_name: str) -> List[Dict[str, Any]]:
        """Fetch sheet data and convert to list of dictionaries"""
        data = self.get_sheet_data(spreadsheet_id, range_name)
        if not data:
            return []
        
        headers = data[0]
        return [dict(zip(headers, row)) for row in data[1:]]


def save_json(data: Any, filepath: str, ensure_ascii: bool = False) -> None:
    """Save data as JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=2)


def load_json(filepath: str) -> Any:
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_markdown(content: str, filepath: str) -> None:
    """Save content as Markdown file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def load_markdown(filepath: str) -> str:
    """Load Markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()