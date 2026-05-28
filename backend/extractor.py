import fitz
import re
from dateutil import parser
import shutil

# Verificar si los ejecutables de OCR existen en el sistema
TESSERACT_DISPONIBLE = shutil.which('tesseract') is not None
POPPLER_DISPONIBLE = shutil.which('pdfinfo') is not None

def extraer_texto_pdf(contenido_bytes: bytes) -> str:
    # 1. Intentar extraer texto digital
    doc = fitz.open(stream=contenido_bytes, filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()

    # 2. Si no hay texto, evaluar OCR
    if not texto.strip():
        if not TESSERACT_DISPONIBLE or not POPPLER_DISPONIBLE:
            # Lanzar error controlado si faltan dependencias del sistema
            raise Exception("PDF escaneado (sin texto digital). Se requiere instalar Tesseract y Poppler en el sistema para OCR.")
        
        # Si están instalados, intentar OCR
        try:
            import pytesseract
            from pdf2image import convert_from_bytes
            
            imagenes = convert_from_bytes(contenido_bytes)
            texto_ocr = ""
            for img in imagenes:
                texto_ocr += pytesseract.image_to_string(img, lang='spa')
            texto = texto_ocr
        except Exception as e:
            raise Exception(f"Error durante el procesamiento OCR: {str(e)}")

    return texto

def parsear_datos(texto: str) -> dict:
    cedula_match = re.search(r'(?:C\.?C\.?|Cedula)\s*[:\-]?\s*(\d{6,10})', texto, re.IGNORECASE)
    nombre_match = re.search(r'paciente\s+([a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+),', texto, re.IGNORECASE)
    eps_match = re.search(r'EPS\s*[:\-]?\s*([a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+)', texto, re.IGNORECASE)
    
    fechas_encontradas = re.findall(r'\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}', texto)
    
    fecha_inicio = None
    fecha_fin = None
    dias = None

    if len(fechas_encontradas) >= 2:
        try:
            fecha_inicio = parser.parse(fechas_encontradas[0], dayfirst=True).date()
            fecha_fin = parser.parse(fechas_encontradas[-1], dayfirst=True).date()
            dias = (fecha_fin - fecha_inicio).days + 1
        except Exception:
            pass

    return {
        "nombre_empleado": nombre_match.group(1).strip() if nombre_match else "Por confirmar",
        "cedula": cedula_match.group(1) if cedula_match else None,
        "eps": eps_match.group(1).strip() if eps_match else "Por confirmar",
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "dias": dias
    }