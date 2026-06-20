"""
One-time helper: creates the S3 bucket if it doesn't already exist.

Run this once after setting up your .env file:
    python setup_bucket.py

Works the same whether you're pointed at MinIO (local) or real AWS S3 -
it just calls create_bucket() and ignores the error if the bucket is
already there.
"""

from dotenv import load_dotenv
load_dotenv()

import os
from botocore.exceptions import ClientError
import s3_utils

bucket = s3_utils.BUCKET_NAME

try:
    s3_utils.s3_client.create_bucket(Bucket=bucket)
    print(f"Bucket '{bucket}' created.")
except ClientError as e:
    code = e.response.get("Error", {}).get("Code", "")
    if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
        print(f"Bucket '{bucket}' already exists, nothing to do.")
    else:
        print(f"Could not create bucket: {e}")
