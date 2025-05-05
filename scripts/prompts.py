# prompts.py

def generate_prompt_ficha_trabajador(texto):
    """Prompt para extraer Ficha de Trabajador"""
    return f"""
EXTRACCIÓN DE DATOS - FICHA DE TRABAJADOR

INSTRUCCIONES OBLIGATORIAS:
- Tu respuesta debe ser exclusivamente un único bloque JSON válido.
- NO escribas ningún texto fuera del JSON (ni explicaciones, saludos, comentarios, análisis, pasos intermedios, resultados, advertencias, ni notas).
- NO uses expresiones como "Let's start", "Here's the JSON", "First...", "Ok, here's...", etc.
- NO pongas títulos ni encabezados ("Extracted Data:", "Result:", "Data:", etc).
- NO agregues líneas de separación ni saltos de línea fuera del JSON.
- El JSON debe empezar directamente con '{' y terminar con '}'.
- Usa comillas dobles ("") para todos los strings.
- Si algún campo no tiene dato, igual debe existir y su valor debe ser "N/A".
- NO cierres el mensaje con frases como "Process completed", "Done", "Listo", etc.
- Responde ÚNICAMENTE con el bloque JSON, sin ningún contenido adicional.

ESTRUCTURA:

{{
  "fecha_ingreso": "string",
  "hora_ingreso": "string",
  "codigo_ingreso": "string",
  "nombres": "string",
  "apellidos": "string",
  "dni": "string",
  "edad": "string",
  "fecha_nacimiento": "string",
  "lugar_nacimiento": "string",
  "departamento": "string",
  "provincia": "string",
  "direccion": "string",
  "referencia": "string",
  "telefono": "string",
  "movil": "string",
  "correo_electronico": "string",
  "alergias": "string",
  "enfermedades": "string",
  "dolencias": "string",
  "tipo_sangre": "string",
  "asegurado": "string",
  "licencia_conducir": "string",
  "experiencia_mineria": "string",
  "afiliacion_pension": "string",
  "nombre_afp": "string",
  "cuenta_ahorros": {{
    "banco": "string",
    "numero_cuenta": "string",
    "moneda": "string"
  }},
  "observaciones": "string",
  "firma_trabajador": "string",
  "firma_representante_mina": "string"
}}

TEXTO ESCANEADO:
{texto}
"""


def generate_prompt_ficha_equipo(texto):
    """Prompt para extraer Ficha de Equipo"""
    return f"""
EXTRACCIÓN DE DATOS - FICHA DE EQUIPO

INSTRUCCIONES OBLIGATORIAS:
(mismas reglas que arriba)

ESTRUCTURA:

{{
  "proyecto": "string",
  "codigo_equipo": "string",
  "equipo": "string",
  "anio_fabricacion": "string",
  "numero_serie": "string",
  "fecha_inicio_uso": "string",
  "estado": "string",
  "marca": "string",
  "modelo": "string",
  "color": "string",
  "periodo_mantenimiento": "string",
  "cuidados_precauciones": "string",
  "responsable": {{
    "nombres_apellidos": "string",
    "firma": "string"
  }},
  "inventarios": [
    {{
      "anio": "string",
      "firma": "string"
    }}
  ],
  "mantenimiento_reparaciones": [
    {{
      "tipo": "string",
      "fecha": "string",
      "hora": "string",
      "detalle": "string",
      "nombres_apellidos": "string",
      "firma": "string"
    }}
  ]
}}

TEXTO ESCANEADO:
{texto}
"""


def generate_prompt_requerimiento_herramientas(texto):
    """Prompt para Requerimiento de Herramientas"""
    return f"""
EXTRACCIÓN DE DATOS - FORMULARIO DE HERRAMIENTAS Y EQUIPOS

INSTRUCCIONES OBLIGATORIAS:
(mismas reglas que arriba)

ESTRUCTURA:

{{
  "documento": "string",
  "proyecto": "string",
  "tipo_documento": "string",
  "fecha": "string",
  "numero": "string",
  "hora": "string",
  "requerimiento": {{
    "solicitante": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }},
    "herramientas": [
      {{
        "cantidad": "string",
        "descripcion": "string",
        "estado": "string",
        "observaciones": "string"
      }}
    ],
    "entrega_almacen": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }}
  }},
  "devolucion": {{
    "devolvente": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }},
    "herramientas": [
      {{
        "cantidad": "string",
        "descripcion": "string",
        "estado": "string",
        "observaciones": "string"
      }}
    ],
    "recepcion_almacen": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }}
  }}
}}

TEXTO ESCANEADO:
{texto}
"""


def generate_prompt_requerimiento_voladura(texto):
    """Prompt para Requerimiento de Voladura"""
    return f"""
EXTRACCIÓN DE DATOS - FORMULARIO DE VOLADURA

INSTRUCCIONES OBLIGATORIAS:
(mismas reglas que arriba)

ESTRUCTURA:

{{
  "documento": "string",
  "proyecto": "string",
  "tipo_documento": "string",
  "fecha": "string",
  "numero": "string",
  "hora": "string",
  "requerimiento": {{
    "solicitante": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }},
    "materiales": [
      {{
        "marca": "string",
        "tipo": "string",
        "cantidad": "string",
        "unidad": "string"
      }}
    ],
    "entrega_polvorin": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }}
  }},
  "devolucion": {{
    "devolvente": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }},
    "materiales": [
      {{
        "marca": "string",
        "tipo": "string",
        "cantidad": "string",
        "unidad": "string"
      }}
    ],
    "recepcion_polvorin": {{
      "firma": "string",
      "nombre": "string",
      "cargo": "string"
    }}
  }},
  "observaciones": "string"
}}

TEXTO ESCANEADO:
{texto}
"""