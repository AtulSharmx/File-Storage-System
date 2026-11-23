import os
import uuid
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "ap-south-1"))
BUCKET = os.getenv("S3_BUCKET_NAME")

# The API is unauthenticated, so an uncapped upload endpoint is an open invitation
# to fill the bucket at the account owner's expense.
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024


def require_bucket():
    if not BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME is not set")
    return BUCKET

def merge_sort(items, key=lambda x: x, reverse=False):
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid], key, reverse)
    right = merge_sort(items[mid:], key, reverse)
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if not reverse:
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if key(left[i]) >= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    return result + left[i:] + right[j:]

def linear_search(items, query, key=lambda x: x):
    result = []
    for item in items:
        if query.lower() in str(key(item)).lower():
            result.append(item)
    return result

def list_files():
    bucket = require_bucket()
    try:
        pages = s3.get_paginator("list_objects_v2").paginate(Bucket=bucket)
        files = []
        for page in pages:
            for obj in page.get("Contents", []):
                files.append({
                    "name": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"].isoformat()
                })
        return files
    except (BotoCoreError, ClientError) as exc:
        # Returning [] here made a missing permission or a bad bucket name look
        # exactly like an empty bucket.
        raise HTTPException(status_code=502, detail=f"Could not list the bucket: {exc}") from exc

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/upload")
def upload(file: UploadFile):
    bucket = require_bucket()

    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"Files are capped at {MAX_UPLOAD_MB} MB")

    # basename keeps a crafted filename from steering the S3 key into a folder.
    original = os.path.basename(file.filename or "file")
    name = str(uuid.uuid4())[:8] + "_" + original
    try:
        s3.upload_fileobj(file.file, bucket, name)
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(status_code=502, detail=f"Upload failed: {exc}") from exc
    return {"message": "uploaded", "name": name}

@app.get("/files")
def get_files(sort_by: str = "name", order: str = "asc"):
    files = list_files()
    if sort_by == "name":
        files = merge_sort(files, key=lambda f: f["name"].lower(), reverse=(order == "desc"))
    elif sort_by == "size":
        files = merge_sort(files, key=lambda f: f["size"], reverse=(order == "desc"))
    elif sort_by == "date":
        files = merge_sort(files, key=lambda f: f["last_modified"], reverse=(order == "desc"))
    return {"files": files}

@app.get("/files/search")
def search(query: str):
    files = list_files()
    results = linear_search(files, query, key=lambda f: f["name"])
    return {"results": results}

@app.delete("/files/{filename}")
def delete(filename: str):
    bucket = require_bucket()
    # delete_object reports success whether or not the key was there, so the old
    # 404 could never fire. Check first, then delete.
    try:
        s3.head_object(Bucket=bucket, Key=filename)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            raise HTTPException(status_code=404, detail="Not found") from exc
        raise HTTPException(status_code=502, detail=f"Could not reach the bucket: {exc}") from exc
    except BotoCoreError as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach the bucket: {exc}") from exc

    s3.delete_object(Bucket=bucket, Key=filename)
    return {"message": "deleted"}

@app.get("/files/{filename}/download")
def download(filename: str):
    bucket = require_bucket()
    url = s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": filename}, ExpiresIn=3600)
    return {"url": url}
