from feature_achievement.db.engine import init_db
import feature_achievement.db.models  # noqa:F401

if __name__ == "__main__":
    init_db()
    print("DB initialized successfully")
