import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Ventas import *
import matplotlib.pyplot as plt

# Función para limpiar el contenido de las entradas
def clear_entries():
    entry_categoria.delete(0, tk.END)
    entry_producto.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

def agregar_categoria():
    name_categoria = entry_categoria.get()
    cursor.execute(f"INSERT INTO categorias (name_categoria) VALUES('{name_categoria}')")
    cnx.commit()
    messagebox.showinfo("Información", "Categoría agregada correctamente")
    clear_entries()

def agregar_producto():
    name_producto = entry_producto.get()
    cantidad_producto = entry_cantidad.get()

    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()

    categoria_id = categorias_combobox.get().split(":")[0]

    cursor.execute(f"INSERT INTO productos (name_producto, cantidad, id_categoria) VALUES('{name_producto}', '{cantidad_producto}', '{categoria_id}')")
    cnx.commit()
    messagebox.showinfo("Información", "Producto agregado correctamente")
    clear_entries()

def listar_categorias():
    cursor.execute('SELECT * FROM categorias')
    categorias = cursor.fetchall()
    categorias_list.delete(0, tk.END)
    for categoria in categorias:
        categorias_list.insert(tk.END, categoria)

def listar_productos():
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    productos_list.delete(0, tk.END)
    for producto in productos:
        productos_list.insert(tk.END, producto)

def reporte1():
    query_reporte1 = '''
        SELECT 
            c.name_categoria, 
            COALESCE(SUM(p.cantidad), 0) as total_productos
        FROM 
            categorias c
        LEFT JOIN 
            productos p ON p.id_categoria = c.id
        GROUP BY 
            c.name_categoria
    '''
    cursor.execute(query_reporte1)
    data = cursor.fetchall()

    categorias = [resultado[0] for resultado in data]
    total_productos = [resultado[1] for resultado in data]

    plt.figure(figsize=(10, 6))
    plt.bar(categorias, total_productos, color='skyblue')
    plt.xlabel('Categorías')
    plt.ylabel('Total de productos')
    plt.title('Total de productos por categoría')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def productos_por_categoria():
    query='''
        SELECT
            c.name_categoria,
            p.name_producto,
            p.cantidad
        FROM
            productos p INNER JOIN
                categorias c
            ON p.id_categoria = c.id
        ORDER BY
            c.name_categoria, p.name_producto
    '''
    cursor.execute(query)
    productos = cursor.fetchall()
    productos_list.delete(0, tk.END)
    for producto in productos:
        productos_list.insert(tk.END, producto)

def cerrar_conexion():
    cnx.close()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Ventas")

# Crear etiquetas y entradas
tk.Label(root, text="Categoría:").grid(row=0, column=0, padx=10, pady=10)
entry_categoria = tk.Entry(root)
entry_categoria.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Producto:").grid(row=1, column=0, padx=10, pady=10)
entry_producto = tk.Entry(root)
entry_producto.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Cantidad:").grid(row=2, column=0, padx=10, pady=10)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Categoría:").grid(row=3, column=0, padx=10, pady=10)
cursor.execute('SELECT * FROM categorias')
categorias = cursor.fetchall()
categorias_combobox = ttk.Combobox(root, values=[f"{categoria[0]}: {categoria[1]}" for categoria in categorias])
categorias_combobox.grid(row=3, column=1, padx=10, pady=10)

# Crear botones
tk.Button(root, text="Agregar Categoría", command=agregar_categoria).grid(row=0, column=2, padx=10, pady=10)
tk.Button(root, text="Agregar Producto", command=agregar_producto).grid(row=1, column=2, padx=10, pady=10)
tk.Button(root, text="Listar Categorías", command=listar_categorias).grid(row=2, column=2, padx=10, pady=10)
tk.Button(root, text="Listar Productos", command=listar_productos).grid(row=3, column=2, padx=10, pady=10)
tk.Button(root, text="Reporte 1", command=reporte1).grid(row=4, column=2, padx=10, pady=10)
tk.Button(root, text="Productos por Categoría", command=productos_por_categoria).grid(row=5, column=2, padx=10, pady=10)
tk.Button(root, text="Cerrar Conexión", command=cerrar_conexion).grid(row=6, column=2, padx=10, pady=10)

# Crear listas para mostrar datos
categorias_list = tk.Listbox(root, width=50, height=10)
categorias_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

productos_list = tk.Listbox(root, width=50, height=10)
productos_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
