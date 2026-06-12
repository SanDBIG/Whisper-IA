import os
import logging

import torch
import whisper


def setup_paths():
    """
    Define las rutas principales del proyecto y crea las carpetas necesarias.

    Retorna un diccionario con las rutas que usará el script:
    - Carpeta base del archivo actual.
    - Carpeta de logs.
    - Carpeta donde deben estar los audios.
    - Carpeta donde se guardarán las transcripciones.
    - Ruta del archivo de log.
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))

    paths = {
        "base": base_dir,
        "logs": os.path.join(base_dir, "Logs"),
        "data": os.path.join(base_dir, "Data"),
        "transcription": os.path.join(base_dir, "Transcription"),
    }

    paths["log_file"] = os.path.join(paths["logs"], "execution_log.txt")

    # Crea las carpetas si no existen.
    # exist_ok=True evita errores si las carpetas ya estaban creadas.
    for folder in [paths["logs"], paths["data"], paths["transcription"]]:
        os.makedirs(folder, exist_ok=True)

    return paths


def setup_logging(log_file):
    """
    Configura el sistema de logging del script.

    El logging permite registrar eventos importantes en un archivo externo.
    En este caso, se guardan mensajes informativos, advertencias y errores
    dentro del archivo execution_log.txt.
    """

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def find_audio_file(data_folder, file_name):
    """
    Busca un archivo de audio dentro de la carpeta Data.

    El usuario ingresa el nombre del archivo sin extensión.
    Esta función prueba automáticamente con las extensiones permitidas.

    Parámetros:
    - data_folder: carpeta donde se buscará el archivo.
    - file_name: nombre del archivo sin extensión.

    Retorna:
    - La ruta completa del archivo si lo encuentra.
    - None si no encuentra ningún archivo válido.
    """

    allowed_extensions = [".mp3", ".wav", ".m4a"]

    for extension in allowed_extensions:
        candidate_path = os.path.join(data_folder, file_name + extension)

        if os.path.isfile(candidate_path):
            return candidate_path

    return None


def transcribe_audio(file_path, output_file):
    """
    Transcribe un archivo de audio usando Whisper.

    La función detecta si hay GPU disponible mediante CUDA.
    Si hay GPU, usa cuda.
    Si no hay GPU, usa cpu.

    Luego carga el modelo medium de Whisper, transcribe el audio en español
    y guarda el resultado en un archivo de texto con marcas de tiempo.

    Parámetros:
    - file_path: ruta completa del audio que se quiere transcribir.
    - output_file: ruta completa del archivo de salida.
    """

    try:
        # Selecciona automáticamente el dispositivo de ejecución.
        device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Dispositivo seleccionado: {device}")
        logging.info(f"Dispositivo seleccionado: {device}")

        # Carga el modelo de Whisper en el dispositivo seleccionado.
        # El modelo medium ofrece mayor precisión que small o base,
        # aunque consume más memoria y tarda más tiempo.
        model = whisper.load_model("medium", device=device)

        print(f"Modelo cargado correctamente en {device}")
        logging.info("Modelo medium cargado correctamente")

        # Ejecuta la transcripción.
        # language="es" fuerza el reconocimiento en español.
        # task="transcribe" indica que se quiere transcribir, no traducir.
        result = model.transcribe(
            file_path,
            language="es",
            task="transcribe"
        )

        # Guarda cada segmento con su tiempo de inicio, tiempo de término y texto.
        with open(output_file, "w", encoding="utf-8") as file:
            for segment in result["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

                file.write(f"[{start:.2f} - {end:.2f}] {text}\n")

        print(f"Transcripción completada: {output_file}")
        logging.info(f"Transcripción completada: {file_path} -> {output_file}")

    except Exception as error:
        # Captura errores de carga del modelo, lectura del audio,
        # problemas de CUDA, escritura del archivo u otros errores inesperados.
        print(f"Error durante la transcripción: {error}")
        logging.error(f"Error procesando {file_path}: {error}")


def main():
    """
    Controla el flujo principal del programa.

    Pasos:
    1. Prepara las rutas del proyecto.
    2. Configura el archivo de log.
    3. Pide al usuario el nombre del audio.
    4. Busca el archivo en la carpeta Data.
    5. Define el nombre del archivo de salida.
    6. Ejecuta la transcripción.
    """

    paths = setup_paths()
    setup_logging(paths["log_file"])

    print("Ingresa el nombre del archivo de audio sin extensión:")
    file_name = input().strip()

    audio_file = find_audio_file(paths["data"], file_name)

    if audio_file is None:
        allowed_extensions = [".mp3", ".wav", ".m4a"]

        print(f"Archivo no encontrado. Extensiones permitidas: {allowed_extensions}")
        logging.warning(
            f"No se encontró el archivo {file_name} con extensiones {allowed_extensions}"
        )

        print("Proceso finalizado.")
        return

    # Usa el nombre real del archivo encontrado para construir el nombre de salida.
    # os.path.splitext() separa el nombre base de la extensión de forma segura.
    output_name = f"{os.path.splitext(os.path.basename(audio_file))[0]}_transcription.txt"
    output_file = os.path.join(paths["transcription"], output_name)

    transcribe_audio(audio_file, output_file)

    print("Proceso finalizado.")


# Este bloque evita que el script se ejecute automáticamente si se importa desde otro archivo.
# Solo ejecuta main() cuando este archivo se corre directamente.
if __name__ == "__main__":
    main()