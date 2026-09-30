import json
from tools import get_flight_price, generate_ticket_pdf

# Función para limpiar el historial del chat, extrayendo únicamente el texto y eliminando metadatos como PDFs
def sanitize_history(history):
    clean_messages = []
    for msg in history:
        role = msg["role"]
        content = msg["content"]
    
        if isinstance(content, dict):
            content = content.get("text", "")

        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)
            content = " ".join(text_parts)
            
        clean_messages.append({"role": role, "content": str(content)})
    return clean_messages

# Función para ejecutar las funciones de cada tool y retorna la respuesta formateada
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    tool_call_id = tool_call.id
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    file_path = None
    
    if function_name == 'get_flight_price':
        result = get_flight_price(**arguments)
        
    elif function_name == 'generate_ticket_pdf':
        output_dict = generate_ticket_pdf(**arguments)
        file_path = output_dict.get("file_path")
        result = json.dumps(output_dict)
        
    else:
        result = "Error: Función no reconocida."
        
    response = {
        'role':'tool',
        'content':str(result),
        'tool_call_id': tool_call_id
    }
    return response, file_path