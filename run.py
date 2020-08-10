from app.app import create_app
import os

settings_name = os.getenv("APP_SETTINGS")

app = create_app(settings_name)