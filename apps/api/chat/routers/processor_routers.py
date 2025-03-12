from fastapi import APIRouter, Depends, HTTPException, Request
from chat.services import ExcelProcessorService
from chat.schemas import ProcessorRequest, ProcessorResponse
import traceback

router = APIRouter(prefix="/processor", tags=["processor"])


def get_processor_service():
    return ExcelProcessorService()


@router.post("/process", response_model=ProcessorResponse)
async def process(
    request: ProcessorRequest,
    processor_service=Depends(get_processor_service),
):
    try:
        processor_service.process(request.key)
        return {"message": "Processing completed successfully"}
    except Exception as e:
        # Get the full stack trace
        error_trace = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_trace}")

        # Return a more detailed error message
        raise HTTPException(status_code=500, detail=f"Failed to process: {str(e)}")
