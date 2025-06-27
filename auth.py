# auth.py
# Este módulo se encarga de la autenticación de los usuarios administradores.
# Implementa diferentes tipos de login (básico, getpass, asteriscos)
# y gestiona el hashing seguro de contraseñas con bcrypt.
# Se integra con AdminDao para la gestión de usuarios administradores.

import os
import pickle
import bcrypt # Importamos bcrypt para el hashing seguro de contraseñas
import getpass # Módulo estándar para pedir contraseñas sin que se vean
try:
    import pwinput # Librería de terceros para mostrar asteriscos al escribir contraseña
except ImportError:
    pwinput = None # Si pwinput no está instalado, la funcionalidad no estará disponible

# Importar las clases de modelos y las funciones/clases DAO necesarias
from Models.clases import Admin # Necesitamos la clase Admin para crear objetos de usuario
from Dao.funciones import AdminDao, guardar_admin_users # Necesitamos AdminDao para interactuar con los datos de admin, y guardar_admin_users para la inicialización

def _hash_password(password: str) -> str:
    """
    Hashea una contraseña usando el algoritmo bcrypt.
    Genera un 'salt' aleatorio para cada hash, lo que hace que sea más seguro
    contra ataques de tablas arcoíris.
    
    Args:
        password (str): La contraseña en texto plano a hashear.
        
    Returns:
        str: La contraseña hasheada como una cadena de texto (UTF-8 decodificada).
    """
    # bcrypt.gensalt() genera un salt aleatorio (costo por defecto es 12)
    # bcrypt.hashpw() hashea la contraseña. Espera bytes, por eso se codifica a 'utf-8'.
    # .decode('utf-8') es necesario porque hashpw retorna bytes y queremos una cadena.
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def _check_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada
    previamente utilizando bcrypt.
    
    Args:
        password (str): La contraseña en texto plano proporcionada por el usuario.
        hashed_password (str): La contraseña hasheada almacenada.
        
    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    try:
        # bcrypt.checkpw espera ambos argumentos como bytes
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # Si el hashed_password no es un hash bcrypt válido (ej. formato incorrecto),
        # bcrypt.checkpw lanzará un ValueError. En este caso, la verificación falla.
        return False

def crear_admin_iniciales():
    """
    Función de inicialización que asegura la existencia de usuarios administradores por defecto.
    Si el archivo de administradores está vacío o no existe, crea un conjunto de usuarios
    administradores predefinidos con contraseñas hasheadas y los guarda.
    """
    admin_dao = AdminDao() # Instancia el DAO para acceder a los datos de administradores
    existing_admins = admin_dao.get_all_admin_users() # Carga los administradores existentes

    # Si no hay administradores cargados, significa que el archivo está vacío o no existe
    if not existing_admins:
        print("ℹ️  No se encontraron administradores existentes. Creando usuarios administradores por defecto.")
        
        # Define los usuarios administradores por defecto
        # Las contraseñas se hashean utilizando la función _hash_password
        admin_default = Admin(
            nombre="admin", 
            codigo="ADM001", 
            cedula="000000001A0000", # Cédula de 14 caracteres (13 digitos + 1 letra)
            telefono="88887777", 
            password_hashed=_hash_password("admin123")
        )
        juan_default = Admin(
            nombre="juan", 
            codigo="USR001", 
            cedula="000000002B0000", # Cédula de 14 caracteres (13 digitos + 1 letra)
            telefono="88886666", 
            password_hashed=_hash_password("clave456")
        )
        estudiante_default = Admin(
            nombre="estudiante", 
            codigo="EST001", 
            cedula="000000003C0000", # Cédula de 14 caracteres (13 digitos + 1 letra)
            telefono="88885555", 
            password_hashed=_hash_password("password789")
        )

        # Guarda la lista de administradores por defecto usando la función DAO de guardado
        guardar_admin_users([admin_default, juan_default, estudiante_default])
        print("✅ Usuarios administradores por defecto guardados.")
    else:
        print("ℹ️  Usuarios administradores ya existen. Saltando creación de usuarios por defecto.")

