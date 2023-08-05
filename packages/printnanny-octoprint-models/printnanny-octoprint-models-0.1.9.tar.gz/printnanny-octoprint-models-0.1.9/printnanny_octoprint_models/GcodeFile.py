
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class GcodeFile(BaseModel): 
  fileName: str = Field()
  display: Optional[str] = Field()
  filePath: str = Field()
  origin: Optional[str] = Field()
  size: Optional[int] = Field()
  timestamp: Optional[int] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return GcodeFile(**json.loads(json_string))
