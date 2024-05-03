from pydantic import BaseModel, EmailStr
from typing import Optional

class Location(BaseModel):
    address: str
    api_key: str

class LocationResponse(BaseModel):
    address: str
    lat: float
    lng: float

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class Cordinates_Schemas(BaseModel):
    address: str
    latitude: float
    longitude: float

class CordinateResponse(BaseModel):
    address: str
    latitude: float
    longitude: float


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None