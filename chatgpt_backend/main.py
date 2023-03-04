from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import chat

app = FastAPI()
app.include_router(chat.router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)