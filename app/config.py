import pathlib

import toml
from pydantic import BaseSettings

path = pathlib.Path(__file__).parent.absolute()
with open(f"{path}/../pyproject.toml") as f:
    project_data = toml.load(f)

app_version = project_data["tool"]["poetry"]["version"]
app_name = project_data["tool"]["poetry"]["name"]


class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str
    static_token: str
    environment: str = "prod"
    logging_level: str = "INFO"
    root_path: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
