import tkinter as tk
from   tkinter  import messagebox
from   perfil_I import *

def ejecutar():
    try:
        # Captura de datos
        h    = float(ent_alto.get())
        w    = float(ent_ancho.get())
        ala  = float(ent_ala.get())
        alma = float(ent_alma.get())

        if h >= 0 and w >= 0 and ala >= 0 and alma >= 0:
            objeto = perfil_I()
            objeto.config(w, h, ala, alma)

            try:
                objeto.draw()
                doc = objeto.get_doc()
                doc.saveas("test.dxf")
                messagebox.showinfo("OK", "Archivo guardado")
            except:
                messagebox.showerror("Error", "Revisar datos")
        else:
            messagebox.showerror("Error", "Un dato es nulo")
            
    except : messagebox.showerror("Error", "Ingrese números válidos")

        
# ------------------------------
# Ventana
root = tk.Tk()
root.title("Perfil I")

# Colocando titulos de pantalla
tk.Label(root,text="Perfil I").pack()

# colocando imagen
img = tk.PhotoImage(file="imagen.png")
lbl_img = tk.Label(root, image=img)
lbl_img.pack(pady=10)

# Inputs y Etiquetas
tk.Label(root, text="Alto:").pack()
ent_alto = tk.Entry(root)
ent_alto.pack()

tk.Label(root, text="Ancho:").pack()
ent_ancho = tk.Entry(root)
ent_ancho.pack()

tk.Label(root, text="Ala:").pack()
ent_ala = tk.Entry(root)
ent_ala.pack()

tk.Label(root, text="Alma:").pack()
ent_alma = tk.Entry(root)
ent_alma.pack()

# Botón
tk.Button(root, text="GRAFICAR", command=ejecutar).pack(pady=10)

root.mainloop()
