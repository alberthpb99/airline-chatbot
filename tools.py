import json
import random
import string
from fpdf import FPDF


# Cargamos los datos de los vuelos
with open("flights.json", "r", encoding="utf-8") as f:
    precios_vuelos = json.load(f)

# Función para obtener el precio de cada vuelo
def get_flight_price(origen: str, destino: str) -> str:
    origen_clean = origen.lower().strip()
    destino_clean = destino.lower().strip()
    
    rutas_origen = precios_vuelos.get(origen_clean)
    if not rutas_origen:
        return f'No operamos vuelos saliendo desde {origen_clean.title()}'
    
    precio = rutas_origen.get(destino_clean)
    if not precio:
        return f'No tenemos vuelos directos desde {origen.title()} hacia {destino.title()}.'
    
    return f'El precio del vuelo desde {origen_clean.title()} hasta {destino_clean.title()} es {precio}'

# Función para generar el PDF del ticket
def generate_ticket_pdf(nombre_pasajero: str, origen: str, destino: str, fecha: str, hora: str, precio: str) -> dict:
    
    # Datos aleatorios para pnr, asiento y puerta de embarque
    pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    puerta = f"{random.choice(['A', 'B', 'C'])}{random.randint(1, 15)}"
    asiento = f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
    
    # Creamos el PDF
    pdf = FPDF(orientation='P', unit='mm', format='A5')
    pdf.add_page()
    
    # Encabezado
    pdf.set_fill_color(24, 43, 73) 
    pdf.rect(0, 0, 148, 25, 'F')
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "AI AIRLINES - TICKET", ln=True, align="C")
    
    # Cuerpo
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    
    # Datos Principales
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Pasajero:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, nombre_pasajero.title())
    pdf.ln()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Código Reserva:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, pnr)
    pdf.ln()
    
    # Línea separadora
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 138, pdf.get_y())
    pdf.ln(5)
    
    # Detalles del Vuelo
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Origen:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{origen.upper()}")
    pdf.ln()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Destino:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{destino.upper()}")
    pdf.ln()

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Fecha:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{fecha}")
    pdf.ln()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Hora:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{hora}")
    pdf.ln()

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Puerta:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{puerta}")
    pdf.ln()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Asiento:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{asiento}")
    pdf.ln()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 8, "Precio:")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{precio}")
    pdf.ln()

    # Guardamos el archivo en disco
    file_path = f"ticket_{pnr}.pdf"
    pdf.output(file_path)
    
    return {
        "status": "éxito",
        "mensaje": f"Tiquete generado exitosamente para {nombre_pasajero}.",
        "pnr": pnr,
        "file_path": file_path
    }

# JSON Schema - get_flight_price
price_function = {
    'name': 'get_flight_price',
    'description': 'Obtiene el precio del vuelo entre una ciudad de origen y una ciudad de destino.',
    'parameters': {
        'type': 'object',
        'properties': {
            'origen': {
                'type': 'string',
                'description': 'Ciudad de salida (ej. Cali, Bogotá, Medellín)',
            },
            'destino': {
                'type': 'string',
                'description': 'Ciudad de llegada (ej. Cartagena, San Andrés)'
                
            }
        },
        'required': ['origen', 'destino']
    }
}

# JSON Schema - generate_ticket_pdf
ticket_pdf_function = {
    'name': 'generate_ticket_pdf',
    'description': 'Genera y emite un tiquete de avión en formato PDF con la información de la reserva del usuario.',
    'parameters': {
        'type': 'object',
        'properties': {
            'nombre_pasajero': {
                'type': 'string',
                'description': 'Nombre completo de la persona que viajará'
            },
            'origen': {
                'type': 'string',
                'description': 'Ciudad de salida/origen (ej. Cali, Bogotá, Medellín)',
            },
            'destino': {
                'type': 'string',
                'description': 'Ciudad de llegada/destino (ej. Cartagena, San Andrés)'
                
            },
            'fecha': {
                'type': 'string',
                'description': 'Fecha del viaje indicada por el usuario (ej. "2026-10-15" o "15 de Octubre").'
            },
            'hora': {
                'type': 'string',
                'description': 'Hora del vuelo. Usa la hora mencionada previamente por el usuario (ej. "6:00 AM" o "a las 8" o "15:00")'
            },
            'precio': {
                'type': 'string',
                'description': 'Precio total del tiquete obtenido previamente en la consulta.'
            }
        },
        'required': ['nombre_pasajero','origen','destino','fecha','hora', 'precio']
    }
}

# Tools
tools = [
    {'type':'function', 'function':price_function},
    {'type':'function', 'function':ticket_pdf_function}
]