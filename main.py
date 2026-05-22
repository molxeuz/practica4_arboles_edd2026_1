from estructura import arbolfarmacia

def pedir_entero(texto):
    try:
        return int(input(texto))
    except ValueError:
        print("Debe ingresar un número entero")
        return pedir_entero(texto)


def pedir_decimal(texto):
    try:
        return float(input(texto))
    except ValueError:
        print("Debe ingresar un número válido")
        return pedir_decimal(texto)


def registrar(arbol):
    id = pedir_entero("ID: ")
    nombre = input("Nombre: ")
    stock = pedir_entero("Stock: ")
    vencimiento = pedir_entero("Año de vencimiento: ")
    precio = pedir_decimal("Precio: ")

    print(arbol.insertar(id, nombre, stock, vencimiento, precio))


def vender(arbol):
    id = pedir_entero("ID del medicamento: ")
    cantidad = pedir_entero("Cantidad a vender: ")

    print(arbol.vender(id, cantidad))


def eliminar(arbol):
    id = pedir_entero("ID a eliminar: ")

    print(arbol.eliminar(id))


def limpiar(arbol):
    anio = pedir_entero("Año actual: ")

    print(arbol.limpiar_caducados(anio))


def consultar_rango(arbol):
    minimo = pedir_entero("ID inicial: ")
    maximo = pedir_entero("ID final: ")

    arbol.consultar_rango(minimo, maximo)


def fusionar(arbol):
    origen = pedir_entero("ID origen: ")
    destino = pedir_entero("ID destino: ")

    print(arbol.fusionar(origen, destino))


def menu():
    arbol = arbolfarmacia()

    while True:
        print("""
========= MENÚ INVENTARIO FARMACIA =========
1. Registrar medicamento
2. Vender medicamento
3. Eliminar por ID
4. Ejecutar limpieza por caducidad
5. Consultar estado global
6. Mostrar inventario de mayor a menor
7. Consultar rango de IDs
8. Consolidación de inventario
0. Salir
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar(arbol)
        elif opcion == "2":
            vender(arbol)
        elif opcion == "3":
            eliminar(arbol)
        elif opcion == "4":
            limpiar(arbol)
        elif opcion == "5":
            arbol.mostrar_estado()
        elif opcion == "6":
            arbol.mostrar_inverso()
        elif opcion == "7":
            consultar_rango(arbol)
        elif opcion == "8":
            fusionar(arbol)
        elif opcion == "0":
            print("Programa finalizado")
            break
        else:
            print("Opción inválida")


menu()