from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables
    and the backend .env file.
    """

    APP_NAME: str = "DocuMind AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_PREFIX: str = "/api"

    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    ALLOWED_EXTENSIONS: str = ".pdf,.png,.jpg,.jpeg"

    # ---------------------------------------------------------
    # OCR
    # ---------------------------------------------------------

    TESSERACT_CMD: str = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    OCR_LANGUAGE: str = "eng"
    OCR_DPI: int = 200

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.6-luna"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()