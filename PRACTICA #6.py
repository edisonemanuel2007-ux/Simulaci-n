import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
from scipy import stats

# ==========================================
# 1.CÓDIGO BASE DEL GENERADOR
# ==========================================
semilla = 0  # El valor inicial (X0) para iniciar la secuencia de números aleatorios.
a = 5        # Multiplicador del generador congruencial lineal.
c = 1        # Incremento o constante del generador.
m = 4096     # Módulo, el cual define el ciclo máximo de números generados antes de que se repitan.

numeros = []              # Lista para guardar los números enteros generados en la fórmula.
numeros_normalizados = [] # Lista para guardar los números transformados al rango decimal [0 a 1].
x = semilla               # Inicializamos 'x' con el valor de nuestra semilla original.

# Bucle para generar una cantidad 'm' de números (4096 en este caso).
for i in range(m):
    x = (a * x + c) % m                # Fórmula principal del generador congruencial lineal (LCG).
    numeros.append(x)                  # Agrega el nuevo valor de 'x' a la lista de enteros.
    numeros_normalizados.append(x / m) # Divide entre el módulo para obtener un decimal de 0 a 1 y lo guarda.

# ==========================================
# 2. LAS 4 PRUEBAS ESTADÍSTICAS
# ==========================================
datos = np.array(numeros_normalizados) # Convierte la lista en un arreglo de la librería numpy para agilizar matemáticas.
n_datos = len(datos)                   # Obtiene la cantidad total de datos generados (4096).

# A. Prueba de Promedios
m_calc = np.mean(datos)                                      # Obtiene el promedio (media aritmética) de los números generados.
z_prom = abs((m_calc - 0.5) / np.sqrt(1/12 / n_datos))       # Fórmula de la prueba Z: compara si la media se acerca al valor teórico ideal (0.5).
pasa_prom = z_prom < 1.96                                    # Compara contra el valor crítico del 95% de confianza (1.96). True si pasa, False si falla.

# B. Prueba de Frecuencias
freq, _ = np.histogram(datos, bins=5)                        # Divide los datos en 5 "cajas" (intervalos) equitativas y cuenta cuántos caen en cada una.
chi_frec = stats.chisquare(freq, f_exp=[n_datos/5]*5)[0]     # Calcula el estadístico Chi-Cuadrada contrastando lo observado contra una distribución uniforme perfecta.
pasa_frec = chi_frec < 9.488                                 # Si el valor Chi-Cuadrada es menor al crítico (9.488 para 4 grados de libertad), entonces pasa.

# C. Prueba de Corridas (Sobre y debajo de la Mediana)
med = np.median(datos)                                       # Calcula el punto medio (mediana) de los datos generados.
sec = [1 if val > med else 0 for val in datos]               # Genera una lista binaria: anota un 1 si es mayor a la mediana, o un 0 si no lo es.
# Cuenta las corridas sumando 1 cada vez que la secuencia alterna de 0 a 1, o de 1 a 0, más 1 por la corrida inicial.
corridas = 1 + sum(1 for i in range(len(sec)-1) if sec[i] != sec[i+1])
n1, n0 = sum(sec), n_datos - sum(sec)                        # n1 es el total de unos, n0 el total de ceros.
mu_corr = (2 * n0 * n1) / n_datos + 1                        # Calcula cuántas corridas se esperaría tener (Media teórica).
# Calcula la varianza / desviación de las corridas para saber si el margen de error es aceptable.
sigma_corr = np.sqrt((2 * n0 * n1 * (2 * n0 * n1 - n_datos)) / ((n_datos**2) * (n_datos - 1)))
z_corr = abs((corridas - mu_corr) / sigma_corr)              # Estandariza la métrica obteniendo el valor Z.
pasa_corr = z_corr < 1.96                                    # Si Z es menor a 1.96, los datos se consideran independientes.

# D. Prueba de Póker (Utilizando los primeros 3 decimales)
td, un_par, tercia = 0, 0, 0                                 # Contadores inicializados en 0 para las "manos" evaluables.
for num in datos:                                            # Recorre cada uno de los números evaluados.
    s = str(int(num * 1000)).zfill(3)                        # Multiplica por mil para extraer los primeros 3 decimales, lo convierte en texto y si falta, lo rellena con ceros.
    unicos = len(set(s))                                     # Utiliza un conjunto ('set') para eliminar repetidos y ver cuántos dígitos únicos hay en la tercia.
    if unicos == 3: td += 1                                  # Si hay 3 números distintos, es una mano con "Todos diferentes".
    elif unicos == 2: un_par += 1                            # Si hay 2 números distintos, entonces hay "Un par".
    else: tercia += 1                                        # Si sólo hay 1 dígito (Ej. 777), entonces es una "Tercia".
# Calcula Chi-Cuadrada midiendo nuestras manos vs. las probabilidades teóricas (72%, 27%, 1%).
chi_poker = stats.chisquare([td, un_par, tercia], f_exp=[n_datos*0.72, n_datos*0.27, n_datos*0.01])[0]
pasa_poker = chi_poker < 5.991                               # Si el valor Chi es menor a su crítico para 2 grados de libertad (5.991), entonces pasa.

