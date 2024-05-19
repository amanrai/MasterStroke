from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

#Create a class for the settings input
class Settings(BaseModel):
    settingName: str
    settingValue: str

settings = {
    "model": "llama3-8b-8192",
    "temperature":0.9,
    "groq_api_key":"",
    "useAgent": True,
    "useWebSearch": False,
    "brave_api_key": "",
}

#Create a fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Create a route for the app
@app.get("/")
def read_root():
    return {"Hello": "World"}

#Create a health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

#Create a get settings route
@app.get("/settings")
def get_settings():

    return json.dumps(settings)

#Create a post settings route
@app.post("/settings")
def post_settings(new_settings: Settings):
    settings[new_settings.settingName] = new_settings.settingValue
    return settings


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)