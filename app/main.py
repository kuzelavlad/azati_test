import uvicorn
from app.api.main import api_router
from app.core.config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
# admin = get_admin(app=app, engine=async_engine)
# app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
