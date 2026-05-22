TOTAL_OPERACIONES_FUSION = 0

class medicamento:
    def _init_(self, id, nombre, stock, vencimiento, precio):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.vencimiento = vencimiento
        self.precio = precio
        self.izquierda = None
        self.derecha = None

    def mostrar(self):
        print("ID:", self.id, "| Nombre:", self.nombre, "| Stock:", self.stock, "| Vence:", self.vencimiento, "| Precio:", round(self.precio, 2))


class arbolfarmacia:
    def _init_(self):
        self.raiz = None
        self.alertas_stock = 0
        self.valor_total = 0
        self._encontro_rango = False

    def insertar(self, id, nombre, stock, vencimiento, precio):
        if id % 2 == 0:
            precio = precio * 0.90

        nuevo = medicamento(id, nombre, stock, vencimiento, precio)

        if self.raiz is None:
            self.raiz = nuevo
            self._sumar_estado(nuevo)
            return "Medicamento registrado correctamente"

        return self._insertar_recursivo(self.raiz, nuevo)

    def _insertar_recursivo(self, actual, nuevo):
        if nuevo.id == actual.id:
            return "No se puede registrar: ya existe un medicamento con ese ID"

        if nuevo.id < actual.id:
            if actual.izquierda is None:
                actual.izquierda = nuevo
                self._sumar_estado(nuevo)
                return "Medicamento registrado correctamente"
            return self._insertar_recursivo(actual.izquierda, nuevo)

        if actual.derecha is None:
            actual.derecha = nuevo
            self._sumar_estado(nuevo)
            return "Medicamento registrado correctamente"

        return self._insertar_recursivo(actual.derecha, nuevo)

    def _sumar_estado(self, nodo):
        if nodo.stock < 5:
            self.alertas_stock += 1

        self.valor_total += nodo.precio * nodo.stock

    def _restar_estado(self, nodo):
        if nodo.stock < 5:
            self.alertas_stock -= 1

        self.valor_total -= nodo.precio * nodo.stock

    def buscar(self, id):
        actual = self.raiz

        while actual is not None:
            if id == actual.id:
                return actual

            if id < actual.id:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None

    def vender(self, id, cantidad):
        if cantidad <= 0:
            return "La cantidad debe ser mayor que cero"

        nodo = self.buscar(id)

        if nodo is None:
            return "No existe un medicamento con ese ID"

        if nodo.stock == 0:
            return "El medicamento existe, pero tiene stock en cero\n" + self.sugerir_sustituto(id)

        if cantidad > nodo.stock:
            return "No hay stock suficiente. Stock actual: " + str(nodo.stock)

        stock_anterior = nodo.stock
        nodo.stock -= cantidad
        self.valor_total -= nodo.precio * cantidad

        if stock_anterior >= 5 and nodo.stock < 5:
            self.alertas_stock += 1

        if nodo.stock == 0:
            return "Venta realizada. El medicamento quedó con stock en cero\n" + self.sugerir_sustituto(id)

        return "Venta realizada correctamente. Stock actual: " + str(nodo.stock)

    def eliminar(self, id):
        self._eliminado = False
        self.raiz = self._eliminar_recursivo(self.raiz, id, True)

        if self._eliminado:
            return "Medicamento eliminado correctamente"

        return "No existe un medicamento con ese ID"

    def _eliminar_recursivo(self, actual, id, actualizar_estado):
        if actual is None:
            return None

        if id < actual.id:
            actual.izquierda = self._eliminar_recursivo(actual.izquierda, id, actualizar_estado)
            return actual

        if id > actual.id:
            actual.derecha = self._eliminar_recursivo(actual.derecha, id, actualizar_estado)
            return actual

        self._eliminado = True

        if actualizar_estado:
            self._restar_estado(actual)

        if actual.izquierda is None:
            return actual.derecha

        if actual.derecha is None:
            return actual.izquierda

        sucesor = self._minimo(actual.derecha)
        actual.id = sucesor.id
        actual.nombre = sucesor.nombre
        actual.stock = sucesor.stock
        actual.vencimiento = sucesor.vencimiento
        actual.precio = sucesor.precio
        actual.derecha = self._eliminar_recursivo(actual.derecha, sucesor.id, False)

        return actual

    def _minimo(self, actual):
        while actual.izquierda is not None:
            actual = actual.izquierda

        return actual

    def _maximo(self, actual):
        while actual.derecha is not None:
            actual = actual.derecha

        return actual

    def limpiar_caducados(self, anio_actual):
        cantidad = 0

        while True:
            id_vencido = self._buscar_vencido(self.raiz, anio_actual)

            if id_vencido is None:
                break

            self.eliminar(id_vencido)
            cantidad += 1

        return "Limpieza terminada. Medicamentos eliminados: " + str(cantidad)

    def _buscar_vencido(self, actual, anio_actual):
        if actual is None:
            return None

        if actual.vencimiento <= anio_actual:
            return actual.id

        encontrado = self._buscar_vencido(actual.izquierda, anio_actual)

        if encontrado is not None:
            return encontrado

        return self._buscar_vencido(actual.derecha, anio_actual)

    def mostrar_inverso(self):
        if self.raiz is None:
            print("El inventario está vacío")
            return

        self._mostrar_inverso_recursivo(self.raiz)

    def _mostrar_inverso_recursivo(self, actual):
        if actual is None:
            return

        self._mostrar_inverso_recursivo(actual.derecha)
        actual.mostrar()
        self._mostrar_inverso_recursivo(actual.izquierda)

    def consultar_rango(self, minimo, maximo):
        if minimo > maximo:
            temporal = minimo
            minimo = maximo
            maximo = temporal

        self._encontro_rango = False
        self._consultar_rango_recursivo(self.raiz, minimo, maximo)

        if not self._encontro_rango:
            print("No hay medicamentos en ese rango")

    def _consultar_rango_recursivo(self, actual, minimo, maximo):
        if actual is None:
            return

        if actual.id > minimo:
            self._consultar_rango_recursivo(actual.izquierda, minimo, maximo)

        if minimo <= actual.id and actual.id <= maximo:
            actual.mostrar()
            self._encontro_rango = True

        if actual.id < maximo:
            self._consultar_rango_recursivo(actual.derecha, minimo, maximo)

    def sugerir_sustituto(self, id):
        sucesor = self._sucesor(id)

        if sucesor is not None:
            return "Sustituto sugerido por sucesor In-order: ID " + str(sucesor.id) + " - " + sucesor.nombre

        predecesor = self._predecesor(id)

        if predecesor is not None:
            return "Sustituto sugerido por predecesor In-order: ID " + str(predecesor.id) + " - " + predecesor.nombre

        return "No hay sustituto disponible"

    def _sucesor(self, id):
        nodo = self.buscar(id)

        if nodo is None:
            return None

        if nodo.derecha is not None:
            return self._minimo(nodo.derecha)

        actual = self.raiz
        sucesor = None

        while actual is not None:
            if id < actual.id:
                sucesor = actual
                actual = actual.izquierda
            elif id > actual.id:
                actual = actual.derecha
            else:
                break

        return sucesor

    def _predecesor(self, id):
        nodo = self.buscar(id)

        if nodo is None:
            return None

        if nodo.izquierda is not None:
            return self._maximo(nodo.izquierda)

        actual = self.raiz
        predecesor = None

        while actual is not None:
            if id > actual.id:
                predecesor = actual
                actual = actual.derecha
            elif id < actual.id:
                actual = actual.izquierda
            else:
                break

        return predecesor

    def fusionar(self, id_origen, id_destino):
        global TOTAL_OPERACIONES_FUSION

        if id_origen == id_destino:
            return "El ID de origen y el ID de destino no pueden ser iguales"

        origen = self.buscar(id_origen)
        destino = self.buscar(id_destino)

        if origen is None:
            return "No existe el medicamento de origen"

        if destino is None:
            return "No existe el medicamento de destino"

        stock_anterior_destino = destino.stock
        destino.stock += origen.stock
        self.valor_total += destino.precio * origen.stock

        if stock_anterior_destino < 5 and destino.stock >= 5:
            self.alertas_stock -= 1

        self.eliminar(id_origen)
        TOTAL_OPERACIONES_FUSION += 1

        return "Fusión realizada correctamente. Stock destino actual: " + str(destino.stock)

    def mostrar_estado(self):
        print("Alertas de stock:", self.alertas_stock)
        print("Valor total del inventario:", round(self.valor_total, 2))
        print("Total de operaciones de fusión:", self.operaciones_fusion())

    def operaciones_fusion(self):
        global TOTAL_OPERACIONES_FUSION
        return TOTAL_OPERACIONES_FUSION