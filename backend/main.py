from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import features

app = FastAPI()
origins = [
    "chrome-extension://maeacndgihdgafbhjfcljdohilindcdp",
    "https://mail.google.com"
]
 # origin of react-app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(features.router)