from app.core.settings import settings
from apify_client import ApifyClient

client = ApifyClient(settings.APIFY_API_KEY)

apify_get_videos = client.actor(settings.APIFY_TIKTOK_ACTOR)
