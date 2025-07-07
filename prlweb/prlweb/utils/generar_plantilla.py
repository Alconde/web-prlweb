from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

def crear_plantilla(path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Título centrado
    c.setFont('Helvetica', 14)
    y = height - 50
    c.drawCentredString(width/2, y,
        "DESIGNACIÓN DE PERSONA ENCARGADA DE EMERGENCIAS Y PRIMEROS AUXILIOS"
    )

    form = c.acroForm
    y -= 60

    # Etiquetas y campos
    for label in ["EMPRESA", "PERSONA TRABAJADORA", "DNI / NIE", "FECHA"]:
        c.drawString(40, y, f"{label}:")
        form.textfield(
            name=label.lower().replace(" ", "_"),
            x=150, y=y-5, width=300, height=20,
            borderStyle='underlined',
            fontName='Helvetica', fontSize=12
        )
        y -= 40

    # Texto largo centrado con ajuste de línea
    texto = (
        "Mediante la firma del presente documento, se procede a la designación "
        "de la persona trabajadora cuyos datos constan arriba como encargada de "
        "coordinar y poner en práctica.Mediante la firma del presente documento, "
        "se procede a la designación de la persona trabajadora cuyos datos "
        "constan arriba como encargada de coordinar y poner en práctica, en el "
        "ámbito de la empresa, las medidas de emergencia adoptadas en materia de "
        "emergencias, lucha contra incendios, evacuación y primeros auxilios, en "
        "cumplimiento  del  artículo  33  de  la  Ley  de  Prevención de Riesgos Laborales "
        "Consideraciones de la designación:"
        "-Tal designación se produce por considerarse la persona designada como "
        "capacitada y con la formación necesaria en la materia."
        "-En este sentido, la empresa se compromete a facilitar la formación e "
        "información adicional que resultara necesaria."
        "-La empresa facilita a la persona designada copia del documento que contempla "
        "las medidas de emergencia y primeros auxilios aprobadas en la empresa, para el "
        "adecuado cumplimiento de las funciones asignadas"
    )
    c.setFont('Helvetica', 12)
    max_width = width - 80  # márgenes 40 izq y der
    lines = simpleSplit(texto, 'Helvetica', 12, max_width)
    for line in lines:
        c.drawCentredString(width/2, y, line)  # centra cada línea
        y -= 16

    # Firmas centradas
    c.drawCentredString(width/4, y-40, "Firma del trabajador/a:")
    form.textfield(
        name='firma_trabajador',
        x=width/4 + 50, y=y-45,
        width=200, height=20, borderStyle='underlined'
    )
    c.drawCentredString(3*width/4, y-40, "Firma de la empresa:")
    form.textfield(
        name='firma_empresa',
        x=3*width/4 + 50, y=y-45,
        width=200, height=20, borderStyle='underlined'
    )

    c.save()



