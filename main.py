import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import Feedback
from services.google_sheets import GoogleSheetsClient
from typing import Dict

load_dotenv()

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
SPREADSHEET_RANGE = os.getenv("SPREADSHEET_RANGE", "Sheet1!A:F")

if not SPREADSHEET_ID:
    raise RuntimeError("SPREADSHEET_ID environment variable is required. See .env.example for details.")

# initialize sheets client
sheets_client = GoogleSheetsClient(GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID)

app = FastAPI(title="Shopping Feedback")

# Allow local index.html to POST (or other origin you want to use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Shopping Feedback API is running."}

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    try:
        #prepare row data: add timestamp optionally
        from datetime import datetime
        timestamp = datetime.utcnow().isoformat() + "Z"
        row = [
            timestamp,
            feedback.name,
            feedback.contact,
            str(feedback.shopping_rating),
            feedback.items_not_found or "",
            feedback.price_reduction_items or "",
            feedback.improvement_suggestions or ""
        ]

        # if your sheet range expects A:G update SPREADSHEET_RANGE accordingly
        res = sheets_client.append_row(SPREADSHEET_RANGE, row)
        return {"message": "Feedback submitted", "result": res}



