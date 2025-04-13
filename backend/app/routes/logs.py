from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

@router.get("/logs")
def read_logs():
    log_path = Path("logs/app.log")
    if not log_path.exists():
        return {"message": "No logs found"}

    last_lines = log_path.read_text().splitlines()[-20:]
    return {"logs": last_lines}
