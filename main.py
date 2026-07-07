import os
import uuid
import boto3
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    try:
        pages = s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET)
        files = []
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    files.append({
                        "name": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat()
                    })
        return files
    except Exception as e:
        return []

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/upload")
def upload(file: UploadFile):
    name = str(uuid.uuid4())[:8] + "_" + file.filename
    s3.upload_fileobj(file.file, BUCKET, name)
    return {"message": "uploaded"}

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
    try:
        s3.delete_object(Bucket=BUCKET, Key=filename)
        return {"message": "deleted"}
    except:
        raise HTTPException(status_code=404, detail="Not found")

@app.get("/files/{filename}/download")
def download(filename: str):
    url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": filename}, ExpiresIn=3600)
    return {"url": url}
