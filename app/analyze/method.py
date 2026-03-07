from app.analyze.prompt import INPUT_EXTRACTION_PROMPT
from datetime import datetime
from app.utils.openai import oa_client
from app.models.database import TikTokUser
from sqlmodel import Session, select
from app.analyze.schema import ExtractedInputSchema


def get_target_accounts(db: Session):
    stmt = select(TikTokUser).where(TikTokUser.is_priority)
    result = db.exec(stmt)
    return result.all()


def extract_input(topic: str) -> ExtractedInputSchema:
    datenow = datetime.today()
    response = oa_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": INPUT_EXTRACTION_PROMPT.format(datenow=datenow),
            },
            {"role": "user", "content": f"Topic: {topic}"},
        ],
        response_format=ExtractedInputSchema,
    )

    if not response:
        raise ValueError("No response provided")

    parsed_data = response.choices[0].message.parsed.model_dump()  # type: ignore
    return ExtractedInputSchema(**parsed_data)
