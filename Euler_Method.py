import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols,sympify,lambdify
import math
from decimal import getcontext
getcontext().prec=100
    
from matplotlib.figure import Figure

# Interfaz Base
app=tk.Tk()
graph_frame = tk.Frame(app, width=1000, height=1000, bg="lightgrey")
graph_frame.place(relx=0.43, rely=0.13)  # Ubicar el marco del gráfico
# widget_frame = tk.Frame(app, width=400, height=300, bg="white")
# widget_frame.place(relx=0.5, rely=0.6, anchor="n")  # Ubicar los otros widgets
fig = Figure(figsize=(6, 4), dpi=140)
ax = fig.add_subplot(111) 
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
toolbar = NavigationToolbar2Tk(canvas, graph_frame, pack_toolbar=False)
toolbar.pack()
toolbar.update()

def set_ax():
    ax.set_title("Método de Euler.")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.grid()

set_ax()

# Campos
dydx=tk.StringVar(app)
x0=tk.StringVar(app)
y0=tk.StringVar(app)
h=tk.StringVar(app)
x_final=tk.StringVar(app)
y_x_final=tk.StringVar(app)
error=tk.StringVar(app)

# Dimensiones
app.geometry("800x600")

# Color de fondo
app.configure(background="#f1ede3")

# Titulo
tk.Wm.wm_title(app, "Solucionador de Ecuaciones Diferenciales Ordinarias.")

# Parametros
TipoFuente="Courier"
SizeFuente=12
ColorBg="#f1ede3"
ColorE="#ddd4c2"
rh=0.05
rw=0.15

# Etiquetas y Entradas
# y'=
e1=tk.Label(app, text="y'=", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e1.pack()
e1.place(relx=0.03, rely=0.13, relheight=0.05, relwidth=0.1)
i1=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=dydx)
i1.pack()
i1.place(relx=0.13, rely=0.13, relheight=rh, relwidth=rw)

# x0:
e2=tk.Label(app, text="x0:", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e2.pack()
e2.place(relx=0.03, rely=0.2, relheight=0.05, relwidth=0.1)
i2=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=x0)
i2.pack()
i2.place(relx=0.13, rely=0.2, relheight=rh, relwidth=rw)

# y0:
e3=tk.Label(app, text="y0:", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e3.pack()
e3.place(relx=0.03, rely=0.27, relheight=0.05, relwidth=0.1)
i3=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=y0)
i3.pack()
i3.place(relx=0.13, rely=0.27, relheight=rh, relwidth=rw)

# Paso h:
e4=tk.Label(app, text="Paso h:", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e4.pack()
e4.place(relx=0.03, rely=0.34, relheight=0.05, relwidth=0.1)
i4=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=h)
i4.pack()
i4.place(relx=0.13, rely=0.34, relheight=rh, relwidth=rw)

# x_final:
e5=tk.Label(app, text="x_final:", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e5.pack()
e5.place(relx=0.03, rely=0.41, relheight=0.05, relwidth=0.1)
i5=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=x_final)
i5.pack()
i5.place(relx=0.13, rely=0.41, relheight=rh, relwidth=rw)

# y(x_final):
e6=tk.Label(app, text="y(x_final):", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e6.pack()
e6.place(relx=0.03, rely=0.55, relheight=0.05, relwidth=0.1)
i6=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=y_x_final, state="readonly")
i6.pack()
i6.place(relx=0.13, rely=0.55, relheight=rh, relwidth=rw)

# Error:
e7=tk.Label(app, text="Error:", font=(TipoFuente, SizeFuente), bg=ColorBg, justify="center")
e7.pack()
e7.place(relx=0.33, rely=0.9, relheight=0.05, relwidth=0.1)
i7=tk.Entry(app, font=(TipoFuente, SizeFuente), bg=ColorE, fg="black", justify="center", textvariable=error, state="readonly")
i7.pack()
i7.place(relx=0.43, rely=0.9, relheight=rh, relwidth=0.52)

# Logica
def limpiar():
    dydx.set("")
    x0.set("")
    y0.set("")
    h.set("")
    x_final.set("")
    y_x_final.set("")
    error.set("")
    ax.clear()
    set_ax()
    canvas.draw()

# Metodo de Euler
def euler_method(_x0, _y0, _h, _x_final, _f):
    _x0=float(_x0)
    _y0=float(_y0)
    _h=float(_h)
    _x_final=float(_x_final)
    if _x0+10000*_h<_x_final:
        error.set("!!Error: An unexpected error occurred. Please check your input and try again.")
        return [], []
    _x_values=[_x0]
    _y_values=[_y0]
    while _x0<_x_final:
        _y0+=_h*_f(_x0,_y0,math.e)
        _x0+=_h
        _x_values.append(round(_x0,8))
        _y_values.append(round(_y0,8))
    return _x_values, _y_values

def resolver_ecuacion(_input, _x0, _y0, _h, _x_final):
    try:
        x, y, e = symbols('x y e', real = True)
        input = _input
        expr = sympify(input)
        f = lambdify((x,y,e), expr)
        return euler_method(_x0,_y0,_h,_x_final,f)
    except:
        error.set("!!Error: An unexpected error occurred. Please check your input and try again.")
        return [], []

x_values=[]
y_values=[]

def resolver():
    error.set("")
    x_values, y_values=resolver_ecuacion(dydx.get(),x0.get(),y0.get(),h.get(),x_final.get())
    if len(y_values)==0:
        return
    y_x_final.set(y_values[-1])

def graficar():
    error.set("")
    x_values, y_values=resolver_ecuacion(dydx.get(),x0.get(),y0.get(),h.get(),x_final.get())
    if len(y_values)==0:
        return
    ax.clear()
    set_ax()
    ax.plot(x_values,y_values,color="gold")
    canvas.draw()

# Botones
# Resolver
botonResolver=tk.Button(app, text="Resolver", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=resolver)
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.48, relheight=0.04, relwidth=0.08)

# Graficar
botonResolver=tk.Button(app, text="Graficar", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=graficar)
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.62, relheight=0.04, relwidth=0.08)

# Limpiar
botonResolver=tk.Button(app, text="Limpiar", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=limpiar)
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.8, relheight=0.04, relwidth=0.08)

app.mainloop()