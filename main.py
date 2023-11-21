import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time

class Proceso:
    def __init__(self, nombre, tiempo, prioridad):
        self.nombre = nombre
        self.tiempo = tiempo
        self.prioridad = prioridad

class ProcesoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")

        self.procesos = []
        self.resultado_text = tk.Text(root, height=15, width=40, state="disabled")
        self.resultado_text.grid(row=0, column=1, rowspan=4)

        self.cargar_btn = ttk.Button(root, text="Cargar procesos", command=self.cargar_procesos)
        self.cargar_btn.grid(row=0, column=0, padx=10, pady=10)

        self.simular_btn = ttk.Button(root, text="Simular algoritmo", command=self.simular_algoritmo)
        self.simular_btn.grid(row=1, column=0, padx=10, pady=10)

        self.algoritmo_var = tk.StringVar()
        self.algoritmo_var.set("RR")  # Valor predeterminado
        self.algoritmo_combo = ttk.Combobox(root, textvariable=self.algoritmo_var, values=["RR", "SJF", "FIFO", "PRI"])
        self.algoritmo_combo.grid(row=2, column=0, padx=10, pady=10)

        self.nuevo_proceso_entry = ttk.Entry(root, width=10)
        self.nuevo_proceso_entry.grid(row=3, column=0, padx=10, pady=10)

        self.agregar_proceso_btn = ttk.Button(root, text="Agregar nuevo proceso", command=self.agregar_proceso)
        self.agregar_proceso_btn.grid(row=4, column=0, padx=10, pady=10)

    def cargar_procesos_desde_archivo(self, nombre_archivo):
        procesos = []
        try:
            with open(nombre_archivo, "r") as archivo:
                lineas = archivo.readlines()
                for linea in lineas:
                    datos = linea.strip().split(",")
                    nombre = datos[0]
                    tiempo = int(datos[1])
                    prioridad = int(datos[2])
                    procesos.append(Proceso(nombre, tiempo, prioridad))
        except FileNotFoundError:
            print("El archivo especificado no existe.")
        return procesos

    def cargar_procesos(self, archivo_nombre="procesos.txt"):
        if archivo_nombre:
            self.procesos.extend(self.cargar_procesos_desde_archivo(archivo_nombre))

    def agregar_proceso(self):
        nombre = self.nuevo_proceso_entry.get()
        if nombre:
            tiempo = int(tk.simpledialog.askstring("Tiempo", f"Ingrese el tiempo de duración del proceso {nombre}: "))
            prioridad = int(tk.simpledialog.askstring("Prioridad", f"Ingrese la prioridad del proceso {nombre}: "))
            self.procesos.append(Proceso(nombre, tiempo, prioridad))

    def actualizar_resultado_text(self, resultado):
        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, "end")
        for proceso, tiempo in resultado:
            self.resultado_text.insert("end", f"{proceso}: Tiempo total = {tiempo} unidades de tiempo\n")
        self.resultado_text.config(state="disabled")

    def simular_algoritmo(self):
        algoritmo = self.algoritmo_var.get()
        if not self.procesos:
            print("No hay procesos para simular. Por favor, cargue o agregue procesos primero.")
            return

        # Solicitar el quantum aquí, en el hilo principal
        quantum = None
        if algoritmo == "RR":
            quantum = int(tk.simpledialog.askstring("Quantum", "Ingrese el quantum para Round Robin: "))

        # Pasar el quantum como argumento al hilo
        t = threading.Thread(target=self.simular_algoritmo_en_hilo, args=(algoritmo, quantum))
        t.start()

    def simular_algoritmo_en_hilo(self, algoritmo, quantum):
        if algoritmo == "RR":
            resultado = self.round_robin(self.procesos.copy(), quantum)
        elif algoritmo == "SJF":
            resultado = self.sjf(self.procesos.copy())
        elif algoritmo == "FIFO":
            resultado = self.fifo(self.procesos.copy())
        elif algoritmo == "PRI":
            resultado = self.prioridades(self.procesos.copy())
        else:
            print("Algoritmo no válido.")
            return

        self.actualizar_resultado_text(resultado)

    def round_robin(self, procesos, quantum):
        procesos = procesos.copy()
        tiempo_total = 0
        resultado = []

        while procesos:
            proceso_actual = procesos.pop(0)
            if proceso_actual.tiempo > quantum:
                proceso_actual.tiempo -= quantum
                tiempo_total += quantum
                procesos.append(proceso_actual)
            else:
                tiempo_total += proceso_actual.tiempo
                resultado.append((proceso_actual.nombre, tiempo_total))

        return resultado

    def sjf(self, procesos):
        procesos.sort(key=lambda x: x.tiempo)
        tiempo_total = 0
        resultado = []

        for proceso in procesos:
            resultado.append((proceso.nombre, tiempo_total))
            tiempo_total += proceso.tiempo

        return resultado

    def fifo(self, procesos):
        tiempo_total = 0
        resultado = []

        for proceso in procesos:
            tiempo_total += proceso.tiempo
            resultado.append((proceso.nombre, tiempo_total))

        return resultado

    def prioridades(self, procesos):
        procesos.sort(key=lambda x: x.prioridad)
        tiempo_total = 0
        resultado = []

        for proceso in procesos:
            tiempo_total += proceso.tiempo
            resultado.append((proceso.nombre, tiempo_total))

        return resultado


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcesoApp(root)
    root.mainloop()
