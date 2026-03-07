from datetime import datetime
from seed_data.seed_user import seed_user_from_json
from seed_data.seed_videos import seed_videos_from_json
from seed_data.seed_wilayah import seed_from_sql_files
from seed_data.seed_comments import seed_comments_from_json
from seed_data.seed_opd import seed_opd_from_json


def seed_all_data(
    user_videos_filepath="seed_data/user_videos.json",
    videos_filepath="seed_data/videos.json",
    min_date_str="2026-01-01",
):
    try:
        seed_from_sql_files()

        opd_list = seed_opd_from_json(filepath="seed_data/opd.json")
        opd_count = len(opd_list) if opd_list else 0

        users_extracted = seed_user_from_json(filepath=user_videos_filepath)
        users_count = len(users_extracted) if users_extracted else 0

        videos_list, total_comments = seed_videos_from_json(
            filepath=videos_filepath, min_date_str=min_date_str
        )
        videos_count = len(videos_list) if videos_list else 0

        comments_list = seed_comments_from_json(filepath="seed_data/comments.json")
        comments_count = len(comments_list) if comments_list else 0

        return {
            "status": "success",
            "opd_seeded": opd_count,
            "users_seeded": users_count,
            "videos_seeded": videos_count,
            "comments_seeded": comments_count,
            "total_comments": total_comments,
            "min_date_filter": min_date_str,
            "timestamp": datetime.now().isoformat(),
        }

    except FileNotFoundError as e:
        return {
            "status": "error",
            "error": f"File not found: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


if __name__ == "__main__":
    results = seed_all_data(
        user_videos_filepath="seed_data/user_videos.json",
        videos_filepath="seed_data/videos.json",
        min_date_str="2026-01-01",
    )
