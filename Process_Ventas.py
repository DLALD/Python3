from Ventas import *
import matplotlib.pyplot as pt
import os

os.system('cls')

global menu_status
menu_status = True

def crud_db(op):
    if op == 1:
        #Insercion de datos 
        name_categoria = input("Ingrese el nombre de categoria: ")
        cursor.execute(f"INSERT INTO categorias (name_categoria) VALUES('{name_categoria}')")
        cnx.commit() # permite que los datos se guarden en la base de datos
        os.system('pause')
        main_menu()
    elif op == 2:
        name_producto = input("Ingrese el nombre del producto: ")
        cantidad_producto = input("Ingrese la cantidad del producto: ")
        
        print("Listado de categorias")
        #leer datos 
        cursor.execute('SELECT * FROM categorias')
        print(cursor.fetchall())
        categoria_id = input("Ingrese el numero de la categoria: ")
        
        
        cursor.execute(f"INSERT INTO productos (name_producto, cantidad,id_categoria) VALUES('{name_producto}','{cantidad_producto}','{categoria_id}')")
        cnx.commit() # permite que los datos se guarden en la base de datos
        os.system('pause')
        main_menu()
    elif op == 3:
        # Listar categorías
        cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        for categoria in categorias:
            print(categoria)
        os.system('pause')
        main_menu()
    elif op == 4:
        # Listar productos
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        for producto in productos:
            print(producto)
        os.system('pause')
        main_menu()
    elif op == 5:
        sub_menu()
    elif op == 6:
        global menu_status
        menu_status = False
        print("See you")
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        main_menu()

def reporte1():
    query_reporte1='''
        SELECT 
            c.name_categoria, 
            SUM(p.cantidad) as total_productos
        FROM 
            productos p INNER JOIN 
                categorias c
            ON p.id_categoria = c.id
        GROUP BY 
            c.name_categoria 
    '''
    cursor.execute(query_reporte1)
    data=cursor.fetchall()
    # Preparar los datos para la gráfica
    categorias = [resultado[0] for resultado in data]
    total_productos = [resultado[1] for resultado in data]


    # Crear la gráfica
    pt.figure(figsize=(10, 6))
    pt.bar(categorias, total_productos, color='skyblue')
    pt.xlabel('Categorías')
    pt.ylabel('Total de productos')
    pt.title('Total de productos por categoría')
    pt.xticks(rotation=45)
    pt.tight_layout()
    pt.show()

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
    for producto in productos:
        print(producto)
    os.system('pause')
    sub_menu()

def sub_menu():
    os.system('cls')
    print("::: SUB MENU :::")
    print("[1]. Productos disponibles")
    print("[2]. Productos disponibles por categorias")
    print("[3]. Salir")
    print("Press any option: ")
    opt = int(input())
    if opt == 1:
        reporte1()
    elif opt == 2:
        productos_por_categoria()
    elif opt == 3:
        main_menu()
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        sub_menu()

#Main
def main_menu():
    os.system('cls')
    while menu_status:
        print("::: MAIN MENU :::")
        print("[1]. Crear categoria")
        print("[2]. Crear productos")
        print("[3]. Listar categorias")
        print("[4]. Listar productos")
        print("[5]. Reportes")
        print("[6]. Salir")

        print("Press any option: ")
        opt = int(input())
        crud_db(opt)

main_menu()
#Cerrar la conexión 
cnx.close()
