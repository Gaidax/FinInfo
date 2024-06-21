from app.schemas.pan import ProteanPanVerificationRecordSchema
from app.schemas.common import StepStatus


def get_pan_status(pan_record: ProteanPanVerificationRecordSchema) -> StepStatus:
    if (
        pan_record.pan_status == "E"
        and pan_record.name == "Y"
        and pan_record.fathername == "Y"
        and pan_record.dob == "Y"
        and pan_record.seeding_status == "Y"
    ):
        return StepStatus.success
    return StepStatus.failed


def get_status_remark(pan_record: ProteanPanVerificationRecordSchema) -> str:
    if pan_record.pan_status != "E":
        return "The PAN status is not valid"
    if pan_record.name == "N":
        return "Name mismatch"
    if pan_record.fathername == "N":
        return "Father's name mismatch"
    if pan_record.dob == "N":
        return "DOB mismatch"
    if pan_record.seeding_status != "Y":
        return "Aadhaar is not linked"

    