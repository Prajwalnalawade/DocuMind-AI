from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def get_upload_directory() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file_extension(filename: str) -> str:
    extension = get_file_extension(filename)

    allowed_extensions = {
        ext.strip().lower()
        for ext in settings.ALLOWED_EXTENSIONS.split(",")
    }

    if extension not in allowed_extensions:
        raise ValueError(
            f"Unsupported file type '{extension}'. "
            f"Allowed types: {', '.join(sorted(allowed_extensions))}"
        )

    return extension


def generate_document_id() -> str:
    return str(uuid4())


async def save_uploaded_file(
    file: UploadFile,
    document_id: str,
    extension: str,
) -> tuple[Path, int]:

    upload_dir = get_upload_directory()

    safe_filename = f"{document_id}{extension}"
    file_path = upload_dir / safe_filename

    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    total_size = 0

    with file_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            total_size += len(chunk)

            if total_size > max_size:
                file_path.unlink(missing_ok=True)

                raise ValueError(
                    f"File size exceeds the maximum limit of "
                    f"{settings.MAX_FILE_SIZE_MB} MB."
                )

            buffer.write(chunk)

    return file_path, total_size