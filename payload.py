from pydantic import BaseModel

class UserQuery(BaseModel):
  candidate_id: str

class MailQuery(BaseModel):
  product_recommendation: str