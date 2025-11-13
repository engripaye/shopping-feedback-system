from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
if not SPREADSHEET_ID:
    raise RuntimeError("SPREADSHEET_ID environment variable is required. See .env.example for details.")

app = FastAPI()

# Allow frontend form submission
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse("index.html")

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"), scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


@app.post("/submit/")
async def submit_feedback(
        name: str = Form(...),
        contact: str = Form(...),
        rating: str = Form(...),
        missing_items: str = Form(...),
        price_reduce: str = Form(...),
        improvement: str = Form(...),
):
    # Save to Google Sheets
    sheet.append_row([name, contact, rating, missing_items, price_reduce, improvement])
    return {"status": "success", "message": "Feedback saved successfully!"}
