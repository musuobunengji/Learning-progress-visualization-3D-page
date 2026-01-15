from fastapi import FastAPI
from feature_achievement.api.routers import edges

app = FastAPI(title="ChapterGraph API")
app.include_router(edges.router)
