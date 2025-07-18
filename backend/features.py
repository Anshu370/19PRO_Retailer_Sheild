from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from utils import scan_and_parse, compute_security_score
import pandas as pd
from nlp_detector import predict_phishing

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

    # VirusTotal Scan
    vt_records = [await scan_and_parse(link) for link in email_data.links]
    vt_records += [await scan_and_parse(att.url) for att in email_data.attachments]

    print("\n🛡️ VirusTotal Scan Summary:\n")
    df = pd.DataFrame(vt_records)
    print(df)

    # NLP Phishing Prediction
    nlp_result = predict_phishing(email_data.subject, email_data.body)

    # Compute total security score (combined VT + NLP)
    security_score = compute_security_score(vt_records, nlp_result)

    return {
        "subject": email_data.subject,
        "sender": f"{email_data.senderName} <{email_data.senderEmail}>",
        "virustotal": vt_records,
        "nlp_prediction": nlp_result,
        "score": security_score
    }
