from pathlib import Path

import fitz


class PDFParser:
    """
    Responsible only for extracting text from PDF files.
    """

    def extract_text(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        try:
            document = fitz.open(file_path)

            pages = []

            for page in document:
                text = page.get_text("text")

                if text.strip():
                    pages.append(text.strip())

            document.close()

            return "\n\n".join(pages)

        except Exception as exc:
            raise ValueError(
                f"Unable to extract text from PDF: {exc}"
            ) from exc

    def get_page_count(self, file_path: Path) -> int:
        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        try:
            document = fitz.open(file_path)
            page_count = len(document)
            document.close()

            return page_count

        except Exception as exc:
            raise ValueError(
                f"Unable to read PDF: {exc}"
            ) from exc


pdf_parser = PDFParser()