from uuid import uuid4
from fastapi import APIRouter
from app.schemas.bank import CreateBankAccountRequestSchema
from app.schemas.common import StepType, StepStatus

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])


@router.get("")
async def get_bank_accounts():
    return {"bank_accounts": [
        {
            "account_number": "1234567890",
            "IFSC": "HDFC000001",
            "bank": "HDFC Bank",
            "branch": "Nariman Point, Mumbai"
        },
        {
            "account_number": "23234567890",
            "IFSC": "YES00001",
            "bank": "Yes Bank",
            "branch": "C G Road, Ahmedabad"
        }
    ]}


@router.post("")
async def create_bank_account(input: CreateBankAccountRequestSchema):
    """
    - Validate inputs - pydantic
    - Validate session
    - Verify whether the step is already complete
    - invoke bank verification API
      - success: next step
      - fail: return
    - verify whether the bank account belongs to the user
      - success: next step
      - fail: return
    - update session
    - return
    - error handling

    Dependencies:
    - bank verification APIs - available
    - verify bank account - available
    """
    if input.account_number == "1234567890":
        return {
            "id": uuid4(),
            "type": StepType.bank_account,
            "status": StepStatus.success,
            "status_remark": None,
        }

    return {
        "id": uuid4(),
        "type": StepType.bank_account,
        "status": StepStatus.failed,
        "status_remark": "Unable to validate bank account",
    }
