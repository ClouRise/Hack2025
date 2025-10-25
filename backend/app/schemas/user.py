import base64

from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class CreateAvatarUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    avatar_data: str

    #валидация на формат
    @field_validator("avatar_data")
    @classmethod
    def valid_base64(cls, valid_field: str):
        try:
            if "," in valid_field:
                valid_field = valid_field.split(",")[1]
            
            #декодируем
            base64.b64decode(valid_field)
            return valid_field
        except ValueError:
            raise ValueError("Invalid format base64")
        except:
            raise ValueError


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    avatar_data: str
    email: EmailStr
    is_active: bool
    room_id: UUID | None = None


class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(min_length=3)
    avatar_data: str = Field(...)
    password: str = Field(min_length=8)

    #валидация на формат
    @field_validator("avatar_data")
    @classmethod
    def valid_base64(cls, valid_field: str):
        try:
            if "," in valid_field:
                valid_field = valid_field.split(",")[1]
            
            #декодируем
            base64.b64decode(valid_field)
            return valid_field
        except ValueError:
            raise ValueError("Invalid format base64")
        except:
            raise ValueError
