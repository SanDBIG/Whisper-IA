import whisper
import torch
import os
import logging

# ===============================
# CONFIGURACIÓN Y PREPARACIÓN
# ===============================

# Ruta base del script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas internas del proyecto (ahora correctamente relativas)
log_folder = os.path.join(base_dir, "Logs")
data_folder = os.path.join(base_dir, "Data")
transcription_folder = os.path.join(base_dir, "Transcription")
log_file = os.path.join(log_folder, "execution_log.txt")

# Crear carpetas si no existen
print("🔧 Verificando y creando carpetas necesarias...")
for folder in [log_folder, data_folder, transcription_folder]:
    os.makedirs(folder, exist_ok=True)

# Crear archivo de log si no existe
if not os.path.exists(log_file):
    open(log_file, "w").close()

# Configuración de logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===============================
# FUNCIÓN PRINCIPAL DE TRANSCRIPCIÓN
# ===============================

def transcribe_audio(file_path, output_file):
    try:
        # Selección automática de dispositivo
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Dispositivo seleccionado: {device}")
        print(f"📌 Dispositivo seleccionado: {device}")

        # Cargar modelo medium
        model = whisper.load_model("medium", device=device)
        print("📥 Modelo cargado correctamente en", device)

        # Opciones de transcripción
        options = {
            "language": "es",
            "task": "transcribe"
        }

        print(f"🎧 Transcribiendo archivo: {file_path}")
        result = model.transcribe(file_path, **options)

        with open(output_file, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

        print(f"✅ Transcripción completada: {output_file}")
        logging.info(f"Transcripción completada: {file_path} -> {output_file}")

    except Exception as e:
        print(f"❌ Error durante la transcripción: {e}")
        logging.error(f"Error procesando {file_path}: {e}")

# ===============================
# FLUJO PRINCIPAL DEL SCRIPT
# ===============================

print("🎧 Ingresa el nombre del archivo de audio (sin extensión):")
file_input = input().strip()

# Extensiones permitidas
allowed_exts = [".mp3", ".wav", ".m4a"]
found = False
file_path = ""
for ext in allowed_exts:
    candidate = os.path.join(data_folder, file_input + ext)
    if os.path.isfile(candidate):
        file_path = candidate
        found = True
        break

if not found:
    print(f"❌ Archivo no encontrado con ninguna de las extensiones permitidas: {allowed_exts}")
    logging.warning(f"No se encontró el archivo {file_input} con extensiones {allowed_exts}")
    print("🏁 Proceso completado.")
else:
    # Ruta del archivo de salida
    output_file = os.path.join(
        transcription_folder, f"{os.path.basename(file_path).split('.')[0]}_transcription.txt"
    )
    transcribe_audio(file_path, output_file)
    print("🏁 Proceso completado.")
