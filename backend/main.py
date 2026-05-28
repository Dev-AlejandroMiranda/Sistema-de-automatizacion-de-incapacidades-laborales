from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import extractor
import pandas as pd
import io
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "API en linea"}

@app.post("/api/upload")
async def subir_incapacidad(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten PDFs")

    contenido = await file.read()
    
    # Capturar errores del extractor (ej. PDF escaneado sin OCR instalado)
    try:
        texto = extractor.extraer_texto_pdf(contenido)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    datos = extractor.parsear_datos(texto)

    # Validar si la extracción fallo completamente
    if not datos["cedula"] and not datos["fecha_inicio"]:
        raise HTTPException(
            status_code=422, 
            detail="No se pudo extraer información del PDF. Verifique que no sea una imagen o ajuste el OCR."
        )

    db_incapacidad = models.Incapacidad(
        nombre_empleado=datos["nombre_empleado"],
        cedula=datos["cedula"],
        eps=datos["eps"],
        fecha_inicio=datos["fecha_inicio"],
        fecha_fin=datos["fecha_fin"],
        dias=datos["dias"],
        archivo_original=file.filename
    )
    
    db.add(db_incapacidad)
    db.commit()
    db.refresh(db_incapacidad)

    return {
        "mensaje": "Archivo procesado y guardado",
        "datos_extraidos": datos,
        "id_registro": db_incapacidad.id
    }
@app.get("/api/export-excel")
def exportar_excel(ids: List[int] = Query([]), db: Session = Depends(get_db)):
    # Filtrar solo por los IDs proporcionados
    if ids:
        registros = db.query(models.Incapacidad).filter(models.Incapacidad.id.in_(ids)).all()
    else:
        registros = []
    
    if not registros:
        raise HTTPException(status_code=404, detail="No hay registros para exportar")

    data = [{
        "ID": r.id,
        "Nombre": r.nombre_empleado,
        "Cedula": r.cedula,
        "EPS": r.eps,
        "Fecha Inicio": r.fecha_inicio,
        "Fecha Fin": r.fecha_fin,
        "Dias": r.dias,
        "Archivo Original": r.archivo_original
    } for r in registros]

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Incapacidades')
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="incapacidades.xlsx"'
    }
    return StreamingResponse(
        output, 
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        headers=headers
    )