# JD-Parsing-Pipeline

An AI-powered pipeline that converts unstructured job descriptions into clean, structured JSON — extracting role, skills, seniority, location, and salary automatically using Google Gemini.

## What It Does

Recruiters and HR tools often deal with messy, inconsistent job descriptions. This pipeline takes raw JD text (or uploaded PDF/TXT files), runs it through an LLM extraction layer, stores the structured output in a database, and lets you export it as CSV — all through a clean web interface.

## Features

- Paste text or upload PDF/TXT files for batch processing
- Extracts: job role, required skills, seniority level, location, salary
- Stores results in Supabase (PostgreSQL) for persistence
- Export all results as CSV with one click
- REST API with `/process`, `/export`, and `/health` endpoints
- Comprehensive error handling for encoding issues, large files, and API failures

## Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Backend    | Flask (Python)                          |
| AI Model   | Google Gemini (via API)                 |
| Database   | Supabase (PostgreSQL)                   |
| PDF Parser | PyPDF2                                  |
| Frontend   | Bootstrap 5, Vanilla JS                 |

## Project Structure

```
JD-Parsing-Pipeline/
├── app.py              # Flask routes and app entry point
├── ai_processor.py     # Gemini API integration and extraction logic
├── database.py         # Supabase CRUD operations
├── config.py           # Environment and config management
├── utils.py            # File handling, text extraction, CSV export
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt
└── supabase_setup.sql  # DB schema
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/sakshampahariya/JD-Parsing-Pipeline
cd JD-Parsing-Pipeline
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set environment variables**

Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
SECRET_KEY=your_secret_key
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

**5. Set up the database**

Run `supabase_setup.sql` in your Supabase SQL editor to create the `job_extractions` table.

**6. Run the app**
```bash
python app.py
```

Visit `http://localhost:5000`

## API

### `POST /process`
Submit a job description (text or file upload).

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "status": "success",
      "data": {
        "role": "Senior Software Engineer",
        "skills": ["Python", "AWS", "Docker"],
        "seniority": "Senior",
        "location": "Remote",
        "salary": "$150,000 - $200,000"
      }
    }
  ]
}
```

### `POST /export`
Returns a CSV of all extraction results.

### `GET /health`
Returns service status and DB connection state.

## Example Input

```
We are seeking a Senior Backend Engineer with 5+ years of experience.
Required: Python, FastAPI, PostgreSQL, Docker, AWS.
Location: Remote / Bangalore. Salary: ₹30–45 LPA.
```

## Example Output

```json
{
  "role": "Senior Backend Engineer",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
  "seniority": "Senior",
  "location": "Remote / Bangalore",
  "salary": "₹30–45 LPA"
}
```

## License

MIT