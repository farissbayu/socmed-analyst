# Social Media analysis
# -> User input a topic | DONE
# -> Extract information based on user topic | DONE
# -> Get the data (Scraping or Database)
#   -> SCRAPING | Scrape data -> ? -> save to db -> return data
#   -> DATABASE | Get the data
# -> Analyze the problem based on data provided
# -> Generate summmary or report
from app.analyze.method import extract_input
from app.analyze.schema import AnalyzeInput

from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from social media analyst"}


@app.post("/analyze")
def get_socmed_analysis(body: AnalyzeInput):
    result = extract_input(body.topic)
    return result


@app.get("/scalar")
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
