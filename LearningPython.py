#carrito = ["Manzana", "Leche", "Pan"]
#producto = {"Leche": 2.5}

def exe_producto_y_carrito(self):
    class Carrito:
        def __init__(self):
            self.lista_productos = {}
        def add_producto(self, nombre, precio):
            self.lista_productos[nombre] = precio
        def calcular_precio(self):
            total = 0
            for precio in self.lista_productos.values():
                total += precio
            return total

    carrito = Carrito()
    carrito.add_producto("Manzana", 1.50)
    carrito.add_producto("Pera", 2.50)
    carrito.add_producto("Mandarina", 2.00)
    carrito.add_producto("Platano", 3.50)
    print(pagar = carrito.calcular_precio())

## ------------ uso de comprension de lista  ##
#precios = [20.0, 13.00, 10.30, 20.10, 8.5]
#precios_con_iva = [precio * 1.16 for precio in precios]
def exe_producto_y_ropa(self):
    class Producto:
        def __init__(self, nombre, precio):
            self.nombre = nombre
            self.precio = precio
    class Ropa(Producto):
        def __init__(self, nombre, precio, talla):
            super().__init__(nombre, precio)
            self.talla = talla
    mi_camisa = Ropa("Camisa de algodón", 25.00, "M")
    print(f"{mi_camisa.nombre} talla {mi_camisa.talla} cuesta ${mi_camisa.precio}")


if __name__ == "__main__":
    exe_producto_y_ropa()