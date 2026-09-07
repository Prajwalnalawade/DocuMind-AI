from pydantic import BaseModel, Field


class FinancialSummary(BaseModel):
    """
    Human-readable financial summary.
    """

    currency: str | None = Field(
        default=None,
        description="Currency used in the document.",
    )

    subtotal: float | None = Field(
        default=None,
        description="Document subtotal.",
    )

    discount: float | None = Field(
        default=None,
        description="Discount applied to the document.",
    )

    tax: float | None = Field(
        default=None,
        description="Tax amount.",
    )

    shipping: float | None = Field(
        default=None,
        description="Shipping or delivery charges.",
    )

    total: float | None = Field(
        default=None,
        description="Final document total.",
    )

    explanation: str = Field(
        description=(
            "Short natural-language explanation of "
            "the financial information."
        )
    )


class DocumentSummary(BaseModel):
    """
    AI-generated summary of a business document.
    """

    overview: str = Field(
        description=(
            "A concise overview explaining what the "
            "document is about."
        )
    )

    document_type: str = Field(
        description="Identified document type."
    )

    document_number: str | None = Field(
        default=None,
        description="Document or reference number.",
    )

    parties: str = Field(
        description=(
            "Short description of the organizations "
            "or people involved."
        )
    )

    key_points: list[str] = Field(
        default_factory=list,
        description=(
            "Most important points a user should know."
        ),
    )

    items_summary: str = Field(
        description=(
            "Short summary of products or services "
            "mentioned in the document."
        )
    )

    financial_summary: FinancialSummary = Field(
        description="Summary of financial information."
    )

    payment_terms: str | None = Field(
        default=None,
        description="Important payment terms.",
    )

    delivery_terms: str | None = Field(
        default=None,
        description="Important delivery terms.",
    )

    important_terms: list[str] = Field(
        default_factory=list,
        description=(
            "Important contractual or business terms."
        ),
    )

    warnings: list[str] = Field(
        default_factory=list,
        description=(
            "Potential issues, missing information, "
            "or items requiring attention."
        ),
    )

    validation_summary: str = Field(
        description=(
            "Explanation of the document validation result."
        )
    )

    recommendation: str = Field(
        description=(
            "Practical recommendation based only on "
            "the extracted document information."
        )
    )