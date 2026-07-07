# File Storage System

Upload, list, search, sort, and download files — backed by AWS S3.

## Project Structure

```
/
  main.py          # Python backend (FastAPI + S3 + algorithms, all in one file)
  index.html       # Frontend UI
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## Tech Stack

- Python 3 · FastAPI · Boto3 · python-dotenv
- AWS S3 (or local MinIO)
- Vanilla HTML / CSS / JS

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your AWS credentials:

```env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name
# S3_ENDPOINT_URL=http://localhost:9000  ← only for local MinIO
```

### 3. Run the backend

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open the frontend

Open `index.html` in your browser.

## API

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Health check |
| POST | `/upload` | Upload a file |
| GET | `/files` | List files (`sort_by`, `order`) |
| GET | `/files/search?query=x` | Search by name |
| DELETE | `/files/{filename}` | Delete a file |
| GET | `/files/{filename}/download` | Get temp download link |

## Algorithms (in main.py)

- **Merge Sort** `O(n log n)` — sorts files by name / size / date
- **Linear Search** `O(n)` — searches file names by partial match
