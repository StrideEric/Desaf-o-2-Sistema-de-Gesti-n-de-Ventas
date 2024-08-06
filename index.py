"""
Desafío 2: Sistema de Gestión de Ventas
Objetivo: Desarrollar un sistema para registrar y gestionar ventas de productos.

Requisitos:

Crear una clase base Venta con atributos como fecha, cliente, productos vendidos, etc.
Definir al menos 2 clases derivadas para diferentes tipos de ventas (por ejemplo, VentaOnline, VentaLocal) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar las ventas.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.
"""
import json
from datetime import datetime

class Venta:
    def __init__(self, fecha, cliente, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos

    def to_dict(self):
        return {
            'fecha': self.fecha,
            'cliente': self.cliente,
            'productos': self.productos
        }

    def __str__(self):
        return f"Fecha: {self.fecha}, Cliente: {self.cliente}, Productos: {', '.join(self.productos)}"

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, direccion_envio):
        super().__init__(fecha, cliente, productos)
        self.direccion_envio = direccion_envio

    def to_dict(self):
        data = super().to_dict()
        data['direccion_envio'] = self.direccion_envio
        return data

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Dirección de envío: {self.direccion_envio}"

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, tienda):
        super().__init__(fecha, cliente, productos)
        self.tienda = tienda

    def to_dict(self):
        data = super().to_dict()
        data['tienda'] = self.tienda
        return data

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Tienda: {self.tienda}"

class SistemaGestionVentas:
    def __init__(self, archivo='ventas.json'):
        self.archivo = archivo
        self.ventas = self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def guardar_datos(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.ventas, f, indent=4)

    def crear_venta(self, venta):
        self.ventas.append(venta.to_dict())
        self.guardar_datos()

    def leer_ventas(self):
        return self.ventas

    def actualizar_venta(self, indice, nueva_venta):
        try:
            self.ventas[indice] = nueva_venta.to_dict()
            self.guardar_datos()
        except IndexError:
            print("Error: Índice fuera de rango")

    def eliminar_venta(self, indice):
        try:
            del self.ventas[indice]
            self.guardar_datos()
        except IndexError:
            print("Error: Índice fuera de rango")

    def imprimir_ventas(self):
        for indice, venta in enumerate(self.ventas):
            if 'direccion_envio' in venta:
                venta_obj = VentaOnline(venta['fecha'], venta['cliente'], venta['productos'], venta['direccion_envio'])
            else:
                venta_obj = VentaLocal(venta['fecha'], venta['cliente'], venta['productos'], venta['tienda'])
            print(f"Venta {indice + 1}:\n{venta_obj}\n")

def cargar_venta(sistema):
    tipo_venta = int(input("¿Qué tipo de venta es? \n1. Online \n2. Local \n"))
    cliente = input("Ingrese el nombre del cliente: \n")
    productos = input("Ingrese los productos separados por una coma (ejemplo: canasto, sandalias, escoba): \n").split(', ')
    if tipo_venta == 1:
        direccion_envio = input("Ingrese la dirección de envío: \n")
        venta_online = VentaOnline(fecha=str(datetime.now()), cliente=cliente, productos=productos, direccion_envio=direccion_envio)
        sistema.crear_venta(venta_online)
    elif tipo_venta == 2:
        venta_local = VentaLocal(fecha=str(datetime.now()), cliente=cliente, productos=productos, tienda="Tienda Central")
        sistema.crear_venta(venta_local)

def modificar_venta(sistema):
    print("Para modificar una venta seleccione el tipo de venta y la posición de la venta a modificar.")
    tipo_venta = int(input("¿Qué tipo de venta es? \n1. Online \n2. Local \n"))
    posicion = int(input("Posición de la venta: "))
    cliente = input("Ingrese el nombre del cliente: \n")
    productos = input("Ingrese los productos separados por una coma (ejemplo: canasto, sandalias, escoba): \n").split(', ')
    if tipo_venta == 1:
        direccion_envio = input("Ingrese la dirección de envío: \n")
        nueva_venta_online = VentaOnline(fecha=str(datetime.now()), cliente=cliente, productos=productos, direccion_envio=direccion_envio)
        sistema.actualizar_venta(posicion, nueva_venta_online)
    elif tipo_venta == 2:
        nueva_venta_local = VentaLocal(fecha=str(datetime.now()), cliente=cliente, productos=productos, tienda="Tienda Central")
        sistema.actualizar_venta(posicion, nueva_venta_local)

def eliminar_venta(sistema):
    print("Selecciona la posición de la venta a eliminar")
    posicion = int(input("Posición: "))
    sistema.eliminar_venta(posicion)

def ver_ventas(sistema):
    print("Ventas realizadas: \n")
    sistema.imprimir_ventas()
    
def main():
    sistema = SistemaGestionVentas()

    operaciones = {
        1: cargar_venta,
        2: modificar_venta,
        3: eliminar_venta,
        4: ver_ventas
    }

    seleccion = int(input("¿Qué desea hacer? \n1. Cargar una venta \n2. Modificar una venta \n3. Eliminar una venta. \n4. Ver ventas realizadas. \n"))
    operacion = operaciones.get(seleccion, lambda x: print("Operación no válida"))
    operacion(sistema)


if __name__ == '__main__':
    main()
