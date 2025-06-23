class Cliente:
    def __init__(self, nombre, cedula, telefono):
        self.nombre = nombre
        self.id = cedula
        self.telefono = telefono
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "cedula": self.id,
            "telefono": self.telefono
        }
        
    def __str__(self):
        return f"|  Nombre: {self.nombre}  |  Cédula: {self.id}  |  Telefono: {self.telefono}  |"

class Admin:
    def __init__(self, nombre, codigo, cedula, telefono):
        self.nombre = nombre
        self.codigo = codigo
        self.cedula = cedula
        self.telefono = telefono
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codigo": self.codigo,
            "cedula": self.cedula,
            "telefono": self.telefono
        }
        
        
    def __str__(self):
        return f"|  Nombre: {self.nombre}  |  Código: {self.codigo}  |  Cédula: {self.cedula}  |  Telefono: {self.telefono}  |"

class Prodcut:
    def __init__(self, producto, precio, stock):    
        self.producto = producto
        self.precio = precio
        self.stock = stock
    
    def to_dict(self):
        return {
            "Prodcuto": self.producto,
            "Precio": self.precio,
            "stock": self.stock
        }
    
    def __str__(self):
        return f"|  Producto: {self.producto}  |  Precio: {self.precio: .2f}  |  In Stock: {self.stock}  |"