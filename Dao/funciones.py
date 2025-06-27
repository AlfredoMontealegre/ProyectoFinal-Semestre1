# Dao/funciones.py
# Este archivo contiene las funciones y clases de Acceso a Datos (DAO - Data Access Object)
# para la persistencia de la información del sistema Global Tools.
# Utiliza el módulo 'pickle' para serializar y deserializar objetos Python a archivos binarios.

import os
import pickle
import Models.clases as models # Importa las clases de modelos (Cliente, Admin, Product, Factura)

# Configuración de las rutas de los archivos de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Directorio base del script DAO

# Archivo para guardar datos de trabajadores/administradores del sistema
ADMIN_FILENAME = 'user_admin.bin'
ADMIN_FILE_PATH = os.path.join(BASE_DIR, ADMIN_FILENAME)

# Archivo para guardar datos de clientes
USER_FILENAME = 'usuarios_clientes.bin' # Nombre de archivo específico para clientes para evitar colisiones
USER_FILE_PATH = os.path.join(BASE_DIR, USER_FILENAME)

# Archivo para guardar datos de productos
PRODUCT_FILE_NAME = 'productos.bin'
PRODUCT_FILE_PATH = os.path.join(BASE_DIR, PRODUCT_FILE_NAME)

# Archivo para guardar datos de facturas
INVOICE_FILE_NAME = 'facturas.bin' # Nuevo archivo para facturas
INVOICE_FILE_PATH = os.path.join(BASE_DIR, INVOICE_FILE_NAME)

# --- Funciones de persistencia genéricas para listas de objetos ---

def _save_data(filepath: str, data: list):
    """
    Función genérica y privada para guardar una lista de objetos en un archivo binario.
    Crea el directorio si no existe.
    
    Args:
        filepath (str): Ruta completa del archivo donde se guardarán los datos.
        data (list): Lista de objetos Python a serializar.
    """
    try:
        # Asegura que el directorio para el archivo exista
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as file: # Abre el archivo en modo escritura binaria ('wb')
            pickle.dump(data, file) # Serializa la lista de datos en el archivo
    except Exception as error:
        print(f"❌ ERROR al guardar datos en '{os.path.basename(filepath)}': {error}")

def _load_data(filepath: str) -> list:
    """
    Función genérica y privada para cargar una lista de objetos desde un archivo binario.
    Maneja casos de archivo no encontrado, vacío o corrupto.
    
    Args:
        filepath (str): Ruta completa del archivo desde donde se cargarán los datos.
        
    Returns:
        list: Lista de objetos deserializados. Retorna una lista vacía si hay errores
              o el archivo no existe/está vacío.
    """
    data = []
    try:
        # Verifica si el archivo existe y tiene contenido
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            return [] # Archivo no existe o está vacío, retorna lista vacía
        
        with open(filepath, 'rb') as file: # Abre el archivo en modo lectura binaria ('rb')
            data = pickle.load(file) # Deserializa los datos del archivo
        
        # Valida que los datos cargados sean una lista
        if not isinstance(data, list):
            print(f"Advertencia: El archivo '{os.path.basename(filepath)}' no contiene una lista. Reestableciendo.")
            # Si el contenido no es una lista, se considera corrupto y se reestablece
            _save_data(filepath, []) 
            return []
        return data
    except (FileNotFoundError, EOFError):
        # FileNotFoundError: El archivo no existe (ya cubierto por os.path.exists pero bueno tenerlo).
        # EOFError: El archivo existe pero está vacío o truncado.
        return []
    except pickle.UnpicklingError as e:
        # Error específico de pickle si el archivo binario está mal formado o es incompatible.
        print(f"❌ ERROR al cargar '{os.path.basename(filepath)}' (error de formato pickle): {e}. Se reestablecerá el archivo.")
        _save_data(filepath, []) # Reestablece el archivo corrupto a una lista vacía
        return []
    except Exception as error:
        # Cualquier otro error inesperado durante la carga.
        print(f"❌ ERROR inesperado al cargar '{os.path.basename(filepath)}': {error}")
        return []

# --- Funciones DAO específicas usando las genéricas para cada modelo ---

