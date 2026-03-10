import re
from typing import Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field
from utils.utils import get_hashed_password


class EmailModel(BaseModel):
    email: EmailStr = Field(description="Email inbox")
    model_config = ConfigDict(from_attributes=True)


class UserBase(EmailModel):
    first_name: str = Field(min_length=3, max_length=50,
                            description="Name, from 3 to 50 letters")
    last_name: str = Field(min_length=3, max_length=50,
                           description="Name, from 3 to 50 letters")


class SUserRegister(UserBase):
    password: str = Field(min_length=8, max_length=50,
                          description="Password, from 8 to 50 symbols")
    confirm_password: str = Field(
        min_length=8, max_length=50, description="Confirm password")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Password not matches")
        self.password = get_hashed_password(self.password)
        return self


class SUserAddDb(UserBase):
    password: str = Field(min_length=8, max_length=50,
                          description="Password in HASH-string format")


class SUserAuth(EmailModel):
    password: str = Field(min_length=8, max_length=50,
                          description="Password, from 8 to 50 symbols")


class RoleModel(BaseModel):
    id: int = Field(description="User id")
    name: str = Field(description="Role name")
    model_config = ConfigDict(from_attributes=True)


class SUserInfo(UserBase):
    id: int = Field(description="User id")
    role: RoleModel = Field(exclude=True)

    @computed_field
    def role_name(self) -> str:
        return self.role.name

    @computed_field
    def role_id(self) -> int:
        return self.role.id
