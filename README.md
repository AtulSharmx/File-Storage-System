# File Storage System

Hello! This is a simple File Storage System that I built. It uses a **Python (FastAPI)** backend and an **AWS S3** bucket to store files securely. The frontend is built using standard HTML/CSS/JavaScript.

## Features
- Upload files directly to AWS S3.
- List all uploaded files with their sizes and upload dates.
- Sort files by name, size, or date.
- Search for specific files.
- Download and delete files.

---

## How to run this project on your local computer

If you want to run this project on your own machine, just follow these simple steps!

### 1. Install Requirements
Make sure you have Python installed. Then, open your terminal and install all the necessary libraries by running:
```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Because this project connects to AWS, you need to provide your AWS credentials. 
1. Create a file named exactly `.env` in the same folder as `main.py`.
2. Open the `.env` file and paste the following inside, replacing the placeholder text with your actual AWS details:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name
```
*(Note: Never upload your `.env` file to GitHub! Keep it safe on your computer.)*

### 3. Run the Backend Server
Now it's time to start the server! Run this command in your terminal:
```bash
uvicorn main:app --reload
```
You should see a message saying the application startup is complete. The backend is now running on `http://127.0.0.1:8000`.

### 4. Open the Frontend
Finally, just double-click the `index.html` file to open it in your web browser. You should now be able to see the app, upload files, and interact with the system!
