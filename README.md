1. Create a .env file containing the relevant keys:
    VITE_OPENAI_API_KEY=
    OPENAI_API_KEY=
    HUGGINGFACE_API_TOKEN=
    REASONING_MODEL_ID=deepseek-r1:7b
    TOOL_MODEL_ID=deepseek-r1:7b
    USE_HUGGINGFACE=yes

2. Install the python virtual environment
    > python3.13 -m virtualenv venv
    > .\venv\scripts\activate
    (venv)> pip install -r requirements.txt

3. Install the necessary npm packages
    > npm install
    
4. Run the backend:
    (venv)> fastapi run backend/app.py

5. Run the frontend:
    > npx vite --port=4000

Note that upon loading the chat UI, the frontend will make a request to the backend API, so it's
important to have the backend running first.  