# === TIPO 1: LOGIN BÁSICO ===
def login_basico() -> bool:
    """
    Permite el inicio de sesión con una interfaz básica donde la contraseña es visible.
    Verifica las credenciales del usuario (nombre y contraseña hasheada).
    
    Returns:
        bool: True si el login es exitoso, False en caso contrario.
    """
    print("\n=== LOGIN BÁSICO ===")
    print("(La contraseña se ve mientras escribes)")
    
    admin_dao = AdminDao() # Instancia el DAO para obtener los usuarios administradores
    
    usuario_input = input("Usuario: ").strip() # Pide el nombre de usuario
    clave_input = input("Contraseña: ").strip() # Pide la contraseña (visible)
    
    admin_user = admin_dao.find_admin_by_username(usuario_input) # Busca el usuario por su nombre
    
    # Verifica si el usuario existe, tiene una contraseña hasheada y si la contraseña coincide
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Acceso exitoso!")
        return True
    else:
        print("❌ Usuario o contraseña incorrectos")
        return False

# === TIPO 2: LOGIN CON GETPASS ===
def login_con_getpass() -> bool:
    """
    Permite el inicio de sesión ocultando la contraseña mediante el módulo `getpass`.
    Verifica las credenciales del usuario (nombre y contraseña hasheada).
    
    Returns:
        bool: True si el login es exitoso, False en caso contrario.
    """
    if getpass is None:
        # Si getpass no está disponible (ej. en ciertos entornos IDE), informa al usuario
        print("❌ ERROR: El módulo 'getpass' no está disponible en este entorno.")
        return login_basico() # Recurre al login básico si getpass no se puede usar

    print("\n=== LOGIN CON GETPASS ===")
    print("(La contraseña se oculta mientras escribes)")
    
    admin_dao = AdminDao()
    
    usuario_input = input("Usuario: ").strip()
    clave_input = getpass.getpass("Contraseña: ") # Pide la contraseña sin eco (oculta)
    
    admin_user = admin_dao.find_admin_by_username(usuario_input)
    
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Acceso exitoso!")
        return True
    else:
        print("❌ Usuario o contraseña incorrectos")
        return False
            
# === TIPO 3: LOGIN CON ASTERISCOS ===
def login_con_asteriscos() -> bool:
    """
    Permite el inicio de sesión mostrando asteriscos (*) mientras se escribe la contraseña,
    utilizando el módulo `pwinput`.
    Si `pwinput` no está instalado, informa al usuario y no permite esta opción de login.
    
    Returns:
        bool: True si el login es exitoso, False en caso contrario.
    """
    if pwinput is None:
        # Si pwinput no está disponible, informa al usuario y no permite el login para esta opción.
        print("❌ ERROR: El módulo 'pwinput' no está instalado. No se puede mostrar asteriscos.")
        print("Para instalarlo, ejecuta: pip install pwinput")
        return False # No permite el inicio de sesión sin pwinput para esta opción

    print("\n=== LOGIN CON ASTERISCOS ===")
    print("(Se muestran * mientras escribes)")
    
    admin_dao = AdminDao()
    
    usuario_input = input("Usuario: ").strip()
    clave_input = pwinput.pwinput("Contraseña: ", mask="*") # Pide la contraseña mostrando asteriscos
    
    admin_user = admin_dao.find_admin_by_username(usuario_input)
    
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Acceso exitoso!")
        return True
    else:
        print("❌ Usuario o contraseña incorrectos")
        return False

def mostrar_usuarios_disponibles():
    """
    Muestra una lista de los nombres de usuario de los administradores registrados en el sistema.
    Útil para pruebas o recordatorios de credenciales.
    """
    admin_dao = AdminDao()
    admins = admin_dao.get_all_admin_users()
    
    print("\nℹ️  Usuarios administradores disponibles:")
    if admins:
        for admin_user in admins:
            print(f"- {admin_user.nombre} (Código: {admin_user.codigo})")
    else:
        print("No hay usuarios administradores registrados. Intenta agregando uno.")
    print("Nota: Las contraseñas se almacenan hasheadas para seguridad.")

