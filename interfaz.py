import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from funcionalidad import solucion, leer_entrada_desde_archivo

def cargar_archivo():
    nombre_archivo = filedialog.askopenfilename(title="Seleccione el archivo de entrada", filetypes=[("Archivos de texto", "*.txt")])
    if nombre_archivo:
        try:
            poblacion, empresarial, ubicaciones_existentes, n_sedes = leer_entrada_desde_archivo(nombre_archivo)
            entrada_label.config(text=f"Archivo cargado: {nombre_archivo}")
            global datos
            datos = (poblacion, empresarial, ubicaciones_existentes, n_sedes)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {e}")

def ejecutar_solucion():
    if 'datos' not in globals():
        messagebox.showwarning("Advertencia", "Debe cargar un archivo primero.")
        return
    poblacion, empresarial, ubicaciones_existentes, n_sedes = datos
    resultado = solucion(poblacion, empresarial, ubicaciones_existentes, n_sedes)
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, resultado)

def guardar_salida():
    if resultado_text.get("1.0", tk.END).strip() == "":
        messagebox.showwarning("Advertencia", "No hay resultados para guardar.")
        return
    nombre_archivo = filedialog.asksaveasfilename(title="Guardar resultado", defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if nombre_archivo:
        try:
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(resultado_text.get("1.0", tk.END))
            messagebox.showinfo("Información", "Resultado guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Matrices y Solución")
ventana.geometry("600x500")

# Etiqueta y botón para cargar archivo
entrada_label = ttk.Label(ventana, text="Cargue un archivo de entrada para comenzar.")
entrada_label.pack(pady=10)

cargar_boton = ttk.Button(ventana, text="Cargar Archivo", command=cargar_archivo)
cargar_boton.pack(pady=5)

# Botón para ejecutar la solución
ejecutar_boton = ttk.Button(ventana, text="Ejecutar Solución", command=ejecutar_solucion)
ejecutar_boton.pack(pady=10)

# Área de texto para mostrar el resultado
resultado_text = tk.Text(ventana, wrap=tk.WORD, height=15, width=70)
resultado_text.pack(pady=10)

# Botón para guardar la salida
guardar_boton = ttk.Button(ventana, text="Guardar Resultado", command=guardar_salida)
guardar_boton.pack(pady=10)

ventana.mainloop()
