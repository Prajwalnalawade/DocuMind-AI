from app.infrastructure.llm.llm_client import LLMClient
from app.schemas.extraction_schema import DocumentExtraction
from app.schemas.summary_schema import DocumentSummary
from app.schemas.validation_schema import ValidationResult


SUMMARY_SYSTEM_PROMPT = """
You are DocuMind AI, an intelligent business document
analysis assistant.

Your task is to generate a concise and useful summary
of a business document using the structured information
provided to you.

The document may be:

- invoice
- quotation
- receipt
- contract
- other

Rules:

1. Use only the supplied structured document data.
2. Never invent missing information.
3. Do not create values that are not present.
4. Clearly mention missing important information.
5. Explain financial information accurately.
6. Highlight important business terms.
7. Highlight validation errors and warnings.
8. Keep the summary professional and easy to understand.
9. Recommendations must be based only on the supplied data.
10. Do not provide legal, financial or professional advice.
11. Return only the requested structured output.
"""


SUMMARY_USER_PROMPT = """
Generate an intelligent summary of the following business
document.

STRUCTURED DOCUMENT DATA
========================

{document_data}

VALIDATION RESULT
=================

{validation_data}

Summary requirements:

- Explain what the document is about.
- Identify the document type.
- Identify the parties involved.
- Summarize important products or services.
- Summarize financial information.
- Mention payment and delivery terms.
- Highlight important contractual or business terms.
- Highlight validation warnings or errors.
- Clearly identify important missing information.
- Provide a practical document-level recommendation.
- Do not invent information.
"""


class SummaryService:
    """
    Application service responsible for generating
    AI-powered document summaries.

    Flow:

    Structured document
          ↓
    Validation result
          ↓
    Summary prompt
          ↓
    LLM client
          ↓
    Pydantic DocumentSummary
    """

    def __init__(self):
        self.llm_client = LLMClient()

    def generate_summary(
        self,
        document: DocumentExtraction,
        validation: ValidationResult,
    ) -> DocumentSummary:
        """
        Generate an AI summary from structured document
        information and its validation result.
        """

        document_data = document.model_dump(
            mode="json"
        )

        validation_data = validation.model_dump(
            mode="json"
        )

        user_prompt = SUMMARY_USER_PROMPT.format(
            document_data=document_data,
            validation_data=validation_data,
        )

        return self.llm_client.extract_structured_data(
            system_prompt=SUMMARY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=DocumentSummary,
        )


summary_service = SummaryService()