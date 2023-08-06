import os


class Config:
    SERVER_LOG_LEVEL = os.environ.get("SERVER_LOG_LEVEL", "info")
