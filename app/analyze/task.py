from app.models.engine import engine
from app.celery_app import celery_app
from sqlmodel import Session
import datetime
from markdown import markdown
from weasyprint import HTML

from app.analyze.method import (
    extract_input,
    get_safe_timeframe,
    get_from_database,
    extract_core_issue,
    generate_executive_summary,
)


def analyze(topic: str, db: Session):
    extracted_input = extract_input(topic)
    topic = extracted_input.topic
    keywords = extracted_input.keywords

    print(extracted_input)
    safe_timeframe = get_safe_timeframe(extracted_input.time_filter)

    # data_source = determine_data_source(db, safe_timeframe[1])

    data = []

    # PENDING | BUDGET RELATED REASON
    # if data_source == "scraping":
    #     pass
    # elif data_source == "scraping newest":
    #     target_accounts = get_target_accounts(db)
    #     videos_result = scrape_tiktok_videos(
    #         target_accounts, safe_timeframe[0], safe_timeframe[1]
    #     )
    #     data = videos_result
    # elif data_source == "database only":
    #     data = get_from_database(db, safe_timeframe[0], safe_timeframe[1])

    data = get_from_database(db, keywords, safe_timeframe[0], safe_timeframe[1])

    if len(data) == 0:
        return {
            "message": "Gagal mendapatkan data atau tidak ada data dalam rentang yang diminta."
        }

    core_issue = extract_core_issue(topic, data)

    executive_summary = generate_executive_summary(core_issue)

    result = markdown(text=executive_summary, output_format="html")
    filename = f"Executive_summary_{datetime.datetime.now()}.pdf"
    HTML(string=result).write_pdf(filename)


@celery_app.task
def analyze_task(topic: str):
    with Session(engine) as db:
        analyze(topic, db)
