
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class JobProgress(BaseModel): 
  completion: Optional[float] = Field()
  filepos: Optional[int] = Field()
  printTime: Optional[int] = Field()
  printTimeLeft: Optional[int] = Field()
  printTimeLeftOrigin: Optional[str] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return JobProgress(**json.loads(json_string))
