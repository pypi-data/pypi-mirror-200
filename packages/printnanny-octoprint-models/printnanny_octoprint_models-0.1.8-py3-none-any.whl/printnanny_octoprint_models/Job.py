from .GcodeFile import GcodeFile
from .Filament import Filament
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class Job(BaseModel): 
  file: GcodeFile = Field()
  averagePrintTime: Optional[float] = Field()
  estimatedPrintTime: float = Field()
  lastPrintTime: float = Field()
  filaments: Optional[list[Filament]] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return Job(**json.loads(json_string))
