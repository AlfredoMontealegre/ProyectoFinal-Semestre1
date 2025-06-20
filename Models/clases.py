class Cliente:
    def __init__(self, nombre, cedula, telefono):
        self.nombre = nombre
        self.id = cedula
        self.telefono = telefono
        
    def __str__(self):
        return f"Cliente: {self.nombre}, Cédula: {self.id}, Telefono: {self.telefono}"

class Admin:
    def __init__(self, nombre, codigo, cedula, telefono):
        self.nombre = nombre
        self.codigo = codigo
        self.cedula = cedula
        self.telefono = telefono
        
    def __str__(self):
        return f"User: {self.user}, Cédula: {self.cedula}, Código De trabajador: {self.codigo}, Telefono: {self.telefono}"

class Prodcut:
    def __init__(self, producto, precio, stock):    
        self.producto = producto
        self.precio = precio
        self.stock = stock
    
    def __str__(self):
        return f"Producto: {self.producto}, Precio: {self.precio: .2f}, In Stock: {self.stock}"