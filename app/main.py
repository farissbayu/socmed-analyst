# Social Media analysis
# -> User input a topic | DONE
# -> Extract information based on user topic | DONE
# -> Get the data (Scraping or Database)
#   -> SCRAPING | Scrape data -> ? -> save to db -> return data
#   -> DATABASE | Get the data
# -> Analyze the problem based on data provided
# -> Generate summmary or report
from sqlmodel import Session
from app.models.engine import get_db
from app.analyze.method import (
    extract_input,
    get_safe_timeframe,
    determine_data_source,
    get_from_database,
    get_target_accounts,
    scrape_tiktok_videos,
)
from app.analyze.schema import AnalyzeInput

from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from social media analyst"}


@app.post("/analyze")
def get_socmed_analysis(body: AnalyzeInput, db: Session = Depends(get_db)):
    extracted_input = extract_input(body.topic)
    print(extracted_input)

    safe_timeframe = get_safe_timeframe(extracted_input.time_filter)
    print(safe_timeframe)

    data_source = determine_data_source(db, safe_timeframe[1])
    print(data_source)

    data = []
    if data_source == "scraping":
        pass
    # PENDING | BUDGET RELATED REASON
    # elif data_source == "scraping newest":
    #     target_accounts = get_target_accounts(db)
    #     videos_result = scrape_tiktok_videos(
    #         target_accounts, safe_timeframe[0], safe_timeframe[1]
    #     )
    #     data = videos_result
    elif data_source == "database only":
        data = get_from_database(db, safe_timeframe[0], safe_timeframe[1])

    return data


@app.get("/scalar")
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
