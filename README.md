# File storage system

Upload files to AWS S3 from the browser, then list, sort, search, download and delete
them. FastAPI on the backend, one HTML page on the front.

[Live demo](https://file-storage-with-aws.vercel.app/)

## Why the sorting and searching are written by hand

The sort and the search in `main.py` are implemented from scratch rather than calling
`sorted()` or a list comprehension, because that was the point of the exercise. Python
would do both in one line; writing them out is what the assignment was about.

`merge_sort` is the standard divide and conquer: split the list in half, sort each half
recursively, then walk the two sorted halves together taking the smaller head each time.
It takes a `key` function and a `reverse` flag so the same function handles sorting by
name, by size and by date without three copies of it.

`linear_search` walks the whole list and keeps anything whose name contains the query,
case-insensitively. That is O(n) every time, which is fine here: S3 returns a few hundred
keys and the network round trip costs far more than the scan. A real search over a large
bucket would need the index somewhere else, not a loop in the request handler.

## API

| Method | Path | What it does |
|---|---|---|
| `GET` | `/` | Serves the page |
| `POST` | `/upload` | Uploads a file to the bucket |
| `GET` | `/files?sort_by=&order=` | Lists files, sorted by `name`, `size` or `date` |
| `GET` | `/files/search?query=` | Filters by filename |
| `DELETE` | `/files/{filename}` | Removes it from the bucket |
| `GET` | `/files/{filename}/download` | Returns a presigned URL, valid one hour |

Uploads get an eight character uuid prefixed to the filename, so two people uploading
`notes.pdf` do not overwrite each other.

Downloads hand back a presigned S3 URL rather than streaming the file through the server.
The bucket stays private, the link expires after an hour, and the file never passes
through the backend.

## Running it

```bash
pip install -r requirements.txt
```

Make a `.env` next to `main.py`:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name
```

`.env` is in `.gitignore`. Keep it that way: those two keys can run up a real bill.

```bash
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Known limits

This was built to practise the algorithms, not to be deployed as-is, and a few things
would have to change first:

- CORS is open to every origin (`allow_origins=["*"]`).
- There is no authentication, so anyone who can reach the API can delete anyone's files.
- Uploads are capped at 10 MB (`MAX_UPLOAD_MB`), but the file is still buffered in full before it reaches S3.
- Every list, sort and search re-fetches the whole bucket listing from S3.

## Files

```
main.py           FastAPI app, merge sort and linear search
index.html        the page
requirements.txt
```
