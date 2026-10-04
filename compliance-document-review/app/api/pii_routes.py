from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.models.pii import (
    MaskingResult,
    RehydrationRequest,
    RehydrationResponse,
)

from app.services.document.extractor import (
    DocumentExtractionError,
    UnsupportedDocumentTypeError,
    extract_text,
)

from app.services.pii.masking_service import (
    pii_masking_service,
)

from app.services.pii.unmasker import (
    MappingNotFoundError,
    unmask_text,
)


router = APIRouter(
    prefix="/api/v1/pii",
    tags=["PII Security"],
)


@router.post(
    "/mask",
    response_model=MaskingResult,
)
async def mask_document(
    file: UploadFile = File(...),
):

    try:

        content = await file.read()

        text = extract_text(
            filename=file.filename or "document.txt",
            content=content,
        )

        if not text.strip():

            raise HTTPException(
                status_code=400,
                detail="Document contains no extractable text.",
            )

        result = pii_masking_service.mask(
            text=text
        )

        return result

    except UnsupportedDocumentTypeError as exc:

        raise HTTPException(
            status_code=415,
            detail=str(exc),
        ) from exc

    except DocumentExtractionError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc


@router.post(
    "/rehydrate",
    response_model=RehydrationResponse,
)
async def rehydrate_document(
    request: RehydrationRequest,
):

    try:

        text = unmask_text(
            document_id=request.document_id,
            masked_text=request.masked_text,
        )

        return RehydrationResponse(
            document_id=request.document_id,
            text=text,
        )

    except MappingNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc