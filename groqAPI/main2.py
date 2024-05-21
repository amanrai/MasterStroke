from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import mysql.connector
from mysql.connector import Error
from typing import List, Optional
import uuid

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'chatbot_user',
    'password': 'chatbot_password',
    'database': 'chatbot_db'
}

# Create a FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database interaction function
def execute_query(query: str, params: tuple = (), fetchone: bool = False, fetchall: bool = False):
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = None
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")

# Define models for API requests
class UserModel(BaseModel):
    username: str
    email: Optional[str] = None

class SessionModel(BaseModel):
    user_id: str

class MessageModel(BaseModel):
    session_id: str
    user_id: str
    message_text: str
    is_bot: bool = False

class MetadataModel(BaseModel):
    session_id: str
    metadata_key: str
    value: str

class SettingsModel(BaseModel):
    user_id: str
    setting_name: str
    setting_value: str

class SettingsUpdateModel(BaseModel):
    setting_name: str
    setting_value: str

# Create a route for the app
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Create a health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# CRUD operations for users
@app.post("/users")
def create_user(user: UserModel):
    user_id = str(uuid.uuid4())
    query = "INSERT INTO users (user_id, username, email) VALUES (%s, %s, %s)"
    execute_query(query, (user_id, user.username, user.email))
    return {"user_id": user_id, "message": "User created successfully"}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    query = "SELECT * FROM users WHERE user_id = %s"
    user = execute_query(query, (user_id,), fetchone=True)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CRUD operations for sessions
@app.post("/createSession")
def create_session(session: SessionModel):
    session_id = str(uuid.uuid4())
    query = "INSERT INTO sessions (session_id, user_id) VALUES (%s, %s)"
    execute_query(query, (session_id, session.user_id))
    
    # Generate a new message ID and insert the initial message
    message_id = str(uuid.uuid4())
    initial_message = "Session started"
    query = "INSERT INTO messages (message_id, session_id, user_id, message_text, is_bot, response_to) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(query, (message_id, session_id, session.user_id, initial_message, True, None))
    
    return {"session_id": session_id, "message_id": message_id, "message": "Session created successfully"}

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    query = "SELECT * FROM sessions WHERE session_id = %s"
    session = execute_query(query, (session_id,), fetchone=True)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    query = "SELECT * FROM messages WHERE session_id = %s ORDER BY message_time"
    messages = execute_query(query, (session_id,), fetchall=True)
    
    response = {
        "session": session,
        "message_list": messages
    }
    return response

@app.get("/users/{user_id}/sessions")
def get_session_list(user_id: str):
    query = "SELECT * FROM sessions WHERE user_id = %s"
    sessions = execute_query(query, (user_id,), fetchall=True)
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this user")
    return sessions

# CRUD operations for messages
@app.post("/messages")
def create_message(message: MessageModel):
    message_id = str(uuid.uuid4())
    query = "INSERT INTO messages (message_id, session_id, user_id, message_text, is_bot, response_to) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(query, (message_id, message.session_id, message.user_id, message.message_text, message.is_bot, None))
    return {"message_id": message_id, "message": "Message created successfully"}

@app.get("/messages/{message_id}")
def read_message(message_id: str):
    query = "SELECT * FROM messages WHERE message_id = %s"
    message = execute_query(query, (message_id,), fetchone=True)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

# CRUD operations for session metadata
@app.post("/metadata")
def create_metadata(metadata: MetadataModel):
    query = "INSERT INTO session_metadata (session_id, metadata_key, value) VALUES (%s, %s, %s)"
    execute_query(query, (metadata.session_id, metadata.metadata_key, metadata.value))
    return {"message": "Metadata created successfully"}

@app.get("/metadata/{metadata_id}")
def read_metadata(metadata_id: int):
    query = "SELECT * FROM session_metadata WHERE metadata_id = %s"
    metadata = execute_query(query, (metadata_id,), fetchone=True)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return metadata

# CRUD operations for user settings
@app.post("/users/{user_id}/settings")
def create_setting(user_id: str, setting: SettingsUpdateModel):
    query = "INSERT INTO user_settings (user_id, setting_name, setting_value) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE setting_value = %s"
    execute_query(query, (user_id, setting.setting_name, setting.setting_value, setting.setting_value))
    return {"message": "Setting created/updated successfully"}

@app.get("/users/{user_id}/settings")
def get_settings(user_id: str):
    query = "SELECT setting_name, setting_value FROM user_settings WHERE user_id = %s"
    settings = execute_query(query, (user_id,), fetchall=True)
    if not settings:
        raise HTTPException(status_code=404, detail="No settings found for this user")
    return settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
