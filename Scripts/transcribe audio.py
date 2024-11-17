import whisper
import torch
import os
import logging

# Obtener la ruta base del script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Definir rutas relativas basadas en la ubicación del script
log_folder = os.path.join(base_dir, "../Logs/")
data_folder = os.path.join(base_dir, "../Data/")
transcription_folder = os.path.join(base_dir, "../Transcription/")
log_file = os.path.join(log_folder, "execution_log.txt")

# Crear carpetas si no existen
for folder in [log_folder, data_folder, transcription_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Verificar si el archivo de logs existe, si no, crearlo vacío
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("")  # Crear un archivo vacío

# Configurar logging para guardar los logs en el archivo
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transcribe_audio(file_path, output_file):
    try:
        # Verificar si CUDA está disponible para usar la GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Dispositivo seleccionado: {device}")
        print(f"Dispositivo seleccionado: {device}")
        
        # Cargar el modelo "medium" de Whisper especificando el dispositivo
        model = whisper.load_model("medium", device=device)
        
        # Configurar el idioma español y otras opciones
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
        logging.info(f"Transcripción completada: {file_path} -> {output_file}")
        print(f"Audio Transcribed: {file_path}")
    except Exception as e:
        logging.error(f"Error procesando {file_path}: {e}")
        print(f"Error procesando {file_path}: {e}")

def process_all_audios(input_folder, output_folder):
    # Iterar sobre los archivos de la carpeta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.endswith((".wav", ".m4a", ".mp3")):  # Extensiones compatibles
            file_path = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, f"{file_name.split('.')[0]}_transcription.txt")
            
            logging.info(f"Procesando archivo: {file_name}")
            transcribe_audio(file_path, output_file)

# Procesar todos los audios
process_all_audios(data_folder, transcription_folder)
