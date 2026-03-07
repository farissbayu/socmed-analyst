# Social Media analysis
# -> User input a topic
# -> Extract information based on user topic
# -> Get the data (Scraping or Database)
#   -> SCRAPING | Scrape data -> ? -> save to db -> return data
#   -> DATABASE | Get the data
# -> Analyze the problem based on data provided
# -> Generate summmary or report
from scalar_fastapi import get_scalar_api_reference

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from social media analyst"}


@app.get("/scalar")
def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
