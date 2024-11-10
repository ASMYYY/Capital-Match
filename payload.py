from pydantic import BaseModel

class UserQuery(BaseModel):
  candidate_id: str