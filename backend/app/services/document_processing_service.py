from pathlib import Path

from app.infrastructure.document_processing.pdf_parser import (
    pdf_parser,
)
from app.services.ocr_service import ocr_service


class DocumentProcessingService:
    """
    Coordinates document processing.

    Processing strategy:

    1. Try normal text extraction.
    2. If meaningful text is found, use it.
    3. If no meaningful text is found, use OCR.
    """

    MIN_TEXT_CHARACTERS = 20

    def extract_text(
        self,
        file_path: Path,
        file_type: str,
    ) -> dict:

        normalized_type = file_type.lower()

        if normalized_type == ".pdf":

            return self._process_pdf(
                file_path
            )

        raise ValueError(
            f"Text extraction for '{file_type}' "
            "is not implemented yet."
        )

    def _process_pdf(
        self,
        file_path: Path,
    ) -> dict:

        # -----------------------------------------
        # STEP 1: Try normal PDF text extraction
        # -----------------------------------------

        extracted_text = pdf_parser.extract_text(
            file_path
        )

        page_count = pdf_parser.get_page_count(
            file_path
        )

        cleaned_text = extracted_text.strip()

        # -----------------------------------------
        # STEP 2: If enough text exists,
        #         return normal extraction
        # -----------------------------------------

        if len(cleaned_text) >= self.MIN_TEXT_CHARACTERS:

            return {
                "text": cleaned_text,
                "page_count": page_count,
                "character_count": len(cleaned_text),
                "has_text": True,
                "extraction_method": "pdf_text",
            }

        # -----------------------------------------
        # STEP 3: No meaningful text.
        #         Fall back to OCR.
        # -----------------------------------------

        ocr_result = ocr_service.extract_text_from_pdf(
            file_path
        )

        return {
            "text": ocr_result["text"],
            "page_count": ocr_result["page_count"],
            "character_count": ocr_result[
                "character_count"
            ],
            "has_text": ocr_result["has_text"],
            "extraction_method": "ocr",
        }


document_processing_service = DocumentProcessingService()