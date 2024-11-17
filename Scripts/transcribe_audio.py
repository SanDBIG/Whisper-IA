#--------------------

# transcribe_audio.py

import whisper
import torch

def transcribe_audio(file_path, output_file="transcription_with_timestamps_3.txt"):
    # Verificar si CUDA está disponible para usar la GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Dispositivo seleccionado: {device}")
    
    # Cargar el modelo "medium" de Whisper especificando el dispositivo
    model = whisper.load_model("medium", device=device)
    
    # Configurar el idioma español y la transcripcion
    options = {
        "language": "es",
        "task": "transcribe"  # 'transcribe' para transcripción
    }
    
    # Procesar el archivo de audio y transcribir con timestamps
    result = model.transcribe(file_path, **options)
    
    # Guardar la transcripción con timestamps en un archivo de texto
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
    
    # Mensaje de confirmación
    print("Audio Transcribed")  # Mensaje en consola para indicar que terminó la transcripción

# Ruta del archivo de audio procesado
file_path = "Entrevista Allan Ugarte Ejemplo 2.m4a"  # Asegúrate de que el archivo esté en la misma carpeta o proporciona la ruta completa
transcribe_audio(file_path)


