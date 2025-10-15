from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from config.db import SessionLocal
from model.vehicles import VehiculoActivo, VehiculoHistorial
from schema.vehicle_schema import VehiculoEntrada, VehiculoSalida, VehiculoResponse

vehiculo = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

# Dependencia de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@vehiculo.post("/entrada", response_model=VehiculoResponse)
def registrar_entrada(data: VehiculoEntrada, db: Session = Depends(get_db)):
    existente = db.query(VehiculoActivo).filter(VehiculoActivo.placa == data.placa).first()
    if existente:
        raise HTTPException(status_code=400, detail="El vehículo ya está registrado como activo")

    nuevo = VehiculoActivo(
        placa=data.placa,
        fecha_entrada=data.fecha_entrada or datetime.now()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@vehiculo.post("/salida")
def registrar_salida(data: VehiculoSalida, db: Session = Depends(get_db)):
    vehiculo = db.query(VehiculoActivo).filter(VehiculoActivo.placa == data.placa).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado en activos")

    historial = VehiculoHistorial(
        placa=vehiculo.placa,
        fecha_entrada=vehiculo.fecha_entrada,
        fecha_salida=data.fecha_salida
    )

    db.add(historial)
    db.delete(vehiculo)
    db.commit()
    return {"mensaje": f"Vehículo {data.placa} movido al historial correctamente"}

@vehiculo.get("/activos", response_model=list[VehiculoResponse])
def listar_activos(db: Session = Depends(get_db)):
    return db.query(VehiculoActivo).all()

@vehiculo.get("/historial")
def listar_historial(db: Session = Depends(get_db)):
    return db.query(VehiculoHistorial).all()

@vehiculo.get("/buscar/{placa}")
def buscar_por_placa(placa: str, db: Session = Depends(get_db)):
    activo = db.query(VehiculoActivo).filter(VehiculoActivo.placa == placa).first()
    if activo:
        return {"estado": "activo", "vehiculo": activo}

    historial = db.query(VehiculoHistorial).filter(VehiculoHistorial.placa == placa).first()
    if historial:
        return {"estado": "historial", "vehiculo": historial}

    raise HTTPException(status_code=404, detail="Vehículo no encontrado")
