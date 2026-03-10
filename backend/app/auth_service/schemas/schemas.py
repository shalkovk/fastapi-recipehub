import re
from typing import Self
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator, computed_field


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
        self.password = get_password_hash(self.password)
        return self
