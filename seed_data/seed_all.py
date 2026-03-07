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
    """
    Comprehensive function to seed all required data.

    This function calls the individual seeder functions:
    1. seed_from_sql_files() - Seeds wilayah data (Kecamatan & Desa)
    2. seed_user_from_json() - Extracts and seeds unique users
    3. seed_videos_from_json() - Extracts and seeds videos filtered by date
    4. seed_comments_from_json() - Extracts and seeds comments

    Args:
        user_videos_filepath: Path to user_videos.json
        videos_filepath: Path to videos.json
        min_date_str: Minimum date filter (YYYY-MM-DD format)

    Returns:
        dict: Summary of seeding results with counts and statistics
    """

    print("=" * 100)
    print("🌱 SEED ALL DATA - Starting process...")
    print("=" * 100)

    try:
        # =====================================================
        # STEP 1: Seed Wilayah Data
        # =====================================================
        print("\n📝 STEP 1: Seeding Wilayah (Kecamatan & Desa)...")
        print("-" * 100)
        try:
            seed_from_sql_files()
        except Exception as e:
            print(f"❌ Error seeding wilayah: {str(e)}")
        print()

        # =====================================================
        # STEP 2: Seed OPD (Organisasi Perangkat Daerah)
        # =====================================================
        print("📝 STEP 2: Seeding OPD (Organisasi Perangkat Daerah)...")
        print("-" * 100)
        try:
            opd_list = seed_opd_from_json(filepath="seed_data/opd.json")
            opd_count = len(opd_list) if opd_list else 0
            if opd_count == 0:
                print("⚠️  Warning: No OPD records extracted or seeded!")
        except Exception as e:
            print(f"❌ Error seeding OPD: {str(e)}")
            opd_list = []
            opd_count = 0
        print()

        # =====================================================
        # STEP 3: Seed Users
        # =====================================================
        print("📝 STEP 3: Seeding Users...")
        print("-" * 100)
        try:
            users_extracted = seed_user_from_json(filepath=user_videos_filepath)
            users_count = len(users_extracted) if users_extracted else 0
            if users_count == 0:
                print("⚠️  Warning: No users extracted or seeded!")
        except Exception as e:
            print(f"❌ Error seeding users: {str(e)}")
            users_extracted = []
            users_count = 0
        print()

        # =====================================================
        # STEP 4: Seed Videos
        # =====================================================
        print("📝 STEP 4: Seeding Videos (with date filter)...")
        print("-" * 100)
        try:
            videos_list, total_comments = seed_videos_from_json(
                filepath=videos_filepath, min_date_str=min_date_str
            )
            videos_count = len(videos_list) if videos_list else 0
            if videos_count == 0:
                print("⚠️  Warning: No videos extracted or seeded!")
        except Exception as e:
            print(f"❌ Error seeding videos: {str(e)}")
            videos_list = []
            total_comments = 0
            videos_count = 0
        print()

        # =====================================================
        # STEP 5: Seed Comments
        # =====================================================
        print("📝 STEP 5: Seeding Comments...")
        print("-" * 100)
        try:
            comments_list = seed_comments_from_json(filepath="seed_data/comments.json")
            comments_count = len(comments_list) if comments_list else 0
            if comments_count == 0:
                print("⚠️  Warning: No comments extracted or seeded!")
        except Exception as e:
            print(f"❌ Error seeding comments: {str(e)}")
            comments_list = []
            comments_count = 0
        print()

        # =====================================================
        # Summary
        # =====================================================
        results = {
            "status": "success",
            "opd_seeded": opd_count,
            "users_seeded": users_count,
            "videos_seeded": videos_count,
            "comments_seeded": comments_count,
            "total_comments": total_comments,
            "min_date_filter": min_date_str,
            "timestamp": datetime.now().isoformat(),
        }

        print("=" * 100)
        print("✅ SEED COMPLETE - Summary:")
        print("=" * 100)
        print(f"🏢 OPD seeded: {results['opd_seeded']}")
        print(f"👥 Users seeded: {results['users_seeded']}")
        print(f"🎬 Videos seeded: {results['videos_seeded']}")
        print(f"💬 Comments seeded: {results['comments_seeded']}")
        print(f"📊 Total comments (from videos): {results['total_comments']}")
        print(f"📅 Date filter applied: {min_date_str} onwards")
        print("=" * 100 + "\n")

        return results

    except FileNotFoundError as e:
        print(f"❌ File not found: {str(e)}")
        return {
            "status": "error",
            "error": f"File not found: {str(e)}",
        }
    except Exception as e:
        print(f"❌ Error: {str(e)}")
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
