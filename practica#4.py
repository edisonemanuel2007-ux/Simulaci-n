import tkinter as tk
from tkinter import scrolledtext

# --- Parámetros del generador ---
semilla = 0
a = 5        # Constante multiplicativa
c = 1        # Constante aditiva
m = 4096     # Módulo del generador

numeros = []
x = semilla  # La variable x inicia con el valor de la semilla

# --- Generar los números ---
# Se repite el proceso 4096 veces para obtener el periodo completo
for i in range(m):
    x = (a * x + c) % m
    numeros.append(x)

# --- Guardar parámetros ---
with open("parametros.txt", "w") as archivo:
    archivo.write(f"Semilla: {semilla}\n")
    archivo.write(f"a: {a}\n")
    archivo.write(f"c: {c}\n")
    archivo.write(f"m: {m}\n")

# --- Guardar números ---
with open("numeros_pseudoaleatorios.txt", "w") as archivo:
    for numero in numeros:
        archivo.write(f"{numero}\n")

# --- Crear ventana ---
ventana = tk.Tk()
ventana.title("Generador de Números Pseudoaleatorios")
ventana.geometry("500x600")

# Etiqueta de parámetros
label_params = tk.Label(ventana, text=f"Parámetros utilizados:\nSemilla = {semilla}\na = {a}\nc = {c}\nm = {m}\n\nNúmeros generados:", justify="left")
label_params.pack(pady=10)

# Caja de texto con scroll
txt_area = scrolledtext.ScrolledText(ventana, width=50, height=20)
txt_area.pack(pady=10)

# Insertar números en la interfaz
for num in numeros:
    txt_area.insert(tk.END, f"{num}\n")

# Configurar como solo lectura
txt_area.configure(state='disabled')

ventana.mainloop()