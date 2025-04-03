from fastapi import FastAPI
from dotenv import load_dotenv
from agent import * 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from a .env file
load_dotenv()

# Maps session_id (str) to agent (CodeAgent) 
agents = {}

def get_agent(session_id: str):
    if session_id not in agents:
        agents[session_id] = create_tool_agent()
    return agents[session_id]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],  # Allow requests from localhost:4000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def greet_json():
    return {"Hello": "World!"}


class UserQuery(BaseModel):
    session_id: str
    message: str | None = None

@app.post("/overview")
def overview(user_query: UserQuery):
    print(f"[overview] session_id: {user_query.session_id}, message: {user_query.message}")
    response = compare_contractors()
    return {"response": response}

@app.post("/chat")
def chat(user_query: UserQuery):
    print(f"[chat] session_id: {user_query.session_id}, message: {user_query.message}")
    agent = get_agent(user_query.session_id)
    response = agent.run(
        user_query.message 
    )
    return {"response": response}