import uuid

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    full_name: str | None = None


class User(UserBase):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))

    class Config:
        allow_population_by_field_name = True


class UserCreate(UserBase):
    password: str


class InternalUser(User):
    hashed_password: str

    class Config(User.Config):
        pass