# GUARDAR SI PASAN TODAS
pasan_todas = pasa_prom and pasa_frec and pasa_corr and pasa_poker # Evalúa un AND lógico de las 4 pruebas.
if pasan_todas:                                                    # Si es verdadero y pasó las 4 pruebas simultáneamente...
    with open("parametros_aprobados.txt", "w") as archivo:         # Abre (o crea) un archivo de texto en modo escritura ("w").
        archivo.write(f"Semilla: {semilla}\na: {a}\nc: {c}\nm: {m}\n") # Guarda las constantes ideales allí.

with open("numeros_pseudoaleatorios.txt", "w") as archivo:         # Este archivo siempre se crea para alojar todos los números
    for numero in numeros_normalizados:                            # Recorre toda la lista final...
        archivo.write(f"{numero}\n")                               # Escribe cada decimal en un renglón nuevo.

# ==========================================
# 3. INTERFAZ GRÁFICA ABSOLUTA E INFALIBLE
# ==========================================
ventana = tk.Tk()           # Instancia la clase principal de Tkinter creando la base de la ventana.
ventana.title("PRACTICA #6")# Otorga el título a la barra de estado de la ventana.
ventana.geometry("1200x600")# Fija las dimensiones en 1200 píxeles de ancho por 600 de alto.
ventana.resizable(False, False)# Evita que el usuario congele el Layout cambiando las dimensiones.

# -------- PANEL IZQUIERDO (GENERADOR) --------
frame_izquierdo = tk.Frame(ventana, bg="#f0f0f0")              # Crea un bloque invisible para alojar cosas a la izquierda.
frame_izquierdo.place(x=0, y=0, width=400, height=600)         # Lo amarra en la coordenada inicial y toma 400px de ancho.

# Crea una etiqueta de texto indicando los parámetros iniciales.
lbl_gen = tk.Label(frame_izquierdo, text=f"Parámetros utilizados:\nSemilla = {semilla}\na = {a}\nc = {c}\nm = {m}\n\nNúmeros generados:", justify="left", font=("Arial", 11), bg="#f0f0f0")
lbl_gen.pack(pady=20, padx=20, anchor="w")                     # La aloja aplicando márgenes y la alinea a la izquierda ('w' = west).

# Crea un bloque de texto interactivo con barra deslizante vertical.
txt_area = scrolledtext.ScrolledText(frame_izquierdo, font=("Consolas", 10))
txt_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20)) # Hace que tome todo el espacio restante disponible del bloque izquierdo.

for num in numeros:                          # Recorremos la lista de números ENTIROS (antes de normalizar).
    txt_area.insert(tk.END, f"{num}\n")      # Los escribe gráficamente uno a uno.
txt_area.configure(state='disabled')         # Le pone candado a la caja de texto para que el usuario no pueda editar los datos con el teclado.

# -------- PANEL DERECHO (PRUEBAS) --------
frame_derecho = tk.Frame(ventana, bg="#1e1e2e")                # Crea el panel contrario oscuro estilo tema Dracula.
frame_derecho.place(x=400, y=0, width=800, height=600)         # Lo dibuja desde el pixel 400 rellenando los otros 800 de ancho.

# Agrega la etiqueta del título en texto celeste oscuro.
lbl_titulo = tk.Label(frame_derecho, text=" Implementación de pruebas estadísticas", font=("Arial", 14, "bold"), bg="#1e1e2e", fg="#89b4fa")
lbl_titulo.pack(pady=20)                     # Aplica 20px de margen vertical.

resultado_texto = "SÍ PASARON TODAS" if pasan_todas else "NO PASARON"  # Un condicional dinámico en una sola línea (Operador ternario).
color_resultado = "#a6e3a1" if pasan_todas else "#f38ba8"              # Cambia a verde brillante si pasan, o rojo brillante si no.
# Crea un gran letrero anunciando el veredicto definitivo.
lbl_resultado = tk.Label(frame_derecho, text=f"¿Pasan todas las pruebas?: {resultado_texto}", font=("Arial", 12, "bold"), bg="#1e1e2e", fg=color_resultado)
lbl_resultado.pack()                         # Lo plasma en el diseño.

notebook = ttk.Notebook(frame_derecho)       # Instancia un 'Cuaderno', esto habilita la posibilidad de usar pestañas (Tabs).
notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20) # Fuerza a ocupar el espacio residual.

estilo = ttk.Style()                         # Modificador estético para repintar las paletas de color estándar del OS.
estilo.theme_use('default')                  # Obliga el re-diseño con el tema predeterminado.
# Configura los colores de fondo e interactividad para cada que cambies de pestaña se vea estético.
estilo.configure("TNotebook", background="#1e1e2e", borderwidth=0)
estilo.configure("TNotebook.Tab", background="#313244", foreground="white", padding=[10, 5])
estilo.map("TNotebook.Tab", background=[("selected", "#89b4fa")], foreground=[("selected", "black")])