def guardar_admin_users(admin_users: list[models.Admin]):
    """
    Guarda la lista completa de objetos Admin en el archivo de administradores.
    
    Args:
        admin_users (list[models.Admin]): Lista de objetos Admin a guardar.
    """
    _save_data(ADMIN_FILE_PATH, admin_users)

def cargar_admin_users() -> list[models.Admin]:
    """
    Carga la lista completa de objetos Admin desde el archivo de administradores.
    
    Returns:
        list[models.Admin]: Lista de objetos Admin cargados.
    """
    return _load_data(ADMIN_FILE_PATH)

def guardar_clientes_data(clientes: list[models.Cliente]):
    """
    Guarda la lista completa de objetos Cliente en el archivo de clientes.
    
    Args:
        clientes (list[models.Cliente]): Lista de objetos Cliente a guardar.
    """
    _save_data(USER_FILE_PATH, clientes)

def cargar_clientes_data() -> list[models.Cliente]:
    """
    Carga la lista completa de objetos Cliente desde el archivo de clientes.
    
    Returns:
        list[models.Cliente]: Lista de objetos Cliente cargados.
    """
    return _load_data(USER_FILE_PATH)

def guardar_productos_data(products: list[models.Product]):
    """
    Guarda la lista completa de objetos Product en el archivo de productos.
    
    Args:
        products (list[models.Product]): Lista de objetos Product a guardar.
    """
    _save_data(PRODUCT_FILE_PATH, products)

def cargar_productos_data() -> list[models.Product]:
    """
    Carga la lista completa de objetos Product desde el archivo de productos.
    
    Returns:
        list[models.Product]: Lista de objetos Product cargados.
    """
    return _load_data(PRODUCT_FILE_PATH)

def guardar_facturas_data(facturas: list[models.Factura]):
    """
    Guarda la lista completa de objetos Factura en el archivo de facturas.
    
    Args:
        facturas (list[models.Factura]): Lista de objetos Factura a guardar.
    """
    _save_data(INVOICE_FILE_PATH, facturas)

def cargar_facturas_data() -> list[models.Factura]:
    """
    Carga la lista completa de objetos Factura desde el archivo de facturas.
    
    Returns:
        list[models.Factura]: Lista de objetos Factura cargados.
    """
    return _load_data(INVOICE_FILE_PATH)


# --- Clases DAO (Data Access Object) para cada modelo ---

class ClienteDao:
    """
    Clase DAO para gestionar las operaciones de persistencia de objetos Cliente.
    """
    def __init__(self):
        """
        Inicializa ClienteDao cargando todos los clientes existentes.
        """
        self.clientes = cargar_clientes_data() # Carga la lista inicial de clientes al instanciar

    def add(self, cliente: models.Cliente):
        """
        Agrega un nuevo objeto Cliente a la lista en memoria y lo persiste en el archivo.
        
        Args:
            cliente (models.Cliente): El objeto Cliente a añadir.
        """
        self.clientes.append(cliente)
        guardar_clientes_data(self.clientes) # Guarda la lista completa actualizada

    def get_all_clientes(self) -> list[models.Cliente]:
        """
        Retorna la lista completa de todos los objetos Cliente en memoria.
        
        Returns:
            list[models.Cliente]: Lista de todos los clientes.
        """
        return self.clientes
    
    def update_clientes_list(self):
        """
        Persiste el estado actual de la lista de clientes en memoria al archivo.
        Útil después de modificar un cliente existente.
        """
        guardar_clientes_data(self.clientes)
    
    def delete_cliente(self, cedula_cliente: str) -> bool:
        """
        Elimina un cliente de la lista en memoria por su número de cédula y lo persiste.
        
        Args:
            cedula_cliente (str): La cédula del cliente a eliminar.
            
        Returns:
            bool: True si el cliente fue eliminado, False si no se encontró.
        """
        len_inicial = len(self.clientes)
        # Crea una nueva lista excluyendo el cliente con la cédula especificada
        self.clientes = [c for c in self.clientes if c.cedula != cedula_cliente]
        if len(self.clientes) < len_inicial: # Si la longitud cambió, significa que se eliminó
            guardar_clientes_data(self.clientes) # Guarda la lista modificada
            return True
        return False
    
    def find_cliente(self, query: str) -> list[models.Cliente]:
        """
        Busca clientes por su número de cédula o por coincidencia parcial en el nombre.
        La búsqueda por nombre es insensible a mayúsculas/minúsculas.
        
        Args:
            query (str): La cédula completa o una parte del nombre a buscar.
            
        Returns:
            list[models.Cliente]: Lista de clientes que coinciden con la consulta.
        """
        found_clientes = []
        for c in self.clientes:
            # Compara por cédula exacta o por nombre parcial (insensible a mayúsculas/minúsculas)
            if c.cedula == query or query.lower() in c.nombre.lower():
                found_clientes.append(c)
        return found_clientes
    
    def show(self):
        """
        Muestra todos los clientes registrados en un formato de tabla legible.
        """
        all_clientes = self.get_all_clientes()
        if not all_clientes:
            print("[INFO] No hay clientes registrados.")
        else:
            print("\n--- LISTA DE CLIENTES ---")
            # Encabezado de la tabla
            print(f"{'Cédula':<15} {'Nombre':<25} {'Teléfono':<15}")
            print("-" * 55)
            # Imprime cada cliente
            for cliente in all_clientes:
                print(f"{cliente.cedula:<15} {cliente.nombre:<25} {cliente.telefono:<15}")
            print("-" * 55)


