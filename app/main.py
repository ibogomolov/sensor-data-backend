import logging.config
from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Response, status
from sqlmodel import Session

from app.database import SensorDataRecord, get_session, init_db
from app.metrics import METRICS_ENDPOINT, MetricsMiddleware, get_metrics
from app.models import SensorData

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

STRAIN_GAUGE_1_THRESHOLD = 500.0
TEST_ENDPOINT = "/test_strain_gauge_warning"
TEST_WEBHOOK_URL = f"http://127.0.0.1:8000{TEST_ENDPOINT}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(MetricsMiddleware)


@app.post("/sensor_data")
async def evaluate_sensor_data(
        data: SensorData,
        background_tasks: BackgroundTasks,
        session: Annotated[Session, Depends(get_session)],
):
    session.add(SensorDataRecord.from_sensor_data(data))
    session.commit()

    if data.sensors.strain_gauge_1 > STRAIN_GAUGE_1_THRESHOLD:
        logger.warning(
            "strain_gauge_1 exceeded threshold for asset %s: %s > %s",
            data.asset_id,
            data.sensors.strain_gauge_1,
            STRAIN_GAUGE_1_THRESHOLD,
        )
        background_tasks.add_task(notify_webhook, data)
    return Response(status_code=status.HTTP_200_OK)


async def notify_webhook(data: SensorData) -> None:
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                TEST_WEBHOOK_URL,
                json=data.model_dump(mode="json"),
                timeout=10.0,
            )
        except httpx.HTTPError:
            logger.exception(
                "Failed to POST strain gauge warning to webhook %s",
                TEST_WEBHOOK_URL,
            )


@app.post(TEST_ENDPOINT)
async def test_strain_gauge_warning(data: SensorData):
    logger.info("Received strain gauge warning for value %s", data.sensors.strain_gauge_1)


@app.get(METRICS_ENDPOINT)
async def metrics():
    return get_metrics()
