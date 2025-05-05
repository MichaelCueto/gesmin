import os
import json
import re
from openai import OpenAI
from ocr_utils import extract_text_from_pdf
from mongo_utils import connect_to_mongo, insert_json_in_collection
from prompts import (generate_prompt_ficha_trabajador, generate_prompt_ficha_equipo,
                     generate_prompt_requerimiento_herramientas, generate_prompt_requerimiento_voladura)
import argparse

# Configuración del Cliente OpenAI
client_openai = OpenAI(
    api_key="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",  # 👉🏻 Reemplaza por tu API Key
    base_url="https://openrouter.ai/api/v1"
)

# Relación carpetas -> prompts
PROMPTS = {
    "fichas_trabajador": generate_prompt_ficha_trabajador,
    "fichas_equipo": generate_prompt_ficha_equipo,
    "requerimientos_herramientas": generate_prompt_requerimiento_herramientas,
    "requerimientos_voladura": generate_prompt_requerimiento_voladura
}


def extract_json_from_response(response: str) -> dict:
    """Extrae el primer bloque JSON bien formado de la respuesta completa"""

    if not response or response.strip() == "":
        raise ValueError("Respuesta vacía: No se puede extraer JSON.")

    # Encuentra el primer '{' para comenzar
    start_idx = response.find('{')
    if start_idx == -1:
        raise ValueError("No se encontró inicio de JSON.")

    # Recorre y cuenta llaves para detectar cierre
    open_braces = 0
    for i in range(start_idx, len(response)):
        if response[i] == '{':
            open_braces += 1
        elif response[i] == '}':
            open_braces -= 1

        if open_braces == 0:
            json_text = response[start_idx:i+1]
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error de decodificación JSON: {str(e)}")

    raise ValueError("No se pudo encontrar un bloque JSON completo.")
        
   
def procesar_documentos(base_path="../documentos/gestion_minera"):
    db, mongo_client = connect_to_mongo()
    total_procesados = 0

    # Crear carpetas auxiliares
    os.makedirs("logs/ocr", exist_ok=True)
    os.makedirs("logs/respuestas", exist_ok=True)
    os.makedirs("output/json", exist_ok=True)

    for carpeta in os.listdir(base_path):
        carpeta_path = os.path.join(base_path, carpeta)
        if os.path.isdir(carpeta_path) and carpeta in PROMPTS:
            print(f"📂 Procesando carpeta: {carpeta}")
            for archivo in os.listdir(carpeta_path):
                if archivo.lower().endswith(".pdf"):
                    ruta_pdf = os.path.join(carpeta_path, archivo)
                    try:
                        texto = extract_text_from_pdf(ruta_pdf)

                        # Guardar texto OCR bruto
                        with open(f"logs/ocr/{archivo}.txt", "w", encoding="utf-8") as f:
                            f.write(texto)

                        prompt_func = PROMPTS[carpeta]
                        prompt = prompt_func(texto)

                        respuesta = client_openai.chat.completions.create(
        quiero                    model="deepseek/deepseek-r1:free",
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=0.4
                        )

                        # Guardar respuesta cruda
                        with open(f"logs/respuestas/{archivo}.txt", "w", encoding="utf-8") as f:
                            f.write(respuesta.choices[0].message.content)

                        json_extraido = extract_json_from_response(respuesta.choices[0].message.content)

                        # Insertar en Mongo
                        insert_json_in_collection(db, carpeta, json_extraido)
                        if "_id" in json_extraido:
                            del json_extraido["_id"]

                        # Guardar local también
                        output_path = f"output/json/{archivo}.json"
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(json_extraido, f, ensure_ascii=False, indent=2)

                        print(f"✅ Procesado: {archivo}")
                        total_procesados += 1

                    except Exception as e:
                        print(f"❌ Error procesando {archivo}: {str(e)}")
    
    mongo_client.close()
    print(f"\n🚀 Total de documentos procesados: {total_procesados}")
    print("🔌 Conexión MongoDB cerrada")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="Carpeta con PDFs a procesar")
    args = parser.parse_args()
    procesar_documentos(base_path=args.path)