# Definimos una pequeña función reutilizable que nos evite reescribir tanto código y cree los espacios gráficos de las pestañas.
def crear_pestana(titulo, texto):
    f = tk.Frame(notebook, bg="#252538")             # Construye el contenedor para esta pestaña.
    notebook.add(f, text=titulo)                     # Le dice al Cuaderno que acaba de nacer un subapartado nuevo.
    # Diseña un bloque de texto gigante envuelto (wrap='word') en los limites de la pantalla y colores grises/azules.
    t = tk.Text(f, font=("Arial", 11), bg="#252538", fg="#cdd6f4", padx=20, pady=20, wrap="word", borderwidth=0)
    t.pack(fill=tk.BOTH, expand=True)                # Imprime el espacio.
    t.insert("1.0", texto)                           # Inyecta tu texto variable adentro.
    t.config(state="disabled")                       # Vuelve a aplicarle candado para evitar que el usuario de click y borre o altere la interfaz.

# Textos, el sufijo 'f' indica cadenas formateadas para incluir variables ({}) dinámicamente.
t_prom = (f"📌 EL PORQUÉ DE ESTA PRUEBA (OBJETIVO):\n"
          f"Verificar que el promedio de los números sea cercano a 0.5.\n\n"
          f"📊 CÁLCULOS Y DATOS:\n"
          f" - Media calculada: {m_calc:.5f}\n"
          f" - Estadístico Z: {z_prom:.4f}\n"
          f" - Valor crítico (95%): 1.96\n\n"
          f"✅ RESPUESTA FINAL:\n"
          f"   >> {'PASAN LA PRUEBA' if pasa_prom else 'FALLAN LA PRUEBA'} <<\n\n"
          f"🧠 JUSTIFICACIÓN:\n"
          f"{'Z es menor a 1.96, la desviación de 0.5 es natural.' if pasa_prom else 'El promedio se desvió demasiado.'}")

t_frec = (f"📌 EL PORQUÉ DE ESTA PRUEBA (OBJETIVO):\n"
          f"Comprobar que los números se distribuyan parejo en 5 intervalos.\n\n"
          f"📊 CÁLCULOS Y DATOS:\n"
          f" - Frecuencias observadas: {list(freq)}\n"
          f" - Chi-Cuadrada: {chi_frec:.4f}\n"
          f" - Valor crítico: 9.488\n\n"
          f"✅ RESPUESTA FINAL:\n"
          f"   >> {'PASAN LA PRUEBA' if pasa_frec else 'FALLAN LA PRUEBA'} <<\n\n"
          f"🧠 JUSTIFICACIÓN:\n"
          f"{'Chi-Cuadrada está bajo el límite, hay buena distribución.' if pasa_frec else 'Los números se amontonan.'}")

t_corr = (f"📌 EL PORQUÉ DE ESTA PRUEBA (OBJETIVO):\n"
          f"Evalúa si el orden de los números es independiente (sin patrones predecibles).\n\n"
          f"📊 CÁLCULOS Y DATOS:\n"
          f" - Corridas: {corridas}\n"
          f" - Estadístico Z: {z_corr:.4f}\n"
          f" - Valor crítico: 1.96\n\n"
          f"✅ RESPUESTA FINAL:\n"
          f"   >> {'PASAN LA PRUEBA' if pasa_corr else 'FALLAN LA PRUEBA'} <<\n\n"
          f"🧠 JUSTIFICACIÓN:\n"
          f"{'Z es menor a 1.96, no hay un patrón evidente en la secuencia.' if pasa_corr else 'Hay un patrón de dependencia.'}")

t_poker = (f"📌 EL PORQUÉ DE ESTA PRUEBA (OBJETIVO):\n"
           f"Verifica la aleatoriedad de los dígitos individuales evaluando 'manos' de póker.\n\n"
           f"📊 CÁLCULOS Y DATOS:\n"
           f" - Diferentes: {td} | Pares: {un_par} | Tercias: {tercia}\n"
           f" - Chi-Cuadrada: {chi_poker:.4f}\n"
           f" - Valor crítico: 5.991\n\n"
           f"✅ RESPUESTA FINAL:\n"
           f"   >> {'PASAN LA PRUEBA' if pasa_poker else 'FALLAN LA PRUEBA'} <<\n\n"
           f"🧠 JUSTIFICACIÓN:\n"
           f"{'Las combinaciones encajan en la teoría probabilística.' if pasa_poker else 'Hay vicio en los dígitos.'}")

# Mandamos llamar la función iterativa con los 4 textos dinámicos previos.
crear_pestana("1. Promedios", t_prom)
crear_pestana("2. Frecuencias", t_frec)
crear_pestana("3. Corridas", t_corr)
crear_pestana("4. Póker", t_poker)

# Este es el comando fundamental, congela la ejecución del script aquí e invoca en pantalla la aplicación
# hasta que el usuario decida cerrarla manualmente dándole a la 'X' superior de su sistema operativo.
ventana.mainloop()