class AdminDao:
    """
    Clase DAO para gestionar las operaciones de persistencia de objetos Admin (administradores).
    """
    def __init__(self):
        """
        Inicializa AdminDao cargando todos los usuarios administradores existentes.
        """
        self.users = cargar_admin_users() # Carga la lista inicial de administradores
    
    def add(self, user: models.Admin) -> bool:
        """
        Agrega un nuevo objeto Admin a la lista en memoria y lo persiste en el archivo.
        Realiza validaciones para evitar códigos o cédulas duplicadas.
        
        Args:
            user (models.Admin): El objeto Admin a añadir.
            
        Returns:
            bool: True si el administrador fue agregado exitosamente, False si ya existe un duplicado.
        """
        # Verificar si el código o cédula ya existen antes de agregar
        if any(u.codigo == user.codigo for u in self.users):
            print(f"[ADVERTENCIA] Ya existe un administrador con el código: {user.codigo}.")
            return False
        if any(u.cedula == user.cedula for u in self.users):
            print(f"[ADVERTENCIA] Ya existe un administrador con la cédula: {user.cedula}.")
            return False

        self.users.append(user)
        guardar_admin_users(self.users) # Guarda la lista completa actualizada
        print("[EXITO] Administrador guardado correctamente.")
        return True
    
    def get_all_admin_users(self) -> list[models.Admin]:
        """
        Retorna la lista completa de todos los objetos Admin en memoria.
        
        Returns:
            list[models.Admin]: Lista de todos los administradores.
        """
        return self.users
    
    def find_admin_by_username(self, username: str) -> models.Admin | None:
        """
        Busca un administrador por su nombre de usuario (sensible a mayúsculas/minúsculas).
        
        Args:
            username (str): El nombre de usuario (campo 'nombre' del Admin) a buscar.
            
        Returns:
            models.Admin | None: El objeto Admin si se encuentra, de lo contrario None.
        """
        for user in self.users:
            if user.nombre == username: # La comparación es sensible a mayúsculas/minúsculas aquí
                return user
        return None

