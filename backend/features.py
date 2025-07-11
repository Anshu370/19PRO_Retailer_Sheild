from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from utils import scan_and_parse
import pandas as pd
from Virustotal import scan_file_virustotal


router = APIRouter()

# Define EmailData model
class Attachment(BaseModel):
    name: str
    type: str
    url: str

class EmailData(BaseModel):
    subject: str
    senderName: str
    senderEmail: str
    body: str
    links: List[str]
    images: List[str]
    attachments: List[Attachment]


@router.post("/api/process_email")
async def process_email(email_data: EmailData):

    print("📩 Received email:", email_data.subject)

    records = [await scan_and_parse(link) for link in email_data.links]
    records += [await scan_and_parse(att.url) for att in email_data.attachments]

    # Create and print the DataFrame
    df = pd.DataFrame(records)
    print("\n🛡️ VirusTotal Scan Summary:\n")
    print(df)

    return {
    "subject": email_data.subject,
    "sender": f"{email_data.senderName} <{email_data.senderEmail}>",
    "virustotal": records
    }

@router.post("/api/scan_attachment")
async def scan_attachment(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        result = await scan_file_virustotal(file_bytes, file.filename)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}