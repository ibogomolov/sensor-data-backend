from collections.abc import Iterator
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine

from app.models import SensorData

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


class SensorDataRecord(SQLModel, table=True):
    __tablename__ = "sensor_data_records"

    id: int | None = Field(default=None, primary_key=True)
    asset_id: str
    timestamp: datetime
    vibration_x: float
    strain_gauge_1: float
    temperature: float

    @classmethod
    def from_sensor_data(cls, data: SensorData) -> "SensorDataRecord":
        return cls(
            asset_id=data.asset_id,
            timestamp=data.timestamp,
            vibration_x=data.sensors.vibration_x,
            strain_gauge_1=data.sensors.strain_gauge_1,
            temperature=data.sensors.temperature,
        )
