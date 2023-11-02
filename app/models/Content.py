from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Default data model corresponding to faker data
class Content(BaseModel):
    username: str = Field(description="User username")
    name: str = Field(description="User name")
    sex: str = Field(description="User sex")
    address: str = Field(description="User address")
    mail: str = Field(description="User mail")
    birthdate: Optional[datetime] = Field(description="User birthdate")

    class Config:
        # Example data for documentation
        schema_extra = {
            "example": {
                "username": "johndoe",
                "name": "John Doe",
                "sex": "M",
                "address": "123 rue du Poulet, 69010 Lyon, France",
                "mail": "johndoe@example.com",
                "birthdate": "1980-01-01T00:00:00"
            }
        }