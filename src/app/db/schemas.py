from pydantic import BaseModel


class ShortLink(BaseModel):
    short_url: str
    long_url: str
    access_count: int
    is_active: bool
    datetime: str

    class Config:
        orm_mode = True


class UserInputShortLink(BaseModel):
    short_url: str
    long_url: str
    is_custom_url: bool

    class Config:
        orm_mode = True
