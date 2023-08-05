from .GcodeEvent import GcodeEvent
import json
from typing import Optional, Any
from pydantic import BaseModel, Field
class OctoPrintGcode(BaseModel): 
  gcode: GcodeEvent = Field()

  def serializeToJson(self):
    return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=2)

  @staticmethod
  def deserializeFromJson(json_string):
    return OctoPrintGcode(**json.loads(json_string))
