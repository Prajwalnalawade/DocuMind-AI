from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """
    Supported business document categories.
    """

    INVOICE = "invoice"
    QUOTATION = "quotation"
    RECEIPT = "receipt"
    CONTRACT = "contract"
    OTHER = "other"


class Party(BaseModel):
    """
    Represents a company, vendor, customer,
    client, supplier or other document party.
    """

    name: str | None = None
    address: str | None = None
    email: str | None = None
    phone: str | None = None
    tax_id: str | None = None


class LineItem(BaseModel):
    """
    Represents an individual item/service
    found inside an invoice or quotation.
    """

    description: str | None = None
    quantity: float | None = None
    unit: str | None = None
    unit_price: float | None = None
    tax_rate: float | None = None
    amount: float | None = None


class FinancialTotals(BaseModel):
    """
    Financial summary extracted from a document.
    """

    subtotal: float | None = None
    discount: float | None = None
    tax: float | None = None
    shipping: float | None = None
    total: float | None = None
    currency: str | None = None


class DocumentExtraction(BaseModel):
    """
    Structured representation of information
    extracted from a business document.
    """

    document_type: DocumentType = Field(
        description="The type of document."
    )

    document_title: str | None = Field(
        default=None,
        description="Title of the document if available.",
    )

    document_number: str | None = Field(
        default=None,
        description=(
            "Invoice number, quotation number, "
            "receipt number, contract number, etc."
        ),
    )

    document_date: str | None = Field(
        default=None,
        description="Main date appearing on the document.",
    )

    due_date: str | None = Field(
        default=None,
        description="Payment due date if available.",
    )

    valid_until: str | None = Field(
        default=None,
        description=(
            "Validity or expiry date of the quotation "
            "or document if available."
        ),
    )

    vendor: Party | None = Field(
        default=None,
        description="Vendor, supplier or issuing organization.",
    )

    customer: Party | None = Field(
        default=None,
        description="Customer, client or receiving organization.",
    )

    items: list[LineItem] = Field(
        default_factory=list,
        description="Products or services listed in the document.",
    )

    totals: FinancialTotals = Field(
        default_factory=FinancialTotals,
        description="Financial totals found in the document.",
    )

    payment_terms: str | None = Field(
        default=None,
        description="Payment terms mentioned in the document.",
    )

    delivery_terms: str | None = Field(
        default=None,
        description="Delivery terms mentioned in the document.",
    )

    contract_terms: list[str] = Field(
        default_factory=list,
        description="Important contractual terms or conditions.",
    )

    notes: list[str] = Field(
        default_factory=list,
        description="Important additional notes.",
    )

    confidence_notes: list[str] = Field(
        default_factory=list,
        description=(
            "Notes about uncertain, missing or ambiguous "
            "information in the source document."
        ),
    )