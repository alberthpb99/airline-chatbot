# AI Airlines Assistant

[Interactuar con el asistente](https://huggingface.co/spaces/alberthpb99/airline-chatbot)

AI Airlines Assistant es un chatbot interactivo diseñado para automatizar la atención al cliente y la reserva de pasajes aéreos. En esta versión inicial el sistema aprovecha la capacidad de Tool Calling de los LLMs para interactuar con herramientas externas como consultar disponibilidad y tarifas de los vuelos en tiempo real desde una base de datos y generar tiquetes de reserva descargables en formato PDF. La aplicación se encuentra desplegada y funcional en la plataforma de Hugging Face.

---

## Funcionalidades Actuales

* **Orquestación con Tool Calling:** El LLM decide de manera autónoma cuándo invocar funciones de lectura de datos o de generación de documentos según la intención del usuario.
* **Consulta de vuelos y tarifas:** El asistente examina rutas y precios consultando la base de datos de la empresa (simulada mediante un archivo JSON).
* **Generación de tiquetes en PDF:** Crea y entrega un comprobante de reserva en formato PDF listo para descargar.

---

## Estructura del repositorio

```text
airline-chatbot/
│
├── .gitignore          # Exclusión de archivos sensibles y temporales
├── app.py              # Interfaz de Gradio y flujo del chat
├── flights.json        # Archivo con rutas y tarifas de vuelos
├── prompts.py          # System prompt - Instrucciones de comportamiento del asistente
├── requirements.txt    # Dependencias del proyecto
├── tools.py            # Definición y esquemas de las herramientas (Tool Calling) para el LLM
└── utils.py            # Funciones auxiliares