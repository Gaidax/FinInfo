from enum import Enum

class StepType(str, Enum):
  pan = 'pan'
  eaadhaar = 'eaadhaar'
  bank_account = 'bank_account'
  vkyc = "vkyc"
  other_detail = "other_detail"


class StepStatus(str, Enum):
  success = 'success'
  in_progress = 'in_progress'
  failed = 'failed'
  error = "error"
  