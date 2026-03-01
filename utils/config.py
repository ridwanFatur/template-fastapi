import sys
from dotenv import load_dotenv
import os
from google.auth import default
from google.cloud import secretmanager

load_dotenv()


def get_project_id():
    _, project_id = default()
    return project_id


IS_DEBUG = "uvicorn" in sys.modules and "--reload" in sys.argv
PROJECT_ID = "" if IS_DEBUG else get_project_id()


def get_secret(secret_name: str, project_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def get_config(env_name: str, secret_name: str):
    return os.getenv(env_name) if IS_DEBUG else get_secret(secret_name, PROJECT_ID)


CORS_ORIGINS = get_config("CORS_ORIGINS", "APP1_CORS_ORIGINS")
SECRET_KEY = get_config("SECRET_KEY", "APP1_SECRET_KEY")
ALGORITHM = get_config("ALGORITHM", "APP1_ALGORITHM")
GOOGLE_CLIENT_ID = get_config("GOOGLE_CLIENT_ID", "APP1_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_config(
    "GOOGLE_CLIENT_SECRET", "APP1_GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = get_config(
    "GOOGLE_REDIRECT_URI", "APP1_GOOGLE_REDIRECT_URI")
