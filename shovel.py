import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import win32com.client
import sys

class StartupApp:
    def __init__(self, master):
        self.master = master
        master.title("Configurador de Startup")
        master.geometry("500x300")

        # Variables
        self.all_users = tk.BooleanVar()
        self.file_path = tk.StringVar()
        self.dest_path = tk.StringVar(value=os.environ['SystemRoot'])  # C:\Windows por defecto

        # Widgets
        self.create_widgets()
        self.all_users.trace_add('write', self.toggle_destination)

    def create_widgets(self):
        # Marco principal
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Selección de archivo
        ttk.Label(main_frame, text="Archivo a copiar:").grid(row=0, column=0, sticky=tk.W)
        file_entry = ttk.Entry(main_frame, textvariable=self.file_path, width=40)
        file_entry.grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Examinar", command=self.browse_file).grid(row=0, column=2)

        # Opción para todos los usuarios
        ttk.Checkbutton(main_frame, 
                       text="Agregar al startup de todos los usuarios",
                       variable=self.all_users).grid(row=1, column=0, columnspan=3, pady=10, sticky=tk.W)

        # Ruta de destino
        ttk.Label(main_frame, text="Ruta de destino:").grid(row=2, column=0, sticky=tk.W)
        self.dest_entry = ttk.Entry(main_frame, textvariable=self.dest_path, width=40)
        self.dest_entry.grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, 
                  text="Ejecutar", 
                  command=self.execute_operation).grid(row=3, column=0, columnspan=3, pady=20)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, pady=10)

    def browse_file(self):
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            initialdir=initial_dir,
            filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)

    def toggle_destination(self, *args):
        if self.all_users.get():
            self.dest_entry.config(state=tk.DISABLED)
            self.dest_path.set(os.environ['SystemRoot'])  # C:\Windows
        else:
            self.dest_entry.config(state=tk.NORMAL)

    def execute_operation(self):
        file_path = self.file_path.get()
        dest_dir = self.dest_path.get()
        all_users = self.all_users.get()

        if not file_path:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return

        try:
            self.progress['value'] = 0
            self.update_progress(25, "Copiando archivo...")
            
            # Copiar archivo
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, file_name)
            shutil.copy(file_path, dest_path)
            
            self.update_progress(50, "Creando acceso directo...")
            
            # Crear acceso directo
            if all_users:
                startup_folder = os.path.join(
                    os.environ['ProgramData'],
                    'Microsoft\Windows\Start Menu\Programs\Startup'
                )
            else:
                startup_folder = os.path.join(
                    os.environ['APPDATA'],
                    'Microsoft\Windows\Start Menu\Programs\Startup'
                )
            
            self.create_shortcut(dest_path, startup_folder, file_name)
            
            self.update_progress(100, "Operación completada!")
            messagebox.showinfo("Éxito", "Archivo configurado correctamente en el startup")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            self.progress['value'] = 0

    def update_progress(self, value, message):
        self.progress['value'] = value
        self.master.title(message)
        self.master.update_idletasks()

    def create_shortcut(self, target_path, startup_folder, file_name):
        if not os.path.exists(startup_folder):
            os.makedirs(startup_folder)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut_name = f"{os.path.splitext(file_name)[0]}.lnk"
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = StartupApp(root)
    
    # Verificar si es Windows
    if os.name != "nt":
        messagebox.showerror("Error", "Esta aplicación solo funciona en Windows")
        sys.exit(1)
    
    root.mainloop()