def agregar_nuevo_admin():
    """
    Permite al usuario agregar un nuevo usuario administrador al sistema a través de la consola.
    Incluye validaciones para los datos de entrada y hashea la contraseña.
    """
    print("\n--- AGREGAR NUEVO ADMINISTRADOR ---")
    admin_dao = AdminDao()
    
    # Solicita y valida el nombre de usuario
    nombre = input("Nombre de usuario (ej: 'nuevo_admin'): ").strip()
    if not nombre:
        print("❌ ERROR: El nombre de usuario no puede estar vacío.")
        return False

    # Valida que el nombre de usuario no exista ya en la base de datos de administradores
    if admin_dao.find_admin_by_username(nombre):
        print(f"⚠️  ADVERTENCIA: El nombre de usuario '{nombre}' ya existe. Elija otro.")
        return False

    # Solicita y valida el código de administrador
    codigo = input("Código de administrador (ej: 'ADM002'): ").strip()
    if not codigo:
        print("❌ ERROR: El código no puede estar vacío.")
        return False

    # Solicita y valida la cédula (formato específico de 13 números + 1 letra)
    cedula = input("Cédula (13 números y 1 letra, ej: 0012345678901A): ").strip()
    if not (len(cedula) == 14 and cedula[:-1].isdigit() and cedula[-1].isalpha()):
        print("❌ ERROR: La cédula debe contener 13 dígitos numéricos seguidos de una letra (ej: 0012345678901A).")
        return False
    cedula = cedula[:-1] + cedula[-1].upper() # Asegura que la letra final sea mayúscula

    telefono = input("Teléfono (8 dígitos, inicia con 2,5,7,8): ").strip()
    if not (len(telefono) == 8 and telefono.isdigit() and telefono.startswith(('2', '5', '7', '8'))):
        print("❌ ERROR: El número de teléfono no es válido. Debe tener 8 dígitos y comenzar con 2, 5, 7 u 8.")
        return False


    clave_input = getpass.getpass("Contraseña: ") 
    if not clave_input:
        print("❌ ERROR: La contraseña no puede estar vacía.")
        return False

    hashed_password = _hash_password(clave_input) # Hashea la contraseña con bcrypt
    
    # Crea un nuevo objeto Admin
    new_admin = Admin(nombre, codigo, cedula, telefono, hashed_password)
    
    # Añadir el nuevo administrador usando el DAO. El método add del DAO
    # ya maneja la persistencia y la impresión de mensajes de éxito/error.
    if admin_dao.add(new_admin): 
        print(f"✅ Administrador '{nombre}' agregado exitosamente.")
        return True
    else:
        print("❌ ERROR: No se pudo agregar el administrador.")
        return False

def seleccionar_tipo_login() -> bool:
    """
    Muestra un menú interactivo para que el usuario elija el tipo de login deseado
    o realice otras acciones relacionadas con la autenticación de administradores.
    
    Returns:
        bool: True si el usuario inicia sesión exitosamente, False si elige salir
              o si el login falla después de los intentos permitidos.
    """
    print("\n" + "="*60)
    print("          SISTEMA DE AUTENTICACIÓN")
    print("="*60)
    print("Selecciona el tipo de login que quieres usar:")
    print("1. Login Básico (se ve la contraseña)")
    print("2. Login con getpass (oculta la contraseña)")
    print("3. Login con asteriscos (muestra *)")
    print("4. Ver usuarios administradores disponibles")
    print("5. Agregar nuevo usuario administrador")
    print("="*50)
    
    while True:
        opcion = input("Elige una opción (1-5): ").strip()
        
        if opcion == "1":
            return login_basico()
        elif opcion == "2":
            return login_con_getpass()
        elif opcion == "3":
            return login_con_asteriscos()
        elif opcion == "4":
            mostrar_usuarios_disponibles() # Muestra los usuarios y luego vuelve a este menú
            continue # Continúa el bucle para que el usuario pueda elegir una opción de login
        elif opcion == "5":
            agregar_nuevo_admin() # Permite agregar un admin y luego vuelve a este menú
            continue # Continúa el bucle para que el usuario pueda elegir una opción de login
        else:
            print("🛑 ERROR: Opción no válida. Elija 1, 2, 3, 4 o 5.")

def inicializar_auth() -> bool:
    """
    Punto de entrada principal para la gestión de autenticación de administradores.
    Asegura que los usuarios administradores por defecto existan y luego presenta
    al usuario el menú de opciones de login.
    
    Returns:
        bool: True si el usuario se autentica exitosamente, False si no.
    """
    crear_admin_iniciales() # Se asegura que los usuarios admin iniciales estén en el archivo
    return seleccionar_tipo_login() # Inicia el proceso de selección de login

