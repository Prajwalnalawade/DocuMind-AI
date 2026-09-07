from datetime import date

from app.schemas.extraction_schema import (
    DocumentExtraction,
)
from app.schemas.validation_schema import (
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class ValidationService:
    """
    Validates structured information extracted from
    business documents.

    Validation categories:

    - Required information
    - Line-item calculations
    - Subtotal calculations
    - Tax calculations
    - Final total calculations
    - Numeric sanity checks
    - Date consistency
    """

    MONEY_TOLERANCE = 0.05
    CALCULATION_TOLERANCE = 0.05

    ERROR_PENALTY = 30
    WARNING_PENALTY = 10

    def validate_document(
        self,
        document: DocumentExtraction,
    ) -> ValidationResult:
        """
        Validate a structured document.

        Warnings indicate incomplete or questionable
        information but do not make the document invalid.

        Errors indicate a failed business-rule check.
        """

        issues: list[ValidationIssue] = []

        checks = 0
        passed_checks = 0

        # =====================================================
        # REQUIRED INFORMATION
        # =====================================================

        checks += 1

        if document.document_type:
            passed_checks += 1
        else:
            issues.append(
                ValidationIssue(
                    code="MISSING_DOCUMENT_TYPE",
                    severity=ValidationSeverity.ERROR,
                    field="document_type",
                    message=(
                        "The document type could not be identified."
                    ),
                )
            )

        # =====================================================
        # DOCUMENT NUMBER
        # =====================================================

        checks += 1

        if document.document_number:
            passed_checks += 1
        else:
            issues.append(
                ValidationIssue(
                    code="MISSING_DOCUMENT_NUMBER",
                    severity=ValidationSeverity.WARNING,
                    field="document_number",
                    message=(
                        "No document number was found."
                    ),
                )
            )

        # =====================================================
        # FINANCIAL VALIDATION
        # =====================================================

        (
            financial_checks,
            financial_passes,
            financial_issues,
        ) = self._validate_financials(document)

        checks += financial_checks
        passed_checks += financial_passes
        issues.extend(financial_issues)

        # =====================================================
        # LINE ITEM VALIDATION
        # =====================================================

        (
            item_checks,
            item_passes,
            item_issues,
        ) = self._validate_line_items(document)

        checks += item_checks
        passed_checks += item_passes
        issues.extend(item_issues)

        # =====================================================
        # DATE VALIDATION
        # =====================================================

        (
            date_checks,
            date_passes,
            date_issues,
        ) = self._validate_dates(document)

        checks += date_checks
        passed_checks += date_passes
        issues.extend(date_issues)

        # =====================================================
        # NUMERIC SANITY
        # =====================================================

        (
            numeric_checks,
            numeric_passes,
            numeric_issues,
        ) = self._validate_numeric_values(document)

        checks += numeric_checks
        passed_checks += numeric_passes
        issues.extend(numeric_issues)

        # =====================================================
        # COUNT FINDINGS
        # =====================================================

        error_count = sum(
            1
            for issue in issues
            if issue.severity == ValidationSeverity.ERROR
        )

        warning_count = sum(
            1
            for issue in issues
            if issue.severity == ValidationSeverity.WARNING
        )

        # INFO findings do not affect validation status
        # or validation score.

        failed_checks = (
            error_count
            + warning_count
        )

        # =====================================================
        # VALIDATION SCORE
        # =====================================================

        score = (
            100
            - (error_count * self.ERROR_PENALTY)
            - (warning_count * self.WARNING_PENALTY)
        )

        score = round(
            max(0.0, min(100.0, score)),
            2,
        )

        # =====================================================
        # VALIDATION STATUS
        # =====================================================

        if error_count > 0:

            status = ValidationStatus.INVALID

            is_valid = False

            summary = (
                "Document validation found one or more "
                "critical errors that require attention."
            )

        elif warning_count > 0:

            status = ValidationStatus.VALID_WITH_WARNINGS

            is_valid = True

            summary = (
                "Document validation completed with warnings. "
                "No critical validation errors were found."
            )

        else:

            status = ValidationStatus.VALID

            is_valid = True

            summary = (
                "Document validation completed successfully. "
                "No errors or warnings were found."
            )

        # =====================================================
        # RETURN RESULT
        # =====================================================

        return ValidationResult(
            status=status,
            is_valid=is_valid,
            score=score,
            total_checks=checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            error_count=error_count,
            warning_count=warning_count,
            issues=issues,
            summary=summary,
        )

    # =========================================================
    # FINANCIAL VALIDATION
    # =========================================================

    def _validate_financials(
        self,
        document: DocumentExtraction,
    ):
        checks = 0
        passed = 0
        issues: list[ValidationIssue] = []

        totals = document.totals

        subtotal = totals.subtotal
        discount = totals.discount
        tax = totals.tax
        shipping = totals.shipping
        total = totals.total

        # -----------------------------------------------------
        # SUBTOTAL VS LINE ITEMS
        # -----------------------------------------------------

        if subtotal is not None:

            item_amounts = [
                item.amount
                for item in document.items
                if item.amount is not None
            ]

            if item_amounts:

                checks += 1

                calculated_subtotal = sum(
                    item_amounts
                )

                difference = round(
                    calculated_subtotal - subtotal,
                    2,
                )

                if abs(difference) <= self.MONEY_TOLERANCE:

                    passed += 1

                else:

                    issues.append(
                        ValidationIssue(
                            code="SUBTOTAL_MISMATCH",
                            severity=ValidationSeverity.ERROR,
                            field="totals.subtotal",
                            message=(
                                "The subtotal does not match "
                                "the sum of the line-item amounts."
                            ),
                            expected=round(
                                calculated_subtotal,
                                2,
                            ),
                            actual=subtotal,
                            difference=difference,
                        )
                    )

        # -----------------------------------------------------
        # FINAL TOTAL
        # -----------------------------------------------------

        if total is not None and subtotal is not None:

            checks += 1

            discount_value = (
                discount
                if discount is not None
                else 0.0
            )

            tax_value = (
                tax
                if tax is not None
                else 0.0
            )

            shipping_value = (
                shipping
                if shipping is not None
                else 0.0
            )

            expected_total = (
                subtotal
                - discount_value
                + tax_value
                + shipping_value
            )

            difference = round(
                expected_total - total,
                2,
            )

            if abs(difference) <= self.MONEY_TOLERANCE:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="TOTAL_MISMATCH",
                        severity=ValidationSeverity.ERROR,
                        field="totals.total",
                        message=(
                            "The final total does not match "
                            "the subtotal, discount, tax "
                            "and shipping calculation."
                        ),
                        expected=round(
                            expected_total,
                            2,
                        ),
                        actual=total,
                        difference=difference,
                    )
                )

        # -----------------------------------------------------
        # TAX INFORMATION
        # -----------------------------------------------------

        if total is not None and subtotal is not None:

            checks += 1

            if tax is not None:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="MISSING_TAX_INFORMATION",
                        severity=ValidationSeverity.WARNING,
                        field="totals.tax",
                        message=(
                            "Tax information was not explicitly "
                            "identified in the document."
                        ),
                    )
                )

        return (
            checks,
            passed,
            issues,
        )

    # =========================================================
    # LINE ITEM VALIDATION
    # =========================================================

    def _validate_line_items(
        self,
        document: DocumentExtraction,
    ):
        checks = 0
        passed = 0
        issues: list[ValidationIssue] = []

        for index, item in enumerate(
            document.items,
            start=1,
        ):

            # -------------------------------------------------
            # QUANTITY × UNIT PRICE = AMOUNT
            # -------------------------------------------------

            if (
                item.quantity is not None
                and item.unit_price is not None
                and item.amount is not None
            ):

                checks += 1

                expected_amount = (
                    item.quantity
                    * item.unit_price
                )

                difference = round(
                    expected_amount - item.amount,
                    2,
                )

                if abs(
                    difference
                ) <= self.CALCULATION_TOLERANCE:

                    passed += 1

                else:

                    issues.append(
                        ValidationIssue(
                            code="LINE_ITEM_AMOUNT_MISMATCH",
                            severity=ValidationSeverity.ERROR,
                            field=f"items[{index}].amount",
                            message=(
                                "The line-item amount does not "
                                "match quantity multiplied "
                                "by unit price."
                            ),
                            expected=round(
                                expected_amount,
                                2,
                            ),
                            actual=item.amount,
                            difference=difference,
                        )
                    )

            # -------------------------------------------------
            # LINE ITEM DESCRIPTION
            # -------------------------------------------------

            checks += 1

            if item.description:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="MISSING_ITEM_DESCRIPTION",
                        severity=ValidationSeverity.WARNING,
                        field=f"items[{index}].description",
                        message=(
                            "A line item does not contain "
                            "a description."
                        ),
                    )
                )

        return (
            checks,
            passed,
            issues,
        )

    # =========================================================
    # DATE VALIDATION
    # =========================================================

    def _validate_dates(
        self,
        document: DocumentExtraction,
    ):
        checks = 0
        passed = 0
        issues: list[ValidationIssue] = []

        document_date = self._parse_date(
            document.document_date
        )

        due_date = self._parse_date(
            document.due_date
        )

        valid_until = self._parse_date(
            document.valid_until
        )

        # -----------------------------------------------------
        # DOCUMENT DATE → DUE DATE
        # -----------------------------------------------------

        if document_date and due_date:

            checks += 1

            if due_date >= document_date:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="INVALID_DUE_DATE",
                        severity=ValidationSeverity.ERROR,
                        field="due_date",
                        message=(
                            "The due date occurs before "
                            "the document date."
                        ),
                        expected=(
                            document_date.isoformat()
                        ),
                        actual=(
                            due_date.isoformat()
                        ),
                    )
                )

        # -----------------------------------------------------
        # DOCUMENT DATE → VALID UNTIL
        # -----------------------------------------------------

        if document_date and valid_until:

            checks += 1

            if valid_until >= document_date:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="INVALID_VALID_UNTIL",
                        severity=ValidationSeverity.ERROR,
                        field="valid_until",
                        message=(
                            "The validity date occurs before "
                            "the document date."
                        ),
                        expected=(
                            document_date.isoformat()
                        ),
                        actual=(
                            valid_until.isoformat()
                        ),
                    )
                )

        return (
            checks,
            passed,
            issues,
        )

    # =========================================================
    # NUMERIC VALIDATION
    # =========================================================

    def _validate_numeric_values(
        self,
        document: DocumentExtraction,
    ):
        checks = 0
        passed = 0
        issues: list[ValidationIssue] = []

        totals = document.totals

        numeric_fields = {
            "totals.subtotal": totals.subtotal,
            "totals.discount": totals.discount,
            "totals.tax": totals.tax,
            "totals.shipping": totals.shipping,
            "totals.total": totals.total,
        }

        for field_name, value in numeric_fields.items():

            if value is None:
                continue

            checks += 1

            if value >= 0:

                passed += 1

            else:

                issues.append(
                    ValidationIssue(
                        code="NEGATIVE_FINANCIAL_VALUE",
                        severity=ValidationSeverity.ERROR,
                        field=field_name,
                        message=(
                            "A financial value cannot be negative."
                        ),
                        actual=value,
                    )
                )

        for index, item in enumerate(
            document.items,
            start=1,
        ):

            if item.quantity is not None:

                checks += 1

                if item.quantity > 0:

                    passed += 1

                else:

                    issues.append(
                        ValidationIssue(
                            code="INVALID_QUANTITY",
                            severity=ValidationSeverity.ERROR,
                            field=f"items[{index}].quantity",
                            message=(
                                "Line-item quantity must be "
                                "greater than zero."
                            ),
                            actual=item.quantity,
                        )
                    )

            if item.unit_price is not None:

                checks += 1

                if item.unit_price >= 0:

                    passed += 1

                else:

                    issues.append(
                        ValidationIssue(
                            code="NEGATIVE_UNIT_PRICE",
                            severity=ValidationSeverity.ERROR,
                            field=f"items[{index}].unit_price",
                            message=(
                                "Unit price cannot be negative."
                            ),
                            actual=item.unit_price,
                        )
                    )

            if item.amount is not None:

                checks += 1

                if item.amount >= 0:

                    passed += 1

                else:

                    issues.append(
                        ValidationIssue(
                            code="NEGATIVE_ITEM_AMOUNT",
                            severity=ValidationSeverity.ERROR,
                            field=f"items[{index}].amount",
                            message=(
                                "Line-item amount cannot "
                                "be negative."
                            ),
                            actual=item.amount,
                        )
                    )

        return (
            checks,
            passed,
            issues,
        )

    # =========================================================
    # DATE PARSER
    # =========================================================

    @staticmethod
    def _parse_date(
        value: str | None,
    ) -> date | None:
        """
        Parse standard ISO date values.

        Non-date expressions such as:
        '24 hours from generation'
        are intentionally ignored.
        """

        if not value:
            return None

        try:

            return date.fromisoformat(
                value.strip()
            )

        except (ValueError, TypeError):

            return None


validation_service = ValidationService()