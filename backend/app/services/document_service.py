from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.schemas.document_schema import DocumentUploadResponse
from app.services.document_processing_service import (
    document_processing_service,
)
from app.utils.file_utils import (
    generate_document_id,
    save_uploaded_file,
    validate_file_extension,
)


class DocumentService:
    """
    Handles the business logic related to documents.

    Responsibilities:
    - Upload documents
    - Validate document types
    - Generate document IDs
    - Process uploaded documents
    """

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadResponse:

        if not file.filename:
            raise ValueError("No filename was provided.")

        extension = validate_file_extension(
            file.filename
        )

        document_id = generate_document_id()

        _, file_size = await save_uploaded_file(
            file=file,
            document_id=document_id,
            extension=extension,
        )

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            file_type=extension,
            file_size=file_size,
            status="uploaded",
            uploaded_at=datetime.now(timezone.utc),
            message="Document uploaded successfully.",
        )

    async def process_document(
        self,
        file_path: Path,
        file_type: str,
    ) -> dict:
        """
        Process an uploaded document and extract its text.
        """

        return document_processing_service.extract_text(
            file_path=file_path,
            file_type=file_type,
        )


document_service = DocumentService()