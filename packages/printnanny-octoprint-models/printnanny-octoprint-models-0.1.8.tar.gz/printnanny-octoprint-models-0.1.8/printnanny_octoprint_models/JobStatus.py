
from enum import Enum
class JobStatus(Enum): 
  PRINT_STARTED = "PrintStarted"
  PRINT_FAILED = "PrintFailed"
  PRINT_DONE = "PrintDone"
  PRINT_CANCELLING = "PrintCancelling"
  PRINT_CANELLED = "PrintCanelled"
  PRINT_PAUSED = "PrintPaused"
  PRINT_RESUMED = "PrintResumed"