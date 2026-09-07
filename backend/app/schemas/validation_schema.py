from enum import Enum

from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    """
    Severity level of a validation finding.
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationStatus(str, Enum):
    """
    Overall document validation status.
    """

    VALID = "valid"
    VALID_WITH_WARNINGS = "valid_with_warnings"
    INVALID = "invalid"


class ValidationIssue(BaseModel):
    """
    Represents one validation finding.
    """

    code: str = Field(
        description="Unique validation rule code."
    )

    severity: ValidationSeverity = Field(
        description="Severity of the validation finding."
    )

    field: str | None = Field(
        default=None,
        description="Field related to the validation finding.",
    )

    message: str = Field(
        description="Human-readable explanation of the finding."
    )

    expected: float | str | None = Field(
        default=None,
        description="Expected value when applicable.",
    )

    actual: float | str | None = Field(
        default=None,
        description="Actual value found in the document.",
    )

    difference: float | None = Field(
        default=None,
        description="Difference between expected and actual values.",
    )


class ValidationResult(BaseModel):
    """
    Complete validation result for a document.
    """

    status: ValidationStatus = Field(
        description="Overall validation status."
    )

    is_valid: bool = Field(
        description=(
            "True when there are no critical validation errors."
        )
    )

    score: float = Field(
        ge=0,
        le=100,
        description="Validation score from 0 to 100.",
    )

    total_checks: int = Field(
        ge=0,
        description="Number of validation checks performed.",
    )

    passed_checks: int = Field(
        ge=0,
        description="Number of validation checks that passed.",
    )

    failed_checks: int = Field(
        ge=0,
        description=(
            "Number of validation checks that failed "
            "because of an error or warning."
        ),
    )

    error_count: int = Field(
        ge=0,
        description="Number of critical validation errors.",
    )

    warning_count: int = Field(
        ge=0,
        description="Number of validation warnings.",
    )

    issues: list[ValidationIssue] = Field(
        default_factory=list,
        description="Validation findings.",
    )

    summary: str = Field(
        description="Human-readable validation summary."
    )