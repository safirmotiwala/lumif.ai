# lumif.ai
Lumif.ai MCP Server Management Agent Assignment

## Steps to run

1. Create virtual env
   ```
   python3.13 -m venv env
   source env/bin/activate
   ```
2. Install requirements.txt
   ```
   pip install -r requirements.txt
   ```
3. Copy .env.example to .env
   ```
   cp .env.example .env
   ```
4. Add the following env variables
   ```
   GOOGLE_API_KEY=
   LANGSMITH_API_KEY=
   ```
5. Run the backend server
   ```
   uvicorn main:app --reload
   ```
After starting the server, you can view the api docs at - http://127.0.0.1:8000/docs

To run frontend, start a new terminal window and navigate to the directory

1. Activate virtual env
  ```
  source env/bin/activate
  ```
2. Run the client server
  ```
  streamlit run streamlit_app.py
  ```
