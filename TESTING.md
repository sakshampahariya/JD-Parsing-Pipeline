# Testing Guide - Job Description Pipeline

This guide will help you test the Job Description Pipeline application.

## Prerequisites

Ensure you have completed the setup in README.md:
- Python environment configured
- Dependencies installed
- `.env` file with API keys configured
- Flask app running on `http://localhost:5000`

## Manual Testing via Web UI

### Test 1: Text Input Processing

1. **Open the application**: Navigate to `http://localhost:5000`
2. **Enter sample text**: Copy and paste the content from `sample_jd.txt` into the textarea
3. **Click Process**: Submit the form
4. **Verify Results**:
   - Should show "1 successful" in the stats
   - Table should display extracted data
   - CSV export button should appear

**Expected Output:**
```json
{
  "role": "Senior Software Engineer - Full Stack",
  "skills": ["Python", "Node.js", "React.js", "PostgreSQL", "Docker", "Kubernetes", "AWS"],
  "seniority": "Senior",
  "location": "San Francisco, CA",
  "salary": "$140,000 - $200,000"
}
```

### Test 2: File Upload (Single File)

1. **Open the application**: Navigate to `http://localhost:5000`
2. **Upload file**: Drag and drop `sample_jd.txt` or click to select
3. **Verify file appears** in the file list
4. **Click Process**: Submit the form
5. **Verify Results**: Same as Test 1

### Test 3: Multiple File Upload

1. **Create multiple test files** with different JD content
2. **Upload multiple files**: Select all test files
3. **Click Process**: Submit the form
4. **Verify Results**:
   - Should show correct total count
   - All successful extractions displayed in table
   - Each file source listed

### Test 4: CSV Export

1. **Process some JDs** (use Test 1 or 2)
2. **Click Export as CSV**: Download should start
3. **Verify CSV contents**:
   - Headers: Status, Role, Skills, Seniority, Location, Salary
   - Data matches displayed results
   - Skills are comma-separated

### Test 5: Error Handling

#### Test 5a: No Input
1. **Leave both textarea and file upload empty**
2. **Click Process**: Should show error "Please provide either text input or upload files"

#### Test 5b: Invalid File
1. **Try uploading a .doc file**: Should be rejected
2. **Try uploading a > 16MB file**: Should be rejected
3. **Try uploading a corrupted PDF**: Should fail gracefully with message

#### Test 5c: Empty File
1. **Create an empty text file**
2. **Upload and process**: Should show "failed to process" result

### Test 6: Mixed Input
1. **Paste text in textarea**
2. **Also upload files**
3. **Click Process**: Should process both text and files
4. **Verify**: All results shown in table with correct sources

## API Testing with cURL or Postman

### Test Endpoint: POST /process with Text

```bash
curl -X POST http://localhost:5000/process \
  -d "jd_text=Senior Software Engineer with 5+ years in Python" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### Test Endpoint: POST /process with File

```bash
curl -X POST http://localhost:5000/process \
  -F "files=@sample_jd.txt"
```

### Test Endpoint: POST /process with Both

```bash
curl -X POST http://localhost:5000/process \
  -F "jd_text=Senior Engineer" \
  -F "files=@sample_jd.txt"
```

### Test Endpoint: GET /health

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "ai_processor": "ready",
  "database": "connected"
}
```

## Database Testing

### Verify Supabase Connection

1. **Check health endpoint**:
   ```bash
   curl http://localhost:5000/health
   ```
   Should show `"database": "connected"`

2. **Verify data insertion**:
   - Process a JD
   - Check Supabase dashboard
   - Navigate to `job_extractions` table
   - Should see newly inserted row

3. **Check table structure**:
   - Verify all columns exist: role, skills, seniority, location, salary, raw_jd, source, created_at

### SQL Queries to Run

Check record count:
```sql
SELECT COUNT(*) as total_records FROM job_extractions;
```

View recent extractions:
```sql
SELECT * FROM recent_extractions LIMIT 5;
```

Get statistics:
```sql
SELECT * FROM extraction_stats;
```

Get skills breakdown:
```sql
SELECT * FROM get_skills_breakdown() LIMIT 10;
```

