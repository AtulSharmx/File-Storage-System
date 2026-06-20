"""
File Storage System - main API
"""

import uuid
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv() 

from algorithms.sorting import merge_sort
from algorithms.searching import linear_search
import s3_utils

app = FastAPI(title="File Storage System")

# SECURITY FIX: Only allow your trusted frontend to talk to this backend.
# If you buy a real domain name later (like mywebsite.com), put it in this list.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:5500", 
        "http://127.0.0.1:8000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "File Storage System API is running"}


# PERFORMANCE FIX: Removed "async" so slow uploads do not freeze the whole server.
@app.post("/upload")
def upload_file(file: UploadFile):
    # OVERWRITE FIX: Add a random 8-character ID to the start of the file name.
    # Example: "resume.pdf" becomes "a1b2c3d4_resume.pdf"
    random_id = str(uuid.uuid4())[:8]
    safe_filename = f"{random_id}_{file.filename}"
    
    s3_utils.upload_file(file.file, safe_filename)
    return {"message": f"{file.filename} uploaded successfully!"}


@app.get("/files")
def get_files(sort_by: str = "name", order: str = "asc"):
    files = s3_utils.list_files()

    key_map = {
        "name": lambda f: f["name"].lower(),
        "size": lambda f: f["size"],
        "date": lambda f: f["last_modified"],
    }
    key_func = key_map.get(sort_by, key_map["name"])

    sorted_files = merge_sort(files, key=key_func, reverse=(order == "desc"))
    return {"files": sorted_files}


@app.get("/files/search")
def search_files(query: str):
    files = s3_utils.list_files()
    results = linear_search(files, query, key=lambda f: f["name"])
    return {"results": results}


@app.delete("/files/{filename}")
def delete_file(filename: str):
    try:
        s3_utils.delete_file(filename)
    except Exception:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": f"{filename} deleted"}


@app.get("/files/{filename}/download")
def download_file(filename: str):
    url = s3_utils.get_download_url(filename)
    return {"url": url}