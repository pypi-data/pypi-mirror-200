
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class Filament(BaseModel): 
  length: float = Field()
  volume: float = Field()
  toolName: str = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return Filament(**json.loads(json_string))
