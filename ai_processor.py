"""AI processing module for job description extraction using Google Gemini"""
import json
import logging
from typing import Dict, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class JDProcessor:
    """Process Job Descriptions and extract structured data using Google Gemini"""
    
    SYSTEM_PROMPT = """You are a precise job description parser. Extract and structure the following information from the provided job description:
1. role: Job title/position name
2. skills: List of required technical and soft skills
3. seniority: Level (Junior/Mid/Senior/Lead/Executive)
4. location: Work location (can be "Remote" if applicable)
5. salary: Salary range if mentioned, otherwise null

IMPORTANT: Always respond with VALID JSON only, no additional text. If a field is not mentioned in the JD, use null for that field.

Example output format:
{
  "role": "Senior Software Engineer",
  "skills": ["Python", "AWS", "Docker", "System Design"],
  "seniority": "Senior",
  "location": "San Francisco, CA",
  "salary": "$150,000 - $200,000"
}"""
    
    def __init__(self, api_key: str, model: str = 'gemini-1.5-flash'):
        """
        Initialize Google Gemini client
        
        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-2.5-flash)
        """
        if not api_key:
            raise ValueError("Google Gemini API key is required")
        
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
        self.model = model
        logger.info(f"JDProcessor initialized with model: {model}")
    
    def extract_json(self, jd_text: str) -> Optional[Dict]:
        """
        Send job description to Google Gemini and extract structured JSON
        
        Args:
            jd_text: Raw job description text
        
        Returns:
            Parsed JSON dictionary with extracted fields, or None if failed
        """
        if not jd_text or not jd_text.strip():
            logger.error("Empty job description provided")
            return None
        
        try:
            logger.info(f"Processing JD with {len(jd_text)} characters")
            
            prompt = f"""{self.SYSTEM_PROMPT}

Extract structured data from this job description:

{jd_text}

Respond with valid JSON only."""
            
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0,  # Deterministic output for consistency
                    max_output_tokens=500,
                )
            )
            
            # Extract and parse the response
            response_text = response.text.strip()
            
            # Try to extract JSON from response (in case there's extra text)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            logger.debug(f"Raw API response: {response_text}")
            
            extracted_data = json.loads(response_text)
            logger.info(f"Successfully extracted data for role: {extracted_data.get('role')}")
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from API response: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during extraction: {str(e)}")
            return None
    
    def validate_extraction(self, extracted_data: Dict) -> bool:
        """
        Validate that extracted data has required fields with valid data
        
        Args:
            extracted_data: Dictionary to validate
        
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['role', 'skills', 'seniority', 'location', 'salary']
        
        if not extracted_data:
            return False
        
        # Check if role exists and is not null
        if not extracted_data.get('role'):
            logger.warning("Validation failed: role field is empty")
            return False
        
        # Skills should be a list if present
        if 'skills' in extracted_data and extracted_data['skills'] is not None:
            if not isinstance(extracted_data['skills'], list):
                logger.warning("Validation failed: skills should be a list")
                return False
        
        return True
    
    def process_jd(self, jd_text: str) -> Optional[Dict]:
        """
        Complete pipeline: extract JSON from JD and validate
        
        Args:
            jd_text: Raw job description text
        
        Returns:
            Validated extracted data or None if failed
        """
        extracted = self.extract_json(jd_text)
        
        if extracted and self.validate_extraction(extracted):
            return extracted
        else:
            logger.warning("Extracted data failed validation")
            return None

class AIPipeline:
    """Main AI pipeline for batch processing"""
    
    def __init__(self, api_key: str):
        """Initialize the AI pipeline"""
        self.processor = JDProcessor(api_key)
    
    def process_multiple(self, jd_texts: list) -> Dict:
        """
        Process multiple job descriptions
        
        Args:
            jd_texts: List of JD text strings
        
        Returns:
            Dictionary with results and summary
        """
        results = []
        successful = 0
        failed = 0
        
        for i, jd_text in enumerate(jd_texts):
            logger.info(f"Processing JD {i+1}/{len(jd_texts)}")
            extracted = self.processor.process_jd(jd_text)
            
            if extracted:
                results.append({
                    'status': 'success',
                    'data': extracted,
                    'raw_jd': jd_text
                })
                successful += 1
            else:
                results.append({
                    'status': 'failed',
                    'error': 'Failed to extract valid JSON from JD',
                    'raw_jd': jd_text
                })
                failed += 1
        
        return {
            'total': len(jd_texts),
            'successful': successful,
            'failed': failed,
            'results': results
        }
