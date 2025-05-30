from fastapi import FastAPI
from api.routes import router 
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
    "http://localhost:5500"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)