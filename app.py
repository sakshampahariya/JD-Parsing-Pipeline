"""Flask application for Job Description Pipeline"""
import os
import io
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from config import DevelopmentConfig, ProductionConfig
from database import DatabaseManager
from ai_processor import JDProcessor
from utils import FileHandler, CSVExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('ENVIRONMENT', 'development')
app.config.from_object(DevelopmentConfig if env == 'development' else ProductionConfig)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
try:
    ai_processor = JDProcessor(api_key=app.config['GEMINI_API_KEY'])
    logger.info("AI processor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI processor: {str(e)}")
    ai_processor = None

try:
    db_manager = DatabaseManager(
        url=app.config['SUPABASE_URL'],
        key=app.config['SUPABASE_KEY'],
        table_name=app.config['SUPABASE_TABLE']
    )
    if db_manager.is_connected():
        logger.info("Database connection successful")
    else:
        logger.warning("Database connection failed - storing will not work")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    db_manager = None

# Routes

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_jd():
    """
    Process job descriptions from text input or file uploads
    
    Expected POST parameters:
    - jd_text: Raw text input (optional)
    - files: Uploaded files (optional)
    
    Returns:
        JSON response with processed data
    """
    try:
        # Validate that AI processor is available
        if not ai_processor:
            return jsonify({
                'success': False,
                'error': 'AI processor is not available. Check your Google Gemini API key.'
            }), 503
        
        jd_texts = []
        
        # Get text from textarea input
        jd_text = request.form.get('jd_text', '').strip()
        if jd_text:
            jd_texts.append({
                'text': jd_text,
                'source': 'manual_input'
            })
            logger.info("Received text input for processing")
        
        # Get text from file uploads
        if 'files' in request.files:
            files = request.files.getlist('files')
            
            for file in files:
                if file and file.filename:
                    if not FileHandler.allowed_file(file.filename):
                        logger.warning(f"File rejected: {file.filename} - invalid extension")
                        continue
                    
                    extracted_text = FileHandler.extract_text_from_file(file)
                    if extracted_text:
                        jd_texts.append({
                            'text': extracted_text,
                            'source': secure_filename(file.filename)
                        })
                        logger.info(f"Extracted text from file: {file.filename}")
                    else:
                        logger.error(f"Failed to extract text from file: {file.filename}")
        
        # Validate that we have content to process
        if not jd_texts:
            return jsonify({
                'success': False,
                'error': 'Please provide either text input or upload files'
            }), 400
        
        # Process all job descriptions
        results = []
        db_records = []
        
        for i, item in enumerate(jd_texts):
            logger.info(f"Processing JD {i+1}/{len(jd_texts)}")
            
            extracted_data = ai_processor.process_jd(item['text'])
            
            if extracted_data:
                result = {
                    'status': 'success',
                    'data': extracted_data,
                    'source': item['source']
                }
                results.append(result)
                
                # Prepare database record
                db_record = {
                    'role': extracted_data.get('role'),
                    'skills': extracted_data.get('skills'),
                    'seniority': extracted_data.get('seniority'),
                    'location': extracted_data.get('location'),
                    'salary': extracted_data.get('salary'),
                    'raw_jd': item['text'],
                    'source': item['source'],
                    'processed_at': datetime.utcnow().isoformat()
                }
                db_records.append(db_record)
            else:
                results.append({
                    'status': 'failed',
                    'error': 'Failed to extract valid JSON from job description',
                    'source': item['source']
                })
                logger.error(f"Failed to process JD from source: {item['source']}")
        
        # Store successful extractions in database
        if db_records and db_manager:
            try:
                inserted_count = db_manager.insert_many(db_records)
                logger.info(f"Stored {inserted_count}/{len(db_records)} records in database")
            except Exception as e:
                logger.error(f"Failed to store records in database: {str(e)}")
        
        # Count successful and failed extractions
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = sum(1 for r in results if r['status'] == 'failed')
        
        return jsonify({
            'success': True,
            'total': len(results),
            'successful': successful,
            'failed': failed,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in /process route: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/export', methods=['POST'])
def export_csv():
    """
    Export extraction results to CSV
    
    Expected POST parameters:
    - results: JSON string containing extraction results
    
    Returns:
        CSV file for download
    """
    try:
        import json
        
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No results to export'
            }), 400
        
        # Filter only successful results and extract the data
        successful_results = []
        for result in results:
            if result.get('status') == 'success':
                successful_results.append(result.get('data', {}))
        
        if not successful_results:
            return jsonify({
                'success': False,
                'error': 'No successful extractions to export'
            }), 400
        
        # Generate CSV
        csv_bytes = CSVExporter.export_to_csv(successful_results)
        
        if not csv_bytes:
            return jsonify({
                'success': False,
                'error': 'Failed to generate CSV'
            }), 500
        
        logger.info(f"Exporting {len(successful_results)} records to CSV")
        
        return send_file(
            io.BytesIO(csv_bytes),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'job_extractions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        logger.error(f"Error in /export route: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Export failed: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_processor': 'ready' if ai_processor else 'unavailable',
        'database': 'connected' if db_manager and db_manager.is_connected() else 'disconnected'
    }), 200

# Error handlers

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
