import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols,sympify,lambdify
import math
from matplotlib.figure import Figure
from decimal import getcontext
from Euler_Method import euler_method
from Cubic_Splines import cubic_splines
getcontext().prec=100

# Interfaz Base
app=tk.Tk()
app.geometry("800x600")
app.configure(background="#f1ede3")
graph_frame = tk.Frame(app, width=1000, height=1000, bg="lightgrey")
graph_frame.place(relx=0.43, rely=0.13)
fig = Figure(figsize=(6, 4), dpi=140)
ax = fig.add_subplot(111) 
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
toolbar = NavigationToolbar2Tk(canvas, graph_frame, pack_toolbar=False)
toolbar.pack()
toolbar.update()
tk.Wm.wm_title(app, "Solucionador de Ecuaciones Diferenciales Ordinarias.")

def set_ax():
    ax.set_title("Método de Euler.")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.grid()

set_ax()

dydx=tk.StringVar(app)
x0=tk.StringVar(app)
y0=tk.StringVar(app)
h=tk.StringVar(app)
x_final=tk.StringVar(app)
y_x_final=tk.StringVar(app)
error=tk.StringVar(app)

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
i7=tk.Entry(app, font=(TipoFuente, SizeFuente, 'bold'), bg=ColorE, fg="red", justify="center", textvariable=error, state="readonly")
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

def resolver_ecuacion(_input, _x0, _y0, _h, _x_final):
    try:
        x, y, e = symbols('x y e', real = True)
        input = _input
        expr = sympify(input)
        f = lambdify((x,y,e), expr)
        e_m = euler_method(_x0,_y0,_h,_x_final,f)
        if e_m[2]:
            return e_m[0], e_m[1]
        error.set("!!Error: An unexpected error occurred. Please check your input and try again.")
        return [], []
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

def graficar(flag):
    error.set("")
    x_values, y_values=resolver_ecuacion(dydx.get(),x0.get(),y0.get(),h.get(),x_final.get())
    if len(y_values)==0:
        return
    if flag:
        X_splines, Y_splines, band=cubic_splines(x_values, y_values)
        if not band:
            error.set("!!Error: An unexpected error occurred. Please check your input and try again.")
            return
        ax.clear()
        set_ax()
        ax.plot(X_splines,Y_splines,color="gold")
        ax.scatter(x_values,y_values,color="black")
    else:
        ax.clear()
        set_ax()
        ax.plot(x_values,y_values,color="gold")
    # Generar campo de isoclinas
    try:
        x, y, e = symbols('x y e', real=True)
        input_expr = dydx.get()
        expr = sympify(input_expr)
        f = lambdify((x, y, e), expr)
        x_min, x_max = float(x0.get()), float(x_final.get())
        y_min = min(y_values) - 1
        y_max = max(y_values) + 1
        x_vals = np.linspace(x_min, x_max, 20)
        y_vals = np.linspace(y_min, y_max, 20)
        X, Y = np.meshgrid(x_vals, y_vals)
        U = 1 
        V = f(X, Y, math.e)
        N = np.sqrt(U**2 + V**2)
        U /= N
        V /= N
        ax.quiver(X, Y, U, V, color="lightgrey", alpha=0.7, pivot="middle", scale=20, label="Campo de Isoclinas.")
        ax.legend()
        canvas.draw()
    except:
        error.set("!!Error: An unexpected error occurred. Please check your input and try again.")

# Botones
# Resolver
botonResolver=tk.Button(app, text="Resolver", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=resolver)
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.48, relheight=0.04, relwidth=0.08)

# Graficar
botonResolver=tk.Button(app, text="Graficar", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=lambda: graficar(False))
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.62, relheight=0.04, relwidth=0.08)

# Interpolar
botonResolver=tk.Button(app, text="Interpolar", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=lambda: graficar(True))
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.71, relheight=0.04, relwidth=0.08)

# Limpiar
botonResolver=tk.Button(app, text="Limpiar", font=(TipoFuente,SizeFuente), bg="#9d8f6d", fg="black", command=limpiar)
botonResolver.pack
botonResolver.place(relx=0.165, rely=0.8, relheight=0.04, relwidth=0.08)

app.mainloop()