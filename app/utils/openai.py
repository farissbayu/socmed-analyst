from app.core.settings import settings
from openai import OpenAI

oa_client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY, base_url=settings.OPENROUTER_BASE_URL
)
