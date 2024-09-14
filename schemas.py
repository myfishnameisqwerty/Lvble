from pydantic import BaseModel, EmailStr


class CommandRequest(BaseModel):
    tenant_portal: str
    username: str
    password: str


class DataSchema(BaseModel):
    email: EmailStr
    phone: str
    management_company: str
    address: str
