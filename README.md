# 🗄️ File Storage System

A lightweight file storage web app built with **FastAPI** (Python) and **AWS S3**. Upload, search, sort, download and delete files — all from a clean browser UI.

🌐 **Live Demo:** [file-storage-with-aws.vercel.app](https://file-storage-with-aws.vercel.app/)

---

## ✨ Features

- ☁️ Upload files directly to AWS S3
- 📋 List all uploaded files with size and upload date
- 🔃 Sort files by name, size, or date
- 🔍 Search for specific files
- ⬇️ Download and 🗑️ delete files

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python + FastAPI |
| Storage | AWS S3 |
| Frontend | HTML / CSS / JavaScript |
| Deployment | Vercel |

---

## 🚀 Run it locally

### 1. Install requirements

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the same folder as `main.py` and paste this inside:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name
```

> ⚠️ **Never upload your `.env` file to GitHub!** It is already in `.gitignore` but double check.

### 3. Start the backend

```bash
uvicorn main:app --reload
```

Backend runs at → `http://127.0.0.1:8000`

### 4. Open the frontend

Just double-click `index.html` to open it in your browser. That is it!

---

## 📁 Project Structure

```
File-Storage-System/
│
├── main.py           # FastAPI backend
├── index.html        # Frontend UI
├── requirements.txt  # Python dependencies
├── .gitignore
└── .env              # (not pushed to GitHub)
```

---

## 👤 Author

**AtulSharmx** — BCA Student | Building projects with Python and Cloud ☁️
