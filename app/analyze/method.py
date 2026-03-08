from app.utils.apify_client import apify_get_videos
from app.analyze.prompt import INPUT_EXTRACTION_PROMPT
from datetime import datetime, timedelta
from app.utils.openai import oa_client
from app.models.database import TikTokUser, TikTokComment, TikTokVideo
from sqlmodel import Session, select, desc
from app.analyze.schema import ExtractedInputSchema, TimeFilter

date_format = "%Y-%m-%d"


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


def get_safe_timeframe(timeframe: TimeFilter) -> tuple[str, str]:
    start_date = timeframe.start_date
    end_date = timeframe.end_date

    # if timeframe is null, fallback to 1 month
    if not start_date or not end_date:
        today = datetime.today()
        thirty_days_ago = today - timedelta(days=30)

        safe_end_date = today.strftime(date_format)
        safe_start_date = thirty_days_ago.strftime(date_format)

        return safe_start_date, safe_end_date

    return start_date, end_date


def get_latest_comment_date(db: Session) -> str | None:
    stmt = select(TikTokComment).order_by(desc(TikTokComment.create_time_iso))
    latest_comment = db.exec(stmt).first()

    if latest_comment and latest_comment.create_time_iso:
        return latest_comment.create_time_iso.strftime(date_format)

    return None


def get_latest_uploaded_video_date(db: Session) -> str | None:
    stmt = select(TikTokVideo).order_by(desc(TikTokVideo.video_created_at))
    latest_video = db.exec(stmt).first()

    if latest_video and latest_video.video_created_at:
        return latest_video.video_created_at.strftime(date_format)

    return None


def determine_data_source(db: Session, requested_end_date: str) -> str:
    latest_comment_date = get_latest_comment_date(db)

    # empty database
    if not latest_comment_date:
        return "scraping"

    db_date = datetime.strptime(latest_comment_date, date_format).date()
    req_end_date = datetime.strptime(requested_end_date, date_format).date()

    print(f"DB Date: {db_date} | Req end date: {req_end_date}")

    # PENDING | BUDGET RELATED REASON
    # there is data on db
    # but need to scrape for current user input needs
    # if req_end_date > db_date:
    #     return "scraping newest"

    # data are ready on db
    return "database only"


def get_from_database(db: Session, requested_start_date: str, requested_end_date: str):
    start_dt = datetime.strptime(requested_start_date, date_format)
    end_dt = datetime.strptime(requested_end_date, date_format).replace(
        hour=23, minute=59, second=59
    )

    print(f"Start date: {start_dt} | End date: {end_dt}")

    stmt = (
        select(TikTokComment.text)
        .where(
            TikTokComment.create_time_iso >= start_dt,
            TikTokComment.create_time_iso <= end_dt,
        )
        .limit(200)
    )
    data_from_db = db.exec(stmt)

    return data_from_db.all()


def scrape_tiktok_videos(
    tiktok_accounts: list[str], req_start_date: str, req_end_date: str
):
    run_input = {
        "commentsPerPost": 0,
        "excludePinnedPosts": True,
        "maxFollowersPerProfile": 0,
        "maxFollowingPerProfile": 0,
        "maxRepliesPerComment": 0,
        "maxPostsPerProfile": 1,
        "newestPostDate": req_end_date,
        "oldestPostDateUnified": req_start_date,
        "profileScrapeSections": ["videos"],
        "profileSorting": "latest",
        "profiles": tiktok_accounts,
        "proxyCountryCode": "None",
        "resultsPerPage": 1,
        "scrapeRelatedVideos": False,
        "shouldDownloadAvatars": False,
        "shouldDownloadCovers": False,
        "shouldDownloadMusicCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadVideos": False,
    }

    result = apify_get_videos.call(run_input=run_input)
    return result
