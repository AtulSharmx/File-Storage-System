"""
Run this with: python diagnose.py

Checks, step by step, why AWS might be rejecting your credentials.
Does NOT print your full access key or secret - only enough to sanity
check them (first few characters + length), so it's safe to share the
output with anyone if needed.
"""

import os
from dotenv import load_dotenv

print("Step 1: Looking for a .env file in this folder...")
env_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(env_path):
    print(f"  Found .env at: {env_path}")
else:
    print(f"  NO .env file found at: {env_path}")
    print("  --> This is likely the problem. Make sure the file is named")
    print("      exactly '.env' (not '.env.txt'). In Notepad, when saving,")
    print("      set 'Save as type' to 'All Files' and type the name as")
    print('      ".env" including the dot, with quotes, to avoid Windows')
    print("      silently adding .txt at the end.")

load_dotenv()

print()
print("Step 2: Checking what got loaded into the environment...")

access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
region = os.environ.get("AWS_REGION", "")
bucket = os.environ.get("S3_BUCKET_NAME", "")
endpoint = os.environ.get("S3_ENDPOINT_URL", "")

def describe(name, value, expect_prefix=None):
    if not value:
        print(f"  {name}: EMPTY / not set")
    else:
        preview = value[:4] + "..." if len(value) > 4 else value
        print(f"  {name}: starts with '{preview}', length {len(value)}")
        if expect_prefix and not value.startswith(expect_prefix):
            print(f"    --> Warning: real AWS access keys usually start with '{expect_prefix}'")
        if value != value.strip():
            print(f"    --> Warning: has leading/trailing spaces - remove them in .env")
        if value.startswith('"') or value.endswith('"') or value.startswith("'"):
            print(f"    --> Warning: looks like it has quote marks included - remove them")

describe("AWS_ACCESS_KEY_ID", access_key, expect_prefix="AKIA")
describe("AWS_SECRET_ACCESS_KEY", secret_key)
print(f"  AWS_REGION: {region or '(empty)'}")
print(f"  S3_BUCKET_NAME: {bucket or '(empty)'}")
print(f"  S3_ENDPOINT_URL: {endpoint or '(empty - good, means using real AWS not MinIO)'}")

print()
print("Step 3: Asking AWS directly 'do you recognize these credentials?'")
print("        (this is the safest possible AWS call - it doesn't touch")
print("         any bucket or data, just checks identity)")
try:
    import boto3
    sts = boto3.client("sts", region_name=region or "ap-south-1")
    identity = sts.get_caller_identity()
    print("  SUCCESS - AWS recognizes these credentials.")
    print(f"  Account: {identity.get('Account')}")
    print(f"  Identity ARN: {identity.get('Arn')}")
    print()
    print("  Since this worked, the access key itself is fine. If upload")
    print("  still fails, the problem is something else (bucket name,")
    print("  bucket region, or permissions) - not the credentials.")
except Exception as e:
    print(f"  FAILED: {e}")
    print()
    print("  This confirms AWS itself does not recognize this access key,")
    print("  independent of any bucket or upload code. This means the key")
    print("  in your .env file is either mistyped, incomplete, or belongs")
    print("  to a key that's been deleted in the AWS console.")
