from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.seismic_service import process_waveform

router = APIRouter()

ALLOWED_EXTENSIONS = {".sac", ".mseed", ".ms", ".seed"}


def _validate_filename(filename: str) -> None:
    dot = filename.rfind(".")
    if dot <= 0:
        raise HTTPException(
            status_code=400,
            detail=f'文件 "{filename}" 缺少扩展名，请上传 SAC（.sac）或 miniSEED（.mseed / .ms / .seed）格式的文件',
        )
    ext = filename[dot:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式：{filename}，扩展名 {ext} 不在允许范围内。请上传 SAC（.sac）或 miniSEED（.mseed / .ms / .seed）格式的文件",
        )


@router.post("/waveform/upload")
async def upload_waveform(file: UploadFile = File(...)):
    """Upload SAC/miniSEED file and run analysis."""
    _validate_filename(file.filename or "unknown")
    content = await file.read()
    result = process_waveform(content, file.filename or "unknown")
    return result


@router.get("/waveform/stations")
def get_stations():
    """Get station list."""
    return [
        {"id": "STA01", "name": "BJI", "latitude": 39.9, "longitude": 116.4, "elevation": 45},
        {"id": "STA02", "name": "SSE", "latitude": 31.2, "longitude": 121.5, "elevation": 10},
    ]


@router.get("/waveform/events")
def get_events():
    """Get seismic event catalog."""
    return [
        {"id": "1", "magnitude": 4.2, "depth": 12.5, "location": "四川雅安"},
        {"id": "2", "magnitude": 3.8, "depth": 8.3, "location": "云南大理"},
    ]