## Performance Testing

### Test Large Batch Processing

1. **Create 5-10 test JD files**
2. **Upload all at once**
3. **Record processing time**:
   - Should process ~2-3 files per minute depending on API rate limits
   - Each API call takes ~2-5 seconds

### Monitor Logs

While processing, check Flask logs for:
- Successful processing messages
- Any errors or warnings
- Database insertion confirmations

## Security Testing

### Test 1: API Key Validation
1. **Modify .env** to use invalid OpenAI key
2. **Try to process**: Should get "AI processor not available" error
3. **Restore correct key**

### Test 2: File Size Limit
1. **Try uploading file > 16MB**: Should get 413 error
2. **Check error message**: Should mention file size limit

### Test 3: File Type Validation
1. **Try various file types**: .doc, .docx, .xls, .zip
2. **All should be rejected**: Only PDF and TXT allowed

## Browser Compatibility Testing

Test on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (if available)

Verify:
- Form displays correctly
- File upload works
- Results table responsive
- CSV download works
- Mobile view is proper (Bootstrap responsive)

## Stress Testing

### Monitor API Quotas

OpenAI GPT-4o-mini pricing is per 1M tokens:
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

**Estimate for sample JD:**
- ~500-1000 input tokens
- ~100-150 output tokens
- Cost per extraction: ~$0.0001-0.0002

### Track Costs

Monitor your OpenAI account:
1. Go to https://platform.openai.com/account/billing/overview
2. Check usage under "Usage"
3. Set limits in account settings if needed

## Logging and Debugging

### Enable Debug Mode

In `.env`:
```env
DEBUG=True
```

This provides:
- Detailed error pages
- Automatic reload on code changes
- Full stack traces

### Check Logs

Flask logs appear in terminal where app runs:
```
2024-04-06 10:30:45,123 - app - INFO - Processing test JD
2024-04-06 10:30:48,456 - ai_processor - INFO - Successfully extracted data for role: Senior Engineer
2024-04-06 10:30:49,789 - database - INFO - Successfully inserted record for role: Senior Engineer
```

### Common Issues and Fixes

| Issue | Cause | Solution |
|-------|-------|----------|
| "AI processor not available" | Invalid OPENAI_API_KEY | Check .env file and API key validity |
| "Table not found" | Supabase table not created | Run SQL from supabase_setup.sql |
| "Empty extraction" | PDF text not extractable | Try with TXT or a different PDF |
| "File rejected" | Invalid file type | Use only PDF or TXT files |
| "Connection refused" | Flask app not running | Run `python app.py` |
| "CORS error" | Frontend trying different origin | Not applicable for same-origin requests |

## Continuous Testing

### Set Up Local Testing Script

Create `test.py`:
```python
import requests
import json

def test_health():
    response = requests.get('http://localhost:5000/health')
    print(f"Health: {response.json()}")
    assert response.status_code == 200

def test_process_text():
    data = {'jd_text': 'Senior Python Developer with 5+ years experience'}
    response = requests.post('http://localhost:5000/process', data=data)
    print(f"Process: {response.json()}")
    assert response.status_code == 200

if __name__ == '__main__':
    test_health()
    test_process_text()
    print("All tests passed!")
```

Run with:
```bash
pip install requests
python test.py
```

## Test Completion Checklist

- [ ] Text input processing works
- [ ] File upload (PDF and TXT) works
- [ ] Batch processing with multiple files works
- [ ] CSV export generates correctly
- [ ] Error handling displays user-friendly messages
- [ ] Database stores extractions
- [ ] CSV export matches displayed results
- [ ] Mobile view is responsive
- [ ] All file types are properly validated
- [ ] API endpoints return correct format
- [ ] Health check shows all systems OK
- [ ] Processing time is acceptable
- [ ] No sensitive data in logs

## Support

If tests fail, check:
1. `.env` file has all required keys
2. Virtual environment is activated
3. Flask app is running
4. Supabase table exists
5. OpenAI API has quota remaining
6. Browser console for JavaScript errors

For detailed troubleshooting, see README.md Troubleshooting section.
