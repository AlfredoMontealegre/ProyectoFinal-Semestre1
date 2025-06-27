class Cliente:
    def __init__(self, nombre, cedula, telefono, password_hashed=None):
        self.nombre = nombre.strip().title()
        self.cedula = cedula
        self.telefono = telefono
        self.password_hashed = password_hashed
        
    def __str__(self):
        return f"|  Nombre: {self.nombre.title()}  |  Cédula: {self.cedula}  |  Telefono: {self.telefono}  |"

class Admin:
    def __init__(self, nombre, codigo, cedula, telefono, password_hashed=None):
        self.nombre = nombre
        self.codigo = codigo
        self.cedula = cedula
        self.telefono = telefono
        self.password_hashed = password_hashed
        
    def __str__(self):
        return f"|  Nombre: {self.nombre}  |  Código: {self.codigo}  |  Cédula: {self.cedula}  |  Telefono: {self.telefono}  |"

class Product:
    def __init__(self, producto, precio, stock):    
        self.producto = producto
        self.precio = precio
        self.stock = stock
    
    def __str__(self):
        return f"|  Producto: {self.producto}  |  Precio: {self.precio: .2f}  |  In Stock: {self.stock}  |"