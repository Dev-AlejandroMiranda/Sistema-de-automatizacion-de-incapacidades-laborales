from sqlalchemy import Column, Integer, String, Date
from database import Base

class Incapacidad(Base): 
    __tablename__ = "incapacidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empleado = Column(String, index=True)
    cedula = Column(String, index=True)
    eps = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    dias = Column(Integer)
    archivo_original = Column(String)