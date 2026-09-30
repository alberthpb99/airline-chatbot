from dotenv import load_dotenv
from openai import OpenAI
import os
import gradio as gr
from tools import tools
from prompts import developer_message
from utils import sanitize_history, handle_tool_call

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o-mini'
openai = OpenAI()

def chat(message,history):
    clean_history = sanitize_history(history[-7:])
    
    messages = [{'role':'developer', 'content': developer_message}] + clean_history + [{'role':'user', 'content':message}]
    response = openai.chat.completions.create(model=MODEL, messages= messages, tools=tools)
    
    file_generated = None
    
    if response.choices[0].finish_reason == 'tool_calls':
        message = response.choices[0].message
        messages.append(message)   # agregamos la respuesta de 'assistant' que contiene la info de tool_calls
        
        tool_response, file_generated = handle_tool_call(message)  
        messages.append(tool_response)  # agregamos el rol 'tool' con el resultado de la función
        
        # una última llamada a la api para traducir la respuesta de la herramienta
        response = openai.chat.completions.create(model=MODEL, messages=messages)
        
    final_text = response.choices[0].message.content
    
    if file_generated:
        return {"text": final_text, "files": [file_generated]}
    
    return final_text

demo = gr.ChatInterface(fn=chat)

if __name__ == "__main__":
    demo.launch()