from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notification
from core.config import settings
from core.logger import logger

logger()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(
    notification.router, prefix="/api/v1/notification", tags=["notification"]
)
