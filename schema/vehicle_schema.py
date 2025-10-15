from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehiculoEntrada(BaseModel):
    placa: str
    fecha_entrada: Optional[datetime] = None

class VehiculoSalida(BaseModel):
    placa: str
    fecha_salida: datetime

class VehiculoResponse(BaseModel):
    id: int
    placa: str
    fecha_entrada: datetime

    class Config:
        orm_mode = True
