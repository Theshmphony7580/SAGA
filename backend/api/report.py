from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.ml.report_builder import export_report
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["report"])


class ReportSection(BaseModel):
    title: str
    content: str


class ReportRequest(BaseModel):
    path: str
    sections: List[ReportSection] = []
    include_charts: bool = True
    format: str = "pdf"  # pdf or xlsx


class ReportResponse(BaseModel):
    output_path: str


@router.post("/report/export", response_model=ReportResponse)
async def report_export(req: ReportRequest) -> ReportResponse:
    try:
        out_path = export_report(
            dataset_path=req.path,
            sections=[s.dict() for s in req.sections],
            include_charts=req.include_charts,
            output_format=req.format,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ReportResponse(output_path=out_path)


