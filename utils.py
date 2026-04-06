"""Utility functions for file handling and CSV export"""
import io
import csv
import logging
from typing import List, Dict, Optional
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

class FileHandler:
    """Handle file uploads and extraction"""
    
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def extract_text_from_file(file) -> Optional[str]:
        """
        Extract text from uploaded file (txt or pdf)
        
        Args:
            file: FileStorage object from Flask
        
        Returns:
            Extracted text or None if failed
        """
        try:
            filename = file.filename
            
            if not FileHandler.allowed_file(filename):
                logger.error(f"File type not allowed: {filename}")
                return None
            
            # Check file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Seek back to start
            
            if file_size > FileHandler.MAX_FILE_SIZE:
                logger.error(f"File too large: {file_size} bytes")
                return None
            
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            if file_extension == 'txt':
                return FileHandler._extract_text_from_txt(file, filename)
            elif file_extension == 'pdf':
                return FileHandler._extract_text_from_pdf(file, filename)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting text from file {file.filename}: {str(e)}")
            return None
    
    @staticmethod
    def _extract_text_from_txt(file, filename: str) -> Optional[str]:
        """Extract text from TXT file"""
        try:
            content = file.read().decode('utf-8')
            logger.info(f"Successfully extracted text from {filename} ({len(content)} chars)")
            return content
        except UnicodeDecodeError:
            logger.error(f"Failed to decode {filename} as UTF-8")
            try:
                content = file.read().decode('latin-1')
                logger.info(f"Successfully extracted text from {filename} using latin-1 encoding")
                return content
            except Exception as e:
                logger.error(f"Failed to extract text from {filename}: {str(e)}")
                return None
        except Exception as e:
            logger.error(f"Error reading TXT file {filename}: {str(e)}")
            return None
    
    @staticmethod
    def _extract_text_from_pdf(file, filename: str) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            pdf_reader = PdfReader(file)
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1} of {filename}: {str(e)}")
                    continue
            
            if text.strip():
                logger.info(f"Successfully extracted text from {filename} ({len(text)} chars)")
                return text
            else:
                logger.warning(f"No text could be extracted from PDF {filename}")
                return None
                
        except Exception as e:
            logger.error(f"Error reading PDF file {filename}: {str(e)}")
            return None

class CSVExporter:
    """Export extracted job data to CSV format"""
    
    @staticmethod
    def export_to_csv(extractions: List[Dict]) -> Optional[bytes]:
        """
        Convert extracted job data to CSV bytes
        
        Args:
            extractions: List of extraction dictionaries
        
        Returns:
            CSV file bytes or None if failed
        """
        if not extractions:
            logger.warning("No extractions provided for CSV export")
            return None
        
        try:
            output = io.StringIO()
            fieldnames = ['role', 'skills', 'seniority', 'location', 'salary', 'source', 'created_at']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for extraction in extractions:
                row = {
                    'role': extraction.get('role', 'N/A'),
                    'skills': '; '.join(extraction.get('skills', [])) if extraction.get('skills') else 'N/A',
                    'seniority': extraction.get('seniority', 'N/A'),
                    'location': extraction.get('location', 'N/A'),
                    'salary': extraction.get('salary', 'N/A'),
                    'source': extraction.get('source', 'N/A'),
                    'created_at': extraction.get('created_at', 'N/A')
                }
                writer.writerow(row)
            
            csv_bytes = output.getvalue().encode('utf-8')
            logger.info(f"Successfully exported {len(extractions)} records to CSV")
            return csv_bytes
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return None
