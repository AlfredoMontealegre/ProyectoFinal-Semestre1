import os
import pickle
import Models.clases as models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Archivo para guardar datos de trabajador
ADMIN_FILENAME = 'user_admin.bin'
ADMIN_FILE_PATH = os.path.join(BASE_DIR, ADMIN_FILENAME)
# Arcihvo para guardar datos de clientes
USER_FILENAME = 'usuarios.bin'
USER_FILE_PATH = os.path.join(BASE_DIR, USER_FILENAME)
# Archivo para guardar datos de productos
PRODUCT_FILE_NAME = 'productos.bin'
PRODUCT_FILE_PATH = os.path.join(BASE_DIR, PRODUCT_FILE_NAME)
# Funciones para guardar datos de trabajadores 

def guardar_admin_user(user_admin):
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        with open(ADMIN_FILE_PATH, 'wb') as file:
            pickle.dump(user_admin, file)
            print("Usuario Guardado correctamente.")
    
    except Exception as error:
        print(f"❌ ERROR al guardar el usuario: {error}")

def cargar_admin_user():
    user_admin = []
    
    try:
        if os.path.exists(ADMIN_FILE_PATH) and os.path.getsize(ADMIN_FILE_PATH) > 0:
            with open(ADMIN_FILE_PATH, 'rb') as file:
                user_admin = pickle.load(file)
        return user_admin
    
    except FileNotFoundError:
        return []
    except EOFError:
        print(f"Advertencia: El archivo '{ADMIN_FILENAME}' está vacío o incompleto. Iniciando con lista vacía.")
        return []
    except Exception as error:
        print(f"❌ ERROR al cargar los usuarios administradores: {error}")
        return []

# Funciones para guardar y cargar datos de clienes.

def guardar_usuarios(usuarios):
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        with open(USER_FILE_PATH, 'wb') as file:
            pickle.dump(usuarios, file)
    except Exception as error:
        print(f"❌ ERROR al guardar el usuario: {error}")

def cargar_usuarios():
    usuarios = [] 
    try:
        if os.path.exists(USER_FILE_PATH) and os.path.getsize(USER_FILE_PATH) > 0:
            with open(USER_FILE_PATH, 'rb') as file:
                usuarios = pickle.load(file)
        return usuarios
    
    except FileNotFoundError:
        return []
    except EOFError:
        print(f"Advertencia: El archivo '{USER_FILENAME}' está vacío o incompleto. Iniciando con lista vacía.")
        return []
    except Exception as error:
        print(f"❌ ERROR al cargar los usuarios: {error}")
        return []

# Manejo de archivo para guardar productos
def guardar_productos(products):
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        with open(PRODUCT_FILE_PATH, 'wb') as file:
            pickle.dump(products, file)
    except Exception as error:
        print(f"❌ ERROR al guardar los productos: {error}")

def cargar_productos():
    try:
        if os.path.exists(PRODUCT_FILE_PATH) and os.path.getsize(USER_FILE_PATH) > 0:
            with open(PRODUCT_FILE_PATH, 'rb') as file:
                productos = pickle.load(file)
        return productos
    
    except (FileNotFoundError, EOFError):
        return []
    except Exception as error:
        print(f"❌ ERROR al cargar los productos: {error}")
        return []

class ClienteDao:
    def __init__(self):
        self.clientes = cargar_usuarios()
        
    def add(self, cliente):
        self.clientes.append(cliente)
        guardar_usuarios(self.clientes)
    
    def get_all_clientes(self):
        return self.clientes
    
    def update_clientes(self):
         guardar_usuarios(self.clientes)
    
    def delete_cliente(self, cedula_cliente):
        len_inicial = len(self.clientes)
        self.clientes = [c for c in self.clientes if c.cedula != cedula_cliente]
        if len(self.clientes) < len_inicial:
            guardar_usuarios(self.clientes)
            return True
        return False
    
    def find_cliente(self, query):
        found_clientes = []
        for c in self.clientes:
            if c.cedula == query or query.lower() in c.nombre.lower():
                found_clientes.append(c)
        return found_clientes
    
    def show(self):
        all_clientes = self.get_all_clientes()
        for cliente in all_clientes:
            print(cliente)
    

class AdminDao:
    def __init__(self):
        self.users = cargar_admin_user()
    
    def add(self, user):
        self.users.append(user)
        guardar_admin_user(self.users)
    
    def get_all_user_admin(self):
        return self.users
           

class ProductDao:
    def __init__(self):
        self.products = cargar_productos()
    
    def add(self, product):
        self.products.append(product)
        guardar_productos(self.products)
    
    def get_all_products(self):
        return self.products
    
    def update_products(self):
        guardar_productos(self.products)
    
    def delete_products(self, product_name):
        len_inicial = len(self.products)
        self.products = [c for c in self.products if c.producto.lower() != product_name.lower()]
        if len(self.products) < len_inicial:
            guardar_productos(self.products)
            return True
        return False
    
    def find_product(self, query):
        found_products = []
        for p in self.products:
            if query.lower() in p.producto.lower():
                found_products.append(p)
        return found_products
    
    def show(self):
        all_products = self.get_all_products()
        if not all_products:
            print("No hay productos registrados.")
        else:
            for product in all_products:
                print(product)