# Models/clases.py
# Este archivo define las clases (modelos) de datos para el sistema Global Tools.
# Incluye clases para Clientes, Administradores, Productos y Facturas, con sus atributos
# y métodos básicos de representación.

from datetime import datetime # Importamos datetime para manejar fechas en Factura

class Cliente:
    """
    Representa un cliente de Global Tools.
    
    Atributos:
        nombre (str): Nombre completo del cliente. Se guarda con formato de título.
        cedula (str): Número de cédula del cliente (identificador único).
        telefono (str): Número de teléfono del cliente.
        password_hashed (str, opcional): Contraseña del cliente hasheada para su autenticación.
                                         Puede ser None si el cliente no tiene una cuenta con login.
    """
    def __init__(self, nombre: str, cedula: str, telefono: str, password_hashed: str = None):
        """
        Inicializa una nueva instancia de Cliente.
        """
        self.nombre = nombre.strip().title() # Elimina espacios extra y capitaliza cada palabra
        self.cedula = cedula
        self.telefono = telefono
        self.password_hashed = password_hashed
        
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Cliente, ideal para impresión.
        """
        return f"|  Nombre: {self.nombre.title()}  |  Cédula: {self.cedula}  |  Telefono: {self.telefono}  |"

class Admin:
    """
    Representa un usuario administrador/trabajador del sistema Global Tools.
    
    Atributos:
        nombre (str): Nombre del administrador.
        codigo (str): Código único de trabajador del administrador.
        cedula (str): Número de cédula del administrador.
        telefono (str): Número de teléfono del administrador.
        password_hashed (str, opcional): Contraseña del administrador hasheada para su autenticación.
    """
    def __init__(self, nombre: str, codigo: str, cedula: str, telefono: str, password_hashed: str = None):
        """
        Inicializa una nueva instancia de Admin.
        """
        self.nombre = nombre
        self.codigo = codigo
        self.cedula = cedula
        self.telefono = telefono
        self.password_hashed = password_hashed
        
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Admin.
        """
        return f"|  Nombre: {self.nombre}  |  Código: {self.codigo}  |  Cédula: {self.cedula}  |  Telefono: {self.telefono}  |"

class Product:
    """
    Representa un producto en el inventario de Global Tools.
    
    Atributos:
        producto (str): Nombre del producto.
        precio (float): Precio unitario del producto.
        stock (int): Cantidad de unidades del producto en inventario.
    """
    def __init__(self, producto: str, precio: float, stock: int):     
        """
        Inicializa una nueva instancia de Product.
        """
        self.producto = producto
        self.precio = precio
        self.stock = stock
    
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Product, ideal para impresión.
        Formatea el precio a dos decimales.
        """
        return f"|  Producto: {self.producto}  |  Precio: {self.precio: .2f}  |  In Stock: {self.stock}  |"


class Factura:
    """
    Representa una factura de compra en el sistema Global Tools.

    Atributos:
        id_factura (str): Identificador único de la factura.
        cliente_cedula (str): Cédula del cliente asociado a la factura.
        fecha_emision (datetime): Fecha y hora en que se emitió la factura.
        productos_comprados (list): Lista de diccionarios, cada uno con 'producto' (nombre), 'cantidad', 'precio_unitario'.
        subtotal (float): Suma de los precios de los productos antes de recargos.
        tipo_pago (str): 'contado' o 'credito'.
        recargo_credito_porcentaje (float): Porcentaje de recargo si el pago es a crédito (ej. 0.10 para 10%).
        monto_recargo_credito (float): Monto calculado del recargo por crédito.
        total_pagar (float): Monto total a pagar, incluyendo recargos si aplica.
        dias_credito (int, opcional): Número de días de crédito otorgados (15 o 30). None si es al contado.
        fecha_vencimiento (datetime, opcional): Fecha límite para pagar el crédito. None si es al contado.
        pagado (bool): True si la factura ha sido pagada, False en caso contrario.
        monto_abonado (float): Cantidad de dinero que el cliente ha abonado a la factura.
    """
    def __init__(self, id_factura: str, cliente_cedula: str, productos_comprados: list,
                 subtotal: float, tipo_pago: str, recargo_credito_porcentaje: float,
                 monto_recargo_credito: float, total_pagar: float,
                 dias_credito: int = None, fecha_vencimiento: datetime = None):
        """
        Inicializa una nueva instancia de Factura.
        """
        self.id_factura = id_factura
        self.cliente_cedula = cliente_cedula
        self.fecha_emision = datetime.now() # La fecha de emisión se establece al momento de crear la factura
        self.productos_comprados = productos_comprados
        self.subtotal = subtotal
        self.tipo_pago = tipo_pago
        self.recargo_credito_porcentaje = recargo_credito_porcentaje
        self.monto_recargo_credito = monto_recargo_credito
        self.total_pagar = total_pagar
        self.dias_credito = dias_credito
        self.fecha_vencimiento = fecha_vencimiento
        self.pagado = False # Una factura nueva siempre empieza como no pagada
        self.monto_abonado = 0.0 # Inicialmente no se ha abonado nada

    def __str__(self):
        """
        Retorna una representación en cadena formateada de la factura.
        """
        productos_str = "\n".join([f"    - {p['producto']} (x{p['cantidad']}) @ ${p['precio_unitario']:.2f}" for p in self.productos_comprados])
        
        status_pago = "Pagada" if self.pagado else "Pendiente"
        
        credito_info = ""
        if self.tipo_pago == 'credito':
            credito_info = (f"\n  Tipo de Crédito: {self.dias_credito} días "
                            f"| Fecha Vencimiento: {self.fecha_vencimiento.strftime('%Y-%m-%d') if self.fecha_vencimiento else 'N/A'}")
            
        return (f"--- FACTURA ID: {self.id_factura} ---\n"
                f"  Cliente Cédula: {self.cliente_cedula}\n"
                f"  Fecha Emisión: {self.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  Productos:\n{productos_str}\n"
                f"  Subtotal: ${self.subtotal:.2f}\n"
                f"  Tipo de Pago: {self.tipo_pago.title()}"
                f"{credito_info}\n"
                f"  Recargo Crédito ({self.recargo_credito_porcentaje*100:.0f}%): ${self.monto_recargo_credito:.2f}\n"
                f"  Total a Pagar: ${self.total_pagar:.2f}\n"
                f"  Monto Abonado: ${self.monto_abonado:.2f}\n"
                f"  Estado: {status_pago}\n"
                f"------------------------------------")

