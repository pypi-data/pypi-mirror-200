from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    chatgpt3_path: Path = Path()
    api_key: str = ""
