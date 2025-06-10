import numpy as np
import sys

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import datetime as dt
from datetime import timedelta
from time import sleep

def biorritmos():
    figura = plt.figure(figsize=(6, 5), facecolor='azure', edgecolor='indianred', linewidth=2)

    win = tb.Window(themename='yeti')  
    win.title('Analizador de Biorrítmos')
    win.geometry('1000x700')

    ttk.Style(win).configure('.', font=('Arial', 12), padding=8)

    lienzo = FigureCanvasTkAgg(figure=figura, master=win).get_tk_widget()
    lienzo.pack(side=tk.LEFT)

    frameDatos = ttk.Frame(win, width=400)
    frameDatos.pack(side=tk.LEFT)

    nacimiento = Fecha(dt.date(dt.now()))
    inicio = Fecha(dt.date(dt.now()))
    ahora = Fecha(dt.date(dt.now()))
    velocidad = tk.DoubleVar(frameDatos, value=0.5)
    activo = tk.BooleanVar(frameDatos, value=False)

    cogeDatos(frameDatos, nacimiento, inicio, velocidad)

    ttk.Separator(frameDatos).grid(row=40, pady=60)

    frameComandos = ttk.Frame(frameDatos)
    frameComandos.grid(row=50, column=10, columnspan=20, sticky=tk.S, pady=20)
    creaComandos(win, frameComandos, figura, nacimiento, inicio, ahora, velocidad, activo)

    win.mainloop()

    sys.exit()


class Fecha(tk.Variable):
    def __init__(self, fecha):
        self.fecha = fecha
    
    def set(self, fecha):
        self.fecha = fecha

    def get(self):
        return self.fecha
    
    def __str__(self):
        return dt.strftime(self.fecha, '%d/%B/%Y')
    
    def __add__(self, other):
        return Fecha(self.fecha + timedelta(other))
        

def cogeFecha(raiz, fecha, texto, fila):
    labelFecha = ttk.Label(raiz, text=texto)
    labelFecha.grid(row=fila, column=10, sticky=tk.W)

    def cogeFecha():
        calendario = tb.Querybox()
        valor = calendario.get_date(startdate=fecha.get(),
                                    firstweekday=0)        
        fecha.set(valor)
        botonFecha.configure(text=str(fecha))

    botonFecha = ttk.Button(raiz, text=str(fecha), command=cogeFecha, style='Outline.TButton', width=16)
    botonFecha.grid(row=fila, column=20, sticky=tk.E, padx=8)


# Fijamos FPS_MAX según medición de la *frame* mínima en el ordenador de albino
FPS_MIN, FPS_MAX = 0.5, 60

def cogeVelocidad(raiz, velocidad, fila):
    fps = FPS_MIN + (FPS_MAX - FPS_MIN) * velocidad.get()
    label = tk.StringVar(raiz, value=f'Velocidad ({fps:.1f} fps): ')
    labelVelocidad = ttk.Label(raiz, textvariable=label)
    labelVelocidad.grid(row=fila, column=10, sticky=tk.W)

    def meteVelocidad(strVelocidad):
        fps = FPS_MIN + (FPS_MAX - FPS_MIN) * velocidad.get()
        label.set(f'Velocidad ({fps:.1f} fps): ')

    deslizaVelocidad = ttk.Scale(raiz, variable=velocidad, value=velocidad.get(), length=210, command=meteVelocidad)
    deslizaVelocidad.grid(row=fila, column=20, sticky=tk.E, padx=12)


def cogeDatos(frameDatos, nacimiento, inicio, velocidad):
    cogeFecha(frameDatos, nacimiento, 'Fecha de nacimiento: ', fila=10)
    cogeFecha(frameDatos, inicio, 'Fecha de inicio: ', fila=20)
    cogeVelocidad(frameDatos, velocidad, fila=30)

    frameDatos.columnconfigure(20, minsize=220, weight=1)


def ritmos(t):
    return np.sin(2 * np.pi * t / 23) ** 2 + np.sin(2 * np.pi * t / 28) ** 2 + np.sin(2 * np.pi * t / 33) ** 2


def dibuja(figura, ax, lineas, nacimiento, ahora):
    inicio = (ahora.get() - nacimiento.get()).days - 50
    final = (ahora.get() - nacimiento.get()).days + 50

    t = np.linspace(inicio, final, 1000)

    lineas[0].set_xdata(t)
    lineas[0].set_ydata(ritmos(t))

    lineas[1].set_xdata([inicio + 50, inicio + 50])
    lineas[1].set_ydata([-1, ritmos(inicio + 50)])

    fechas = np.arange(30.4375 * (inicio // 30.4375 + 1), 30.4375 * (final // 30.4375 + 1), 30.4375)
    ax.set_xticks(fechas)
    ax.set_xticklabels([dt.strftime(nacimiento.get() + timedelta(fecha), '%d/%b/%Y') for fecha in fechas], fontsize=12)
    ax.set_xlim(inicio, final)
    ax.set_title(f'{str(ahora)}', fontsize=16)

    figura.canvas.draw()
    figura.canvas.flush_events()


def reproduce(pausaContinua, figura, ax, lineas, nacimiento, inicio, ahora, velocidad, activo, iniciar):
    def reproduce():
        if iniciar:
            ahora.set(inicio.get())
            activo.set(False)

        if activo.get():
            pausaContinua.set('Continúa')
            activo.set(False)
        else:
            pausaContinua.set('Pausa')
            activo.set(True)

            while activo.get():
                dibuja(figura, ax, lineas, nacimiento, ahora)
                ahora.set(ahora.get() + timedelta(1))
                fps = FPS_MIN + (FPS_MAX - FPS_MIN) * velocidad.get()
                retardo = 1 / fps - 1 / FPS_MAX
                sleep(retardo)

    return reproduce


def termina(raiz, activo):
    def termina():
        activo.set(False)
        raiz.quit()
        raiz.destroy()

    return termina


def creaComandos(raiz, frameComandos, figura, nacimiento, inicio, ahora, velocidad, activo):
    ax = figura.subplots()
    ax.set(xlim=(-50, 50), ylim=(0, 3.2), xticks=[], yticks=[])
    ax.plot([], [])
    ax.plot([], [], ':ro')

    lineas = ax.lines

    dibuja(figura, ax, lineas, nacimiento, inicio)

    pausaContinua = tk.StringVar(frameComandos, value='Continúa')

    botonIniciar = tb.Button(frameComandos,
                             text='Inicia',
                             command=reproduce(pausaContinua, figura, ax, lineas, nacimiento, inicio, ahora, velocidad, activo, iniciar=True),
                             width=8)
    botonIniciar.pack(side=tk.LEFT, padx=8)

    botonPausar = tb.Button(frameComandos,
                            textvariable=pausaContinua,
                            command=reproduce(pausaContinua, figura, ax, lineas, nacimiento, inicio, ahora, velocidad, activo, iniciar=False),
                            width=8)
    botonPausar.pack(side=tk.LEFT, padx=8)

    botonTerminar = tb.Button(frameComandos,
                              text='Termina',
                              command=termina(raiz, activo),
                              width=8)
    botonTerminar.pack(side=tk.LEFT, padx=8)


if __name__ == '__main__':
    biorritmos()