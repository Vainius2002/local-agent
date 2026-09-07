import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
APP_PATH=os.environ["APP_PATH"]

DATABASE_URL=os.environ["DATABASE_URL"]

AUTH_SERVICE_URL=os.environ["AUTH_SERVICE_URL"]
APP_URL=os.environ["APP_URL"]
WORKSPACE_PATH=os.environ["WORKSPACE_PATH"]
