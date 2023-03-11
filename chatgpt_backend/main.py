from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import chat
from routes import user

app = FastAPI()
app.include_router(chat.router)
app.include_router(user.router)

origins = [
    "https://doggy-gpt-frontend.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(GZipMiddleware, minimum_size=500) # It kills the event source stream