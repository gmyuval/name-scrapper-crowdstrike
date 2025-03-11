from pydantic import BaseModel


class Animal(BaseModel):
    name: str
    collateral_adjective: str
    link: str | None = None
    image_path: str | None = None
