import tkinter as tk
from tkinter import scrolledtext
import random

class SimulacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Práctica #3 - Simulación")
        self.root.geometry("800x780")
        
        # Decoración de la ventana (Fondo azul marino)
        self.root.configure(bg="navy")
        
        # Estilos personalizados sin líneas blancas
        estilo_label = {"bg": "navy", "fg": "white", "font": ('Arial', 11, 'bold')}
        estilo_texto = {"bg": "navy", "fg": "white", "insertbackground": "white", 
                        "bd": 0, "highlightthickness": 0, "font": ('Consolas', 10)}
        self.estilo_boton = {"bg": "purple", "fg": "white", "font": ('Arial', 10, 'bold'), 
                        "bd": 0, "highlightthickness": 0, "activebackground": "#9932CC", "activeforeground": "white"}

        # --- SECCIÓN: EJERCICIOS 1 y 2 (Independientes, con botón) ---
        frame_arriba = tk.Frame(root, bg="navy")
        frame_arriba.pack(pady=10, fill="x", padx=20)
        
        tk.Label(frame_arriba, text="--- EJERCICIO 1 y 2: Cuadrado Medio ---", **estilo_label).pack(pady=5)
        
        # Contenedor para alinear los botones
        frame_botones = tk.Frame(frame_arriba, bg="navy")
        frame_botones.pack(pady=5)

        self.btn_generar = tk.Button(frame_botones, text="Generar 20 números", command=self.siguiente_cuadrado_medio, **self.estilo_boton)
        self.btn_generar.grid(row=0, column=0, padx=10, ipadx=10, ipady=5)

        self.btn_reiniciar = tk.Button(frame_botones, text="Reiniciar", command=self.reiniciar_secuencia, **self.estilo_boton)
        self.btn_reiniciar.grid(row=0, column=1, padx=10, ipadx=10, ipady=5)
        self.btn_reiniciar.config(state="disabled") 
        
        self.lbl_estado = tk.Label(frame_arriba, text="Presiona el botón para generar. Semilla inicial: 7326", bg="navy", fg="#00FFFF")
        self.lbl_estado.pack(pady=5)

        self.txt_ej1 = tk.Text(frame_arriba, height=6, width=90, **estilo_texto)
        self.txt_ej1.pack(pady=5)

        # Variables de control para Cuadrado Medio
        self.semilla_inicial = 7326
        self.actual = self.semilla_inicial
        self.historial = {self.semilla_inicial: 0} 
        self.total_generados = 0
        self.consecutivos = 0
        self.ultimo_valor = None

        # Línea separadora morada
        tk.Frame(root, height=3, bg="purple").pack(fill="x", padx=20, pady=5)

        # --- SECCIÓN: EJERCICIOS 3, 4 y 5 (Independientes, automáticos) ---
        frame_abajo = tk.Frame(root, bg="navy")
        frame_abajo.pack(pady=10, fill="both", expand=True, padx=20)
        
        tk.Label(frame_abajo, text="--- EJERCICIOS 3, 4 y 5: Congruencial ---", **estilo_label).pack(pady=5)
        
        self.txt_area = scrolledtext.ScrolledText(frame_abajo, width=90, height=18, **estilo_texto)
        self.txt_area.pack(pady=5)
        
        self.resolver_congruenciales()

    def siguiente_cuadrado_medio(self):
        nuevos_numeros = []
        mensajes_rep = []

        # Bucle del 1 al 20
        for i in range(1, 21):
            self.total_generados += 1
            cuadrado = self.actual ** 2
            s_cuadrado = str(cuadrado).zfill(8)
            medio = int(s_cuadrado[2:6])

            # Regla: máximo 3 repeticiones consecutivas
            if medio == self.ultimo_valor:
                self.consecutivos += 1
                if self.consecutivos >= 3:
                    self.actual = (self.actual + 1111) % 10000 
                    self.consecutivos = 1
                    cuadrado = self.actual ** 2
                    medio = int(str(cuadrado).zfill(8)[2:6])
            else:
                self.consecutivos = 1
                self.ultimo_valor = medio

            # Rastrear repetición GLOBAL
            if medio in self.historial:
                pos_prev = self.historial[medio]
                mensajes_rep.append(f"-> Repetición: {medio} (Visto en pos. {pos_prev} y ahora {self.total_generados})")
            else:
                self.historial[medio] = self.total_generados
            
            nuevos_numeros.append(medio)
            self.actual = medio

        # Mostrar resultados en pantalla
        self.txt_ej1.delete(1.0, tk.END)
        self.txt_ej1.insert(tk.END, f"Números generados:\n{nuevos_numeros}\n\n")
        if mensajes_rep:
            self.txt_ej1.insert(tk.END, "\n".join(mensajes_rep))
        
        self.btn_reiniciar.config(state="normal")
        self.lbl_estado.config(text=f"Total generados: {self.total_generados}. Sigue presionando el botón.", fg="#00FFFF")

    def reiniciar_secuencia(self):
        self.semilla_inicial = 7326
        self.actual = self.semilla_inicial
        self.historial = {self.semilla_inicial: 0}
        self.total_generados = 0
        self.consecutivos = 0
        self.ultimo_valor = None
        self.txt_ej1.delete(1.0, tk.END)
        self.btn_reiniciar.config(state="disabled")
        self.lbl_estado.config(text=f"Secuencia reiniciada. Semilla original: {self.semilla_inicial}. Presiona generar.", fg="#00FFFF")

    def resolver_congruenciales(self):
        resultados = ""
        resultados += "EJERCICIO 3 (a=13, b=7, M=1024):\n"
        for s in [473, 8432, 4728]: 
            rep, pos1, pos2 = self.congruencial(13, 7, 1024, s)
            if rep is not None:
                resultados += f" - Semilla {s}: Se repite el valor {rep} en las posiciones {pos1} y {pos2}.\n"
            else:
                resultados += f" - Semilla {s}: Sin repetición.\n"
        resultados += "\nEJERCICIO 4 (a=25, b=13, M=2048):\n"
        for s in [2537, 4694, 6598]:
            rep, pos1, pos2 = self.congruencial(25, 13, 2048, s)
            if rep is not None:
                resultados += f" - Semilla {s}: Se repite el valor {rep} en las posiciones {pos1} y {pos2}.\n"
            else:
                resultados += f" - Semilla {s}: Sin repetición.\n"
        resultados += "\nEJERCICIO 5 (a=45, b=23, M=512, Semilla=9825, 20 números):\n"
        lista5, rep5, pos5_1, pos5_2 = self.congruencial_n(45, 23, 512, 9825, 20)
        resultados += f"Primeros 20 números:\n{lista5}\n"
        if rep5 is not None:
            resultados += f"--> Hubo repetición en el valor {rep5} (Visto en posiciones {pos5_1} y {pos5_2}).\n"
        else:
            resultados += "--> No se encontró repetición en estos primeros 20 números.\n"
        self.txt_area.insert(tk.INSERT, resultados)
        self.txt_area.config(state='disabled')

    def congruencial(self, a, b, m, x0):
        # ELIMINADO: El bloque 'if' que forzaba valores incorrectos
        historial = {x0: 0}
        actual = x0
        for i in range(1, 5000): 
            actual = (a * actual + b) % m
            if actual in historial: return actual, historial[actual], i
            historial[actual] = i
        return None, None, None

    def congruencial_n(self, a, b, m, x0, n):
        lista = []
        historial = {x0: 0}
        actual = x0
        rep = None
        pos1 = None
        pos2 = None
        for i in range(1, n + 1):
            actual = (a * actual + b) % m
            if actual in historial and rep is None:
                rep = actual
                pos1 = historial[actual]
                pos2 = i
            historial[actual] = i
            lista.append(actual)
        return lista, rep, pos1, pos2

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacionApp(root)
    root.mainloop()