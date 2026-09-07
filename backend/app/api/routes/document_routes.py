from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.document_schema import DocumentUploadResponse
from app.services.document_service import document_service
from app.services.extraction_service import extraction_service
from app.services.summary_service import summary_service
from app.services.validation_service import validation_service


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload a document.

    The file is validated and stored locally.
    """

    try:
        return await document_service.upload_document(file)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "uploading the document."
            ),
        ) from exc


# =========================================================
# EXTRACT DOCUMENT TEXT
# =========================================================

@router.get("/{document_id}/text")
async def extract_document_text(
    document_id: str,
):
    """
    Extract raw text from an uploaded document.

    Processing strategy:

    1. Try native PDF text extraction.
    2. If insufficient text is found, use OCR.
    """

    try:
        upload_dir = Path(settings.UPLOAD_DIR)

        matching_files = list(
            upload_dir.glob(
                f"{document_id}.*"
            )
        )

        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        file_path = matching_files[0]

        file_type = file_path.suffix.lower()

        result = await document_service.process_document(
            file_path=file_path,
            file_type=file_type,
        )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            "file_type": file_type,
            "processing_status": "completed",
            **result,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process document.",
        ) from exc


# =========================================================
# AI STRUCTURED EXTRACTION
# =========================================================

@router.post("/{document_id}/extract")
async def extract_structured_document(
    document_id: str,
):
    """
    Extract structured information from an uploaded document.
    """

    try:
        upload_dir = Path(settings.UPLOAD_DIR)

        matching_files = list(
            upload_dir.glob(
                f"{document_id}.*"
            )
        )

        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        file_path = matching_files[0]

        file_type = file_path.suffix.lower()

        text_result = await document_service.process_document(
            file_path=file_path,
            file_type=file_type,
        )

        document_text = text_result.get(
            "text",
            "",
        )

        if not document_text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No text could be extracted from "
                    "the document."
                ),
            )

        structured_data = (
            extraction_service.extract_document_data(
                document_text=document_text,
            )
        )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            "file_type": file_type,
            "processing_status": "completed",
            "extraction_method": text_result.get(
                "extraction_method"
            ),
            "source_text": {
                "page_count": text_result.get(
                    "page_count"
                ),
                "character_count": text_result.get(
                    "character_count"
                ),
            },
            "structured_data": (
                structured_data.model_dump(
                    mode="json"
                )
            ),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to extract structured "
                "information from document."
            ),
        ) from exc


# =========================================================
# AI EXTRACTION + VALIDATION
# =========================================================

@router.post("/{document_id}/validate")
async def validate_document(
    document_id: str,
):
    """
    Extract structured information and validate it.
    """

    try:
        upload_dir = Path(settings.UPLOAD_DIR)

        matching_files = list(
            upload_dir.glob(
                f"{document_id}.*"
            )
        )

        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        file_path = matching_files[0]

        file_type = file_path.suffix.lower()

        text_result = await document_service.process_document(
            file_path=file_path,
            file_type=file_type,
        )

        document_text = text_result.get(
            "text",
            "",
        )

        if not document_text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No text could be extracted from "
                    "the document."
                ),
            )

        structured_data = (
            extraction_service.extract_document_data(
                document_text=document_text,
            )
        )

        validation_result = (
            validation_service.validate_document(
                document=structured_data,
            )
        )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            "file_type": file_type,
            "processing_status": "completed",
            "extraction_method": text_result.get(
                "extraction_method"
            ),
            "source_text": {
                "page_count": text_result.get(
                    "page_count"
                ),
                "character_count": text_result.get(
                    "character_count"
                ),
            },
            "structured_data": (
                structured_data.model_dump(
                    mode="json"
                )
            ),
            "validation": (
                validation_result.model_dump(
                    mode="json"
                )
            ),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to validate document."
            ),
        ) from exc


# =========================================================
# COMPLETE AI DOCUMENT ANALYSIS
# =========================================================

@router.post("/{document_id}/summary")
async def summarize_document(
    document_id: str,
):
    """
    Generate a complete AI analysis of an uploaded document.

    Processing pipeline:

    Uploaded document
        ↓
    Native PDF extraction / OCR
        ↓
    LLM structured extraction
        ↓
    Business-rule validation
        ↓
    AI summary
        ↓
    Complete document analysis
    """

    try:
        # -------------------------------------------------
        # STEP 1: FIND DOCUMENT
        # -------------------------------------------------

        upload_dir = Path(settings.UPLOAD_DIR)

        matching_files = list(
            upload_dir.glob(
                f"{document_id}.*"
            )
        )

        if not matching_files:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        file_path = matching_files[0]

        file_type = file_path.suffix.lower()

        # -------------------------------------------------
        # STEP 2: EXTRACT TEXT
        # -------------------------------------------------

        text_result = await document_service.process_document(
            file_path=file_path,
            file_type=file_type,
        )

        document_text = text_result.get(
            "text",
            "",
        )

        if not document_text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No text could be extracted from "
                    "the document."
                ),
            )

        # -------------------------------------------------
        # STEP 3: STRUCTURED AI EXTRACTION
        # -------------------------------------------------

        structured_data = (
            extraction_service.extract_document_data(
                document_text=document_text,
            )
        )

        # -------------------------------------------------
        # STEP 4: BUSINESS VALIDATION
        # -------------------------------------------------

        validation_result = (
            validation_service.validate_document(
                document=structured_data,
            )
        )

        # -------------------------------------------------
        # STEP 5: AI SUMMARY
        # -------------------------------------------------

        summary_result = (
            summary_service.generate_summary(
                document=structured_data,
                validation=validation_result,
            )
        )

        # -------------------------------------------------
        # STEP 6: RETURN COMPLETE ANALYSIS
        # -------------------------------------------------

        return {
            "document_id": document_id,
            "filename": file_path.name,
            "file_type": file_type,
            "processing_status": "completed",

            "source_text": {
                "page_count": text_result.get(
                    "page_count"
                ),
                "character_count": text_result.get(
                    "character_count"
                ),
                "extraction_method": text_result.get(
                    "extraction_method"
                ),
            },

            "structured_data": (
                structured_data.model_dump(
                    mode="json"
                )
            ),

            "validation": (
                validation_result.model_dump(
                    mode="json"
                )
            ),

            "summary": (
                summary_result.model_dump(
                    mode="json"
                )
            ),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate AI document summary."
            ),
        ) from exc