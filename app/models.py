from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorReadings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vibration_x: float
    strain_gauge_1: float
    temperature: float


class SensorData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str
    timestamp: datetime
    sensors: SensorReadings
