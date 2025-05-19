from fastapi import FastAPI
from reco_music.api import router 

app=FastAPI()
app.include_router(router)