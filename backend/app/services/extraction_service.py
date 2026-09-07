from app.infrastructure.llm.llm_client import (
    LLMClient,
)
from app.infrastructure.llm.prompts import (
    DOCUMENT_EXTRACTION_SYSTEM_PROMPT,
    DOCUMENT_EXTRACTION_USER_PROMPT,
)
from app.schemas.extraction_schema import (
    DocumentExtraction,
)


class ExtractionService:
    """
    Application service responsible for converting
    extracted document text into structured information.

    Flow:

    Document text
        ↓
    Prompt construction
        ↓
    LLM client
        ↓
    Pydantic structured output
    """

    def __init__(self):
        self.llm_client = LLMClient()

    def extract_document_data(
        self,
        document_text: str,
    ) -> DocumentExtraction:

        if not document_text:
            raise ValueError(
                "Cannot perform structured extraction "
                "because the document contains no text."
            )

        cleaned_text = document_text.strip()

        if not cleaned_text:
            raise ValueError(
                "Cannot perform structured extraction "
                "because the document text is empty."
            )

        user_prompt = DOCUMENT_EXTRACTION_USER_PROMPT.format(
            document_text=cleaned_text
        )

        return self.llm_client.extract_structured_data(
            system_prompt=DOCUMENT_EXTRACTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=DocumentExtraction,
        )


extraction_service = ExtractionService()