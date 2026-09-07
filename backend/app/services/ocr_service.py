from pathlib import Path

import fitz
import pytesseract
from PIL import Image

from app.core.config import settings


class OCRService:
    """
    Handles Optical Character Recognition (OCR).

    This service is responsible for:
    - Converting PDF pages into images
    - Running Tesseract OCR
    - Combining OCR text from multiple pages
    """

    def __init__(self):
        self.tesseract_cmd = settings.TESSERACT_CMD
        self.language = settings.OCR_LANGUAGE
        self.dpi = settings.OCR_DPI

        pytesseract.pytesseract.tesseract_cmd = (
            self.tesseract_cmd
        )

    def verify_tesseract(self) -> bool:
        """
        Verify that the Tesseract OCR engine is available.
        """

        tesseract_path = Path(self.tesseract_cmd)

        if not tesseract_path.exists():
            return False

        try:
            pytesseract.get_tesseract_version()
            return True

        except Exception:
            return False

    def extract_text_from_image(
        self,
        image: Image.Image,
    ) -> str:
        """
        Extract text from a PIL image using Tesseract.
        """

        try:
            text = pytesseract.image_to_string(
                image,
                lang=self.language,
            )

            return text.strip()

        except Exception as exc:
            raise RuntimeError(
                f"OCR failed while processing image: {exc}"
            ) from exc

    def extract_text_from_pdf(
        self,
        file_path: Path,
    ) -> dict:
        """
        Convert each PDF page to an image and perform OCR.
        """

        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if not self.verify_tesseract():
            raise RuntimeError(
                "Tesseract OCR engine was not found. "
                f"Expected executable at: {self.tesseract_cmd}"
            )

        document = None

        try:
            document = fitz.open(file_path)

            pages_text = []

            zoom = self.dpi / 72

            matrix = fitz.Matrix(
                zoom,
                zoom,
            )

            for page_number, page in enumerate(
                document,
                start=1,
            ):
                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False,
                )

                image = Image.frombytes(
                    "RGB",
                    [
                        pixmap.width,
                        pixmap.height,
                    ],
                    pixmap.samples,
                )

                text = self.extract_text_from_image(
                    image
                )

                if text:
                    pages_text.append(
                        f"[Page {page_number}]\n{text}"
                    )

            combined_text = "\n\n".join(
                pages_text
            )

            return {
                "text": combined_text,
                "page_count": len(document),
                "character_count": len(combined_text),
                "has_text": bool(
                    combined_text.strip()
                ),
                "extraction_method": "ocr",
            }

        except RuntimeError:
            raise

        except Exception as exc:
            raise RuntimeError(
                f"Unable to perform OCR on PDF: {exc}"
            ) from exc

        finally:
            if document is not None:
                document.close()


ocr_service = OCRService()