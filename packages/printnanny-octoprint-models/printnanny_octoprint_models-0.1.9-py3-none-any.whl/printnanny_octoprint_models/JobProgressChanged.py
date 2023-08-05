from .Job import Job
from .JobProgress import JobProgress
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class JobProgressChanged(BaseModel): 
  job: Optional[Job] = Field()
  storage: Optional[str] = Field(alias='Drive location of the gcode file')
  path: Optional[str] = Field(alias='Drive location of the gcode file')
  progress: Optional[JobProgress] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return JobProgressChanged(**json.loads(json_string))
