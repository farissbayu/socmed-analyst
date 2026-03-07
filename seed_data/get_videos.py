import json
from datetime import datetime


def get_videos_config(
    filepath="seed_data/videos.json",
    min_date=None,
    comments_per_post=500,
    max_replies_per_comment=100,
    results_per_page=100,
    exclude_pinned_posts=False,
):
    """
    Get videos from videos.json filtered by release date and return as config JSON.
    Filters videos from 1 January 2026 onwards.

    Args:
        filepath: Path to videos.json
        min_date: Minimum date as datetime object (default: 2026-01-01)
        comments_per_post: Number of comments per post (default: 500)
        max_replies_per_comment: Max replies per comment (default: 100)
        results_per_page: Results per page (default: 100)
        exclude_pinned_posts: Whether to exclude pinned posts (default: False)

    Returns:
        dict: Configuration JSON with filtered video URLs and settings
    """

    if min_date is None:
        min_date = datetime(2026, 1, 1)

    post_urls = []
    total_comments = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📊 Total video dalam JSON: {len(data)}")
        print(
            f"🎯 Filter: Video dengan release date >= {min_date.strftime('%Y-%m-%d')}\n"
        )

        for item in data:
            # Extract and parse date from createTimeISO field
            date_str = item.get("createTimeISO")

            if date_str:
                try:
                    # Parse ISO 8601 format (e.g., "2026-03-07T02:52:58.000Z")
                    video_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

                    # Filter by date - only include videos from 2026-01-01 onwards
                    if video_date.date() >= min_date.date():
                        # Extract video URL
                        video_url = item.get("webVideoUrl")
                        if video_url:
                            post_urls.append(video_url)
                            # Sum comments from commentCount field
                            comment_count = item.get("commentCount", 0)
                            if isinstance(comment_count, int):
                                total_comments += comment_count
                except (ValueError, AttributeError):
                    # If date parsing fails, skip this item
                    pass

        print(f"✅ Total video setelah filter: {len(post_urls)}")
        print(f"💬 Total comments dari semua video yang difilter: {total_comments}\n")

        # Create config JSON
        config = {
            "commentsPerPost": comments_per_post,
            "excludePinnedPosts": exclude_pinned_posts,
            "maxRepliesPerComment": max_replies_per_comment,
            "postURLs": post_urls,
            "resultsPerPage": results_per_page,
        }

        # Display filtered videos
        if post_urls:
            print("📹 Daftar Video (dari 1 Januari 2026):")
            print("-" * 100)
            for i, url in enumerate(post_urls, 1):
                print(f"{i}. {url}")
            print("-" * 100)
        else:
            print("⚠️  Tidak ada video dengan date >= 2026-01-01")

        return config, total_comments

    except FileNotFoundError:
        print(f"❌ File {filepath} tidak ditemukan!")
        return {}, 0
    except json.JSONDecodeError:
        print("❌ Format JSON tidak valid. Pastikan formatnya array [...]")
        return {}, 0


if __name__ == "__main__":
    config, total_comments = get_videos_config(filepath="seed_data/videos.json")

    # Print the config as formatted JSON
    print("\n📋 Output JSON Configuration:")
    print(json.dumps(config, indent=4))
