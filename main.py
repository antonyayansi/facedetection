from fastapi import FastAPI, File, UploadFile, Form
import face_recognition
import numpy as np
import json
import io
from PIL import Image

app = FastAPI(title="Tukuy Obra Face API")

@app.post("/encode-face")
async def encode_face(image: UploadFile = File(...)):
    img_bytes = await image.read()
    img = face_recognition.load_image_file(io.BytesIO(img_bytes))
    faces = face_recognition.face_encodings(img)

    if not faces:
        return {"error": "No se detectó ningún rostro"}
    
    # Devolver el descriptor (lista de 128 floats)
    return {"descriptor": faces[0].tolist()}

@app.post("/compare-face")
async def compare_face(
    descriptor: str = Form(...), # "[-0.12922652065410156, 0.03412323498725891, ...]"
    image: UploadFile = File(...)
):
    try:
        descriptor_clean = descriptor.strip()
        if descriptor_clean.startswith('"') and descriptor_clean.endswith('"'):
            descriptor_clean = descriptor_clean[1:-1]
        
        descriptor_list = json.loads(descriptor_clean)
        known_encoding = np.array(descriptor_list, dtype=np.float64)
    except Exception as e:
        return {"error": f"Descriptor inválido: {str(e)}"}

    img_bytes = await image.read()
    img = face_recognition.load_image_file(io.BytesIO(img_bytes))
    unknown_encodings = face_recognition.face_encodings(img)

    if not unknown_encodings:
        return {"error": "No se detectó ningún rostro en la imagen"}

    unknown_encoding = unknown_encodings[0]
    distance = float(np.linalg.norm(known_encoding - unknown_encoding))
    threshold = 0.59999

    # Cálculo de confianza: inversamente proporcional a la distancia
    # Distancia cercana a 0 = alta confianza (100%)
    # Distancia >= threshold = baja confianza (0%)
    confidence = max(0.0, (1.0 - (distance / threshold))) * 100

    return {
        "distance": distance,
        "confidence": round(confidence, 2)
    }

@app.get("/")
async def root():
    return {"message": "Tukuy Obra Face API funcionando correctamente"}
