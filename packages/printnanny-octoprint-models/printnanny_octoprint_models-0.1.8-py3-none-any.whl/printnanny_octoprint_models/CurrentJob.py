from .Job import Job
from .JobProgress import JobProgress
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class CurrentJob(BaseModel): 
  job: Job = Field()
  progress: JobProgress = Field()
  state: str = Field()
  error: Optional[str] = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return CurrentJob(**json.loads(json_string))
