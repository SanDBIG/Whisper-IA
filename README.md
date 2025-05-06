# Whisper-IA: Instalación Local en Windows (GPU NVIDIA)

Este repositorio está diseñado para ejecutar el modelo **Whisper** de OpenAI a nivel local, con aceleración por GPU NVIDIA (en este caso, una RTX 3070 Ti). El objetivo es transcribir audios de entrevistas para una tesis.

---

## ¡Advertencia!

Este proceso involucra instalaciones delicadas a nivel del sistema. Si no cuentas con experiencia suficiente, te recomendamos no continuar sin respaldo técnico, ya que podrías obtener resultados inesperados o dañar tu entorno de trabajo.

Todos los pasos han sido probados y verificados para funcionar en **Windows 10/11**, con **Python 3.11.9**, **CUDA 11.8**, **cuDNN 9.0.1**, y **FFmpeg 7.1.1**.

---

## 1. Requisitos Generales

### Documentación oficial

* Whisper: [https://github.com/openai/whisper](https://github.com/openai/whisper)

### Hardware requerido

* GPU NVIDIA con soporte CUDA (recomendado: 8GB VRAM o más)
* Procesador compatible con instrucciones AVX2

---

## 2. Instalación Paso a Paso

### 1. Instalar Python 3.11.9

Descargar desde:
[https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)

Durante la instalación, activar la opción:

```
[✔] Add Python to PATH
```

Verificación:

```cmd
python --version
# Esperado: Python 3.11.9
```

---

### 2. Instalar CUDA Toolkit 11.8

Descargar desde:
[https://developer.nvidia.com/cuda-11-8-0-download-archive](https://developer.nvidia.com/cuda-11-8-0-download-archive)

Instalación:

* Elegir "custom" solo si sabes lo que haces
* Confirmar que se instalen `nvcc` y `nvml`

Verificación:

```cmd
nvcc --version
```

Esperado:

```
Cuda compilation tools, release 11.8, V11.8.89
```

---

### 3. Instalar cuDNN compatible (v9.0.1 para CUDA 11.x)

Descargar desde:
[https://developer.nvidia.com/rdp/cudnn-archive](https://developer.nvidia.com/rdp/cudnn-archive)

Se usó:

```
cudnn-windows-x86_64-9.0.1.52_cuda11-archive
```

Copiar los siguientes directorios dentro de la ruta de instalación de CUDA (por ejemplo `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`):

* `bin/` ➔ `bin/`
* `include/` ➔ `include/`
* `lib/` ➔ `lib/`

Confirmar que los DLLs como `cudnn64_8.dll` estén en la carpeta `bin/` de CUDA.

---

### 4. Instalar PyTorch compatible con CUDA 11.8

Desde CMD o PowerShell:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Verificación en Python:

```python
import torch
print(torch.cuda.is_available())  # True
print(torch.version.cuda)         # 11.8
print(torch.backends.cudnn.version())  # 90100 (corresponde a cuDNN 9.0.1)
```

---

### 5. Instalar FFmpeg 7.1.1 (Essentials Build)

Descargar desde:
[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Seleccionar:

```
ffmpeg-7.1.1-essentials_build.7z
```

Extraer y mover el contenido a una carpeta como:

```
C:\ffmpeg\ffmpeg-7.1.1-essentials_build
```

Agregar al `PATH` del sistema:

```
C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin
```

Verificación:

```cmd
ffmpeg -version
```

Esperado:

```
ffmpeg version 7.1.1-essentials_build-www.gyan.dev [...]
```

---

### 6. Instalar Whisper desde el repositorio oficial

```bash
pip install git+https://github.com/openai/whisper.git
```

(Si deseas actualizar forzadamente)

```bash
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```

---

## 3. Configuración en Visual Studio Code

* Abrir el proyecto.
* Crear un entorno virtual opcional:

```bash
python -m venv venv
```

* Activar el entorno:

```bash
.\venv\Scripts\activate
```

* Verificar que esté seleccionada la versión de Python correcta (3.11.9)
* Asegurarse de ejecutar desde la terminal de VS Code, no desde Windows CMD

---

## 4. Comandos de Verificación

### Python:

```cmd
python --version
# Python 3.11.9
```

### CUDA:

```cmd
nvcc --version
# release 11.8
```

### PyTorch:

```python
import torch
print(torch.cuda.is_available())  # True
print(torch.version.cuda)         # '11.8'
print(torch.backends.cudnn.version())  # 90100
```

### FFmpeg:

```cmd
ffmpeg -version
# ffmpeg version 7.1.1-essentials_build
```

### Whisper:

```python
import whisper
model = whisper.load_model("base")
```

---

## 5. Documentación Adicional

* Whisper GitHub: [https://github.com/openai/whisper](https://github.com/openai/whisper)
* FFmpeg Builds: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
* CUDA Archive: [https://developer.nvidia.com/cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive)
* cuDNN Archive: [https://developer.nvidia.com/rdp/cudnn-archive](https://developer.nvidia.com/rdp/cudnn-archive)
* Matriz de compatibilidad CUDA/cuDNN: [https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html](https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html)

---

**Fin de la Guía**

---

🛠️ Documento preparado por: **Diego Iturrieta Gajardo**  
📅 Fecha de finalización del entorno: **05 de mayo de 2025**  
💻 GPU utilizada: **NVIDIA GeForce RTX 3070 Ti**  
🧠 Proyecto académico: **Transcripción de entrevistas para tesis con Whisper (OpenAI)**  
