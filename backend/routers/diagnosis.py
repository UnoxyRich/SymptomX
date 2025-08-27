
from fastapi import APIRouter
from ..models import DiagnoseRequest, DiagnoseResponse, Possibility, Medication
from ..providers.logic import score, triage_message

router = APIRouter(prefix="/api", tags=["diagnosis"])

@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: DiagnoseRequest):
    result = score(payload.symptoms)
    top = Possibility(**result["top"])
    others = [Possibility(**o) for o in result["others"]]
    # Attach Amazon search link at the edge case on frontend (hover), here we just pass meds through
    return DiagnoseResponse(
        top=top,
        others=others,
        advice=f'{triage_message(top.triage)} {result["advice"]}'
    )
