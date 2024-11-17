# Whisper-IA
 Este repositorio es para ejecutar a nivel local el modelo Whisper para transcribir audios de entrevistas para una tesis.
 Visitar carpeta documentación para leer los apartados tecnicos necesarios para replicar esta ejecución de manera adecuada.

Para informarte de manera previa sobre el funcionamiento, capacidades y requisitos de whisper
se recomienda visitar y leer detenidamente la documentación:
https://github.com/openai/whisper

Para ejecutar el modelo de whisper son necesarios diferentes pasos previos de instalación de 
diferentes complementos previos, la presente documentación apunta a la ejecución de whisper
mediante python en una tarjeta de video nvidia 3070ti, si no posees los conocimientos suficientes
no ejecutes todo el apartado de instrucciones a continuación, ya que puede llevarte a no tener
resultados, un resultado no esperado, o mal lograr tu computador.


#-----------Requisitos previos de y Comandos de Instalacion-----------------------------------

1.- Instalar Python 3.11.0
    Descarga Python 3.11 desde el sitio oficial.
    Asegúrate de marcar la opción Add Python to PATH durante la instalación.


2.- Instalar CUDA Toolkit 11.8
    Descarga CUDA Toolkit 11.8 desde el archivo de descargas de NVIDIA.
    Durante la instalación, agrega las rutas al PATH del sistema.
    

3.- Instalar PyTorch Compatible con CUDA 11.8
    Ejecuta el siguiente comando en cmd para instalar PyTorch:
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


4.- Instalar FFmpeg
    Descarga FFmpeg desde ffmpeg.org https://ffmpeg.org/download.html
    Agrega la ruta de la carpeta bin a las variables de entorno del sistema (PATH).
    

5.- Instalar Whisper

    Instala el modelo Whisper desde el repositorio oficial:
    El siguiente comando instalara el ultimo commit del repositorio, en las dependencias
    de python, hazlo mediante cmd.
    pip install git+https://github.com/openai/whisper.git

    Para instalar la ultima version del paquete del repositorio de whisper ejecutar en cmd:
    pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git


6.- Revisar capacidades para ejecutar el modelo
    En caso de que exista algún error fuera de lo descrito en esta documentación, visitar la
    documentación propia de whisper.
    https://github.com/openai/whisper

#-------------Comandos de Verificacion de Complementos------------------------------------------


1.- Verificar Python
    En cmd ejectuar:
    python --version
    Esto debe devolver Python 3.11.0.

2.- Verificar CUDA
    En CMD, verifica la instalación de CUDA y la compatibilidad de la GPU:
    nvidia-smi
    Esto debe mostrar la versión de CUDA soportada por los controladores.

3.- Verificar PyTorch
    Ejecuta Python e importa PyTorch para verificar la detección de CUDA:
    import torch
    print(torch.cuda.is_available())  # Debe devolver True
    print(torch.version.cuda)         # Debe devolver '11.8'

4.- Verificar FFmpeg
    Verifica que FFmpeg esté accesible desde cmd:
    ffmpeg -version
    Esto debe mostrar la versión instalada de FFmpeg.

5.- Verificar Whisper
    Prueba importar Whisper en python:
    import whisper
    model = whisper.load_model("base")  # Verifica que carga sin errores

6.- Revisar capacidades para ejecutar el modelo
    En caso de que exista algún error fuera de lo descrito en esta documentación, visitar la
    documentación propia de whisper.
    https://github.com/openai/whisper
