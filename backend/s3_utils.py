"""
All the AWS S3 specific code lives here.
"""

import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL") or None

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL,
)


def upload_file(file_obj, filename: str):
    """Uploads a file-like object to the S3 bucket under the given name."""
    s3_client.upload_fileobj(file_obj, BUCKET_NAME, filename)


def list_files():
    """
    Returns metadata (name, size, last modified) for EVERY file in the bucket.
    Uses a paginator to safely bypass the AWS 1,000 file limit.
    """
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME)
    
    files = []

    for page in pages:
        for obj in page.get("Contents", []):
            files.append({
                "name": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
            })

    return files


def delete_file(filename: str):
    """Deletes a single file from the bucket."""
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)


def get_download_url(filename: str, expires_in: int = 3600):
    """
    Generates a temporary link the file can be downloaded from,
    valid for `expires_in` seconds (default 1 hour).
    """
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": filename},
        ExpiresIn=expires_in,
    )