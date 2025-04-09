# Windows Startup Manager 

Herramienta para gestionar programas en el inicio de Windows con interfaz gráfica

## Características 
- Interfaz gráfica intuitiva
- Soporte para instalación en usuario actual o todos los usuarios
- Selección de archivos con diálogo nativo
- Barra de progreso visual
- Generación de accesos directos automática

## Requisitos 
- Windows 7 o superior
- Python 3.6+
- pip (Gestor de paquetes de Python)

## Instalación 
1. Clonar el repositorio:
git clone https://github.com/JACarlin/Planting_Script.git
cd Planting_Script

2. Crear y activar entorno virtual:
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt

## Uso 
python shovel.py

> **Nota:** Ejecutar como Administrador para modificar el startup de todos los usuarios

## Compilar a .exe 
1. Ejecutar comando de compilación:
pyinstaller --onefile --noconsole --icon=icon.ico shovel.py

**Opciones:**
- `--onefile`: Crea un solo ejecutable
- `--noconsole`: Oculta la consola
- `--icon=icon.ico`: Icono personalizado (opcional)

## Consideraciones importantes 
1. Requiere permisos de administrador para todos los usuarios
2. Antivirus pueden detectar falsos positivos
3. Solo funciona en Windows
4. Mantener el .exe en la misma carpeta

---
