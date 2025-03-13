from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import logging
from backend.Recomendaciones import obtener_recomendacion
from fastapi.responses import FileResponse
import re

logging.basicConfig(level=logging.INFO)

Modelo_Entrenado = "backend/modelos/Modelo_de_Deteccion.pkl"
Vector = "backend/modelos/vectorizador.pkl"

CodigosSegurosCs = "backend/CodigosDescargables/Cs.zip"
CodigosSegurosPy= "backend/CodigosDescargables/Py.zip"

if not os.path.exists(Modelo_Entrenado) or not os.path.exists(Vector):
    raise FileNotFoundError("Modelo no encontrado, favor de entrenar el modelo antes de usarlo")

modelo = joblib.load(Modelo_Entrenado)
vec = joblib.load(Vector)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {"message": "API de detección de vulnerabilidades en código fuente"}


@app.post("/analizar/")
async def predict(file: UploadFile = File(...)):

    try:
        
        filename = re.sub(r"[^\w\.-]", "_", file.filename)

        logging.info(f"Procesando archivo: {file.filename}")
        if not (file.filename.endswith(".cs") or file.filename.endswith(".py")):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos de C# y Python")

        extension = os.path.splitext(file.filename)[1]
        data = await file.read()
        codigo = data.decode("utf-8")

        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

        if len(data) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande")

        if not codigo.strip():
            return {"nombre_archvio": file.filename, "resultado": "archivo vacio"}

        codigo_transformado = vec.transform([codigo])
        resultado = modelo.predict(codigo_transformado)[0]

        if resultado == 0:
            vulnerabilidad = "Tu codigo es seguro"
            resultado = "No se detectaron vulnerabilidades conocidas"
            recomendaciones = []         
            
        else:
            vulnerabilidad = "Tu codigo es vulnerable"
            recomendaciones = obtener_recomendacion(codigo, extension)

        return {
            "nombre_archvio": file.filename,
            "resultado": vulnerabilidad,
            "recomendaciones": recomendaciones
        }
    
    except Exception as e:
        logging.error(f"Error al procesar el archivo: {str(e)}")
        raise HTTPException(status_code = 500, detail=f"Error en el servidor: {str(e)}")
    
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="El archivo no está codificado en UTF-8")
    except Exception as e:
        logging.error(f"Error al procesar el archivo: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.get("/Obtener_Recomendaciones/")
def obtener_recomendaciones(tipo: str):
    try:
        if tipo.lower() == "py":
            file_path = CodigosSegurosPy
        elif tipo.lower() == "cs":
            file_path = CodigosSegurosCs
        else:
            raise HTTPException(status_code=400, detail="Tipo no válido. Use 'py' o 'cs'.")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/zip')
    
    except FileNotFoundError:
        return {"recomendaciones": "No se encontraron recomendaciones"}
