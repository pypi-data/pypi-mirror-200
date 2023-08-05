
from enum import Enum
class GcodeEvent(Enum): 
  ALERT_M300 = "Alert__M300"
  COOLING_M245 = "Cooling__M245"
  DWELL_G4 = "Dwell__G4"
  ESTOP_M112 = "Estop__M112"
  FILAMENT_CHANGE_M600 = "FilamentChange__M600"
  FILAMENT_CHANGE_M701 = "FilamentChange__M701"
  FILAMENT_CHANGE_M702 = "FilamentChange__M702"
  HOME_G28 = "Home__G28"
  POWER_ON_M80 = "PowerOn__M80"
  POWER_OFF_M81 = "PowerOff__M81"