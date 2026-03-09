from pydantic import BaseModel, Field


class AnalyzeInput(BaseModel):
    topic: str = Field(description="Topic to analyze")


class TimeFilter(BaseModel):
    filter: str | None = Field(
        description="Filtered time. Example: Februari 2026, 1 minggu terakhir"
    )
    start_date: str | None = Field(description="Start date if there is time filter")
    end_date: str | None = Field(description="End date if there is time filter")


class ExtractedInputSchema(BaseModel):
    topic: str = Field(description="Topic or problem wanted to solve")
    keywords: list[str] = Field(description="Keyword list for comments query")
    location: str | None = Field(
        description="Affected district if user input includes location"
    )
    time_filter: TimeFilter = Field(description="Time span user asked")


class Aspiration(BaseModel):
    valid_complaint: list[str] = Field(
        description="Valid complaint based on the topic and comments"
    )
    suggested_questions: list[str] = Field(
        description="Suggestion and question extracted from comments"
    )
    appreciation: list[str] = Field(description="Appreciation from comments")
    total_spam: int = Field(
        description="Removed comment that count as spam, oot or emoji only"
    )
