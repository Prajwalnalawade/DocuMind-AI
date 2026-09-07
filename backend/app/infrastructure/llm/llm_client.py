from openai import OpenAI

from app.core.config import settings


class LLMClient:
    """
    Infrastructure layer responsible for communicating
    with the configured LLM provider.

    The rest of the application does not directly
    communicate with the OpenAI SDK.
    """

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured. "
                "Add it to backend/.env."
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_MODEL

    def extract_structured_data(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model,
    ):
        """
        Send document text to the LLM and parse the
        response directly into the supplied Pydantic model.
        """

        try:
            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                text_format=response_model,
            )

            for output in response.output:

                if output.type != "message":
                    continue

                for content in output.content:

                    if content.type != "output_text":
                        continue

                    if content.parsed is None:
                        raise RuntimeError(
                            "The LLM returned no structured data."
                        )

                    return content.parsed

            raise RuntimeError(
                "The LLM response did not contain "
                "structured output."
            )

        except Exception as exc:
            raise RuntimeError(
                f"LLM structured extraction failed: {exc}"
            ) from exc


llm_client = LLMClient