class ProductDao:
    """
    Clase DAO para gestionar las operaciones de persistencia de objetos Product.
    """
    def __init__(self):
        """
        Inicializa ProductDao cargando todos los productos existentes.
        """
        self.products = cargar_productos_data() # Carga la lista inicial de productos
    
    def add(self, product: models.Product) -> bool:
        """
        Agrega un nuevo objeto Product a la lista en memoria y lo persiste en el archivo.
        Realiza validación para evitar nombres de producto duplicados (insensible a mayúsculas/minúsculas).
        
        Args:
            product (models.Product): El objeto Product a añadir.
            
        Returns:
            bool: True si el producto fue agregado exitosamente, False si ya existe un duplicado.
        """
        # Verificar si ya existe un producto con el mismo nombre (insensible a mayúsculas/minúsculas)
        if any(p.producto.lower() == product.producto.lower() for p in self.products):
            print(f"[ADVERTENCIA] Ya existe un producto con el nombre: {product.producto}.")
            return False
        self.products.append(product)
        guardar_productos_data(self.products) # Guarda la lista completa actualizada
        print("[EXITO] Producto guardado correctamente.")
        return True
    
    def get_all_products(self) -> list[models.Product]:
        """
        Retorna la lista completa de todos los objetos Product en memoria.
        
        Returns:
            list[models.Product]: Lista de todos los productos.
        """
        return self.products
    
    def update_products_list(self):
        """
        Persiste el estado actual de la lista de productos en memoria al archivo.
        Útil después de modificar un producto existente.
        """
        guardar_productos_data(self.products)
    
    def delete_product(self, product_name: str) -> bool:
        """
        Elimina un producto de la lista en memoria por su nombre (insensible a mayúsculas/minúsculas)
        y lo persiste.
        
        Args:
            product_name (str): El nombre del producto a eliminar.
            
        Returns:
            bool: True si el producto fue eliminado, False si no se encontró.
        """
        len_inicial = len(self.products)
        # Filtra la lista excluyendo el producto con el nombre especificado
        self.products = [p for p in self.products if p.producto.lower() != product_name.lower()]
        if len(self.products) < len_inicial: # Si la longitud cambió, significa que se eliminó
            guardar_productos_data(self.products) # Guarda la lista modificada
            return True
        return False
    
    def find_product(self, query: str) -> list[models.Product]:
        """
        Busca productos por coincidencia parcial en el nombre (insensible a mayúsculas/minúsculas).
        
        Args:
            query (str): La parte del nombre del producto a buscar.
            
        Returns:
            list[models.Product]: Lista de productos que coinciden con la consulta.
        """
        found_products = []
        for p in self.products:
            if query.lower() in p.producto.lower():
                found_products.append(p)
        return found_products
    
    def show(self):
        """
        Muestra todos los productos registrados en un formato de tabla legible.
        """
        all_products = self.get_all_products()
        if not all_products:
            print("[INFO] No hay productos registrados.")
        else:
            print("\n--- LISTA DE PRODUCTOS ---")
            # Encabezado de la tabla
            print(f"{'Producto':<25} {'Precio':<10} {'Stock':<8}")
            print("-" * 45)
            # Imprime cada producto
            for product in all_products:
                print(f"{product.producto:<25} {product.precio:<10.2f} {product.stock:<8}")
            print("-" * 45)

class FacturaDao:
    """
    Clase DAO para gestionar las operaciones de persistencia de objetos Factura.
    """
    def __init__(self):
        """
        Inicializa FacturaDao cargando todas las facturas existentes.
        """
        self.facturas = cargar_facturas_data() # Carga la lista inicial de facturas

    def add(self, factura: models.Factura):
        """
        Agrega un nuevo objeto Factura a la lista en memoria y lo persiste en el archivo.
        
        Args:
            factura (models.Factura): El objeto Factura a añadir.
        """
        self.facturas.append(factura)
        guardar_facturas_data(self.facturas) # Guarda la lista completa actualizada
        print(f"[EXITO] Factura {factura.id_factura} guardada exitosamente.")

    def get_all_facturas(self) -> list[models.Factura]:
        """
        Retorna la lista completa de todas las facturas en memoria.
        
        Returns:
            list[models.Factura]: Lista de todas las facturas.
        """
        return self.facturas

    def find_facturas_by_client_cedula(self, cedula_cliente: str) -> list[models.Factura]:
        """
        Busca todas las facturas asociadas a una cédula de cliente específica.
        
        Args:
            cedula_cliente (str): La cédula del cliente cuyas facturas se quieren buscar.
            
        Returns:
            list[models.Factura]: Lista de facturas del cliente.
        """
        return [f for f in self.facturas if f.cliente_cedula == cedula_cliente]

    def update_factura(self, factura_actualizada: models.Factura):
        """
        Actualiza una factura existente en la lista en memoria y la persiste.
        Busca la factura por su id_factura.
        
        Args:
            factura_actualizada (models.Factura): La factura con los datos actualizados.
        """
        for i, factura in enumerate(self.facturas):
            if factura.id_factura == factura_actualizada.id_factura:
                self.facturas[i] = factura_actualizada
                guardar_facturas_data(self.facturas)
                print(f"[EXITO] Factura {factura_actualizada.id_factura} actualizada exitosamente.")
                return
        print(f"[ADVERTENCIA] Factura con ID {factura_actualizada.id_factura} no encontrada para actualizar.")

