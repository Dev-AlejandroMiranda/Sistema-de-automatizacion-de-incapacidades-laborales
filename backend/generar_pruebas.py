from fpdf import FPDF

nombres = ["Juan Perez", "Maria Lopez", "Carlos Gomez", "Ana Torres", "Luis Diaz"]
cedulas = ["12345678", "98765432", "11223344", "55667788", "99887766"]
eps_nombres = ["SaludTotal", "Sura", "Sanitas", "Nueva EPS", "Coomeva"]

for i in range(5):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    mes = i + 1
    contenido = f"""
    Certificado de Incapacidad
    
    Se certifica que el paciente {nombres[i]}, 
    identificado con C.C {cedulas[i]}, 
    presenta incapacidad medica desde el 10/0{mes}/2023 hasta el 15/0{mes}/2023.
    
    EPS: {eps_nombres[i]}
    """
    
    pdf.multi_cell(0, 10, txt=contenido)
    pdf.output(f"incapacidad_prueba_{i+1}.pdf")

print("5 PDFs generados exitosamente")