"""Request payload schemas for the API routers."""

from pydantic import BaseModel


class TaskActionPayload(BaseModel):
    action: str


class SensorPayload(BaseModel):
    field_id: str
    temp: float
    moisture: float
    n: int
    p: int
    k: int
    soil_ph: float
    soil_ec: float
    water_ph: float
    water_do: float
    water_turbidity: float


class AIChatPayload(BaseModel):
    prompt: str


class VoiceCommandPayload(BaseModel):
    prompt: str
