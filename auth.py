# auth.py
# Este archivo es para el login de los administradores.
# Aquí aprendemos a ocultar contraseñas y a guardarlas de forma segura.

import os
import pickle
import bcrypt # Usamos esto para que las contraseñas no se vean en el archivo
import getpass # Para pedir la contraseña sin que se muestre en pantalla
try:
    import pwinput # Para que salgan asteriscos (*) cuando escribes la contraseña
except ImportError:
    pwinput = None # Si no lo tienes instalado, no funciona lo de los asteriscos

# Importamos las "recetas" (clases) de nuestros usuarios y las funciones para guardar/cargar
from Models.clases import Admin 
from Dao.funciones import AdminDao, guardar_admin_users, generar_codigo_trabajador # ¡Ahora importamos esto de Dao!

def _hash_password(password: str) -> str:
    """
    Convierte una contraseña normal en una "encriptada" que nadie pueda leer.
    Así, si alguien ve el archivo, no sabrá la contraseña real. ¡Es por seguridad!
    """
    # bcrypt es como una caja fuerte para contraseñas.
    # Necesitamos convertir el texto a bytes y luego lo "hasheamos".
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def _check_password(password: str, hashed_password: str) -> bool:
    """
    Comprueba si la contraseña que el usuario escribe es igual a la que tenemos guardada (la "encriptada").
    No desencriptamos, solo comparamos si coinciden de forma segura.
    """
    try:
        # bcrypt es inteligente y compara los bytes directamente
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # Si la contraseña guardada está rota, decimos que no coincide
        return False

def crear_admin_iniciales():
    """
    Esta función mira si hay admins guardados.
    Si no hay, te pide que crees uno. Antes creaba algunos por defecto, pero ya no.
    """
    admin_dao = AdminDao() # Necesitamos hablar con la base de datos de admins
    existing_admins = admin_dao.get_all_admin_users() # Traemos la lista de admins

    if not existing_admins:
        print("ℹ️ No hay administradores. ¡Necesitas agregar uno primero!")
    else:
        print("ℹ️ Ya hay administradores registrados.")

# === TIPO 1: LOGIN BÁSICO (Para cuando no importa que se vea) ===
def login_basico() -> bool:
    """
    Login normalito, la contraseña se ve.
    """
    print("\n=== LOGIN SENCILLO ===")
    print("(Tu contraseña se va a ver aquí)")
    
    admin_dao = AdminDao() # Otra vez el objeto para manejar admins
    
    usuario_input = input("Tu nombre de usuario: ").strip() # Pedimos el nombre
    clave_input = input("Tu contraseña: ").strip() # Pedimos la contraseña (se ve)
    
    admin_user = admin_dao.find_admin_by_username(usuario_input) # Buscamos al admin por su nombre
    
    # Comprobamos: ¿Existe? ¿Tiene contraseña? ¿Coincide la contraseña?
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Entraste! ¡Bienvenido!")
        return True
    else:
        print("❌ ¡Usuario o contraseña incorrectos!")
        return False

# === TIPO 2: LOGIN CON GETPASS (Para que no se vea la contraseña) ===
def login_con_getpass() -> bool:
    """
    Login donde la contraseña no se ve cuando la escribes.
    """
    if getpass is None:
        print("❌ ¡UPS! No puedo ocultar la contraseña. Usaremos el login sencillo.")
        return login_basico() # Si falla, volvemos al básico
    
    print("\n=== LOGIN OCULTO ===")
    print("(La contraseña NO se ve mientras escribes)")
    
    admin_dao = AdminDao()
    
    usuario_input = input("Tu nombre de usuario: ").strip()
    clave_input = getpass.getpass("Tu contraseña: ") # Aquí se oculta mágicamente
    
    admin_user = admin_dao.find_admin_by_username(usuario_input)
    
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Entraste! ¡Bienvenido!")
        return True
    else:
        print("❌ ¡Usuario o contraseña incorrectos!")
        return False
            
# === TIPO 3: LOGIN CON ASTERISCOS (Para que salgan estrellitas) ===
def login_con_asteriscos() -> bool:
    """
    Login donde ves estrellitas (*) cuando escribes la contraseña. ¡Más bonito!
    """
    if pwinput is None:
        print("❌ ¡Uy! Para los asteriscos, necesitas instalar 'pwinput'. Prueba con 'pip install pwinput'.")
        return False # No podemos hacer este login sin la librería

    print("\n=== LOGIN CON ESTRELLITAS ===")
    print("(Verás * mientras escribes)")
    
    admin_dao = AdminDao()
    
    usuario_input = input("Tu nombre de usuario: ").strip()
    clave_input = pwinput.pwinput("Tu contraseña: ", mask="*") # Aquí salen los asteriscos
    
    admin_user = admin_dao.find_admin_by_username(usuario_input)
    
    if admin_user and admin_user.password_hashed and _check_password(clave_input, admin_user.password_hashed):
        print("✅ ¡Entraste! ¡Bienvenido!")
        return True
    else:
        print("❌ ¡Usuario o contraseña incorrectos!")
        return False

def mostrar_usuarios_disponibles():
    """
    Muestra los nombres de los administradores que ya están registrados.
    Así puedes recordar quiénes son.
    """
    admin_dao = AdminDao()
    admins = admin_dao.get_all_admin_users()
    
    print("\nℹ️ Aquí están los nombres de admins que puedes usar para entrar:")
    if admins:
        for admin_user in admins:
            print(f"- {admin_user.nombre} (Código: {admin_user.codigo})")
    else:
        print("¡No hay admins registrados! Crea uno con la opción 5.")
    print("Nota: Las contraseñas están ocultas por seguridad.")

def agregar_nuevo_admin():
    """
    Para crear un nuevo usuario administrador.
    Pedimos los datos y el CÓDIGO se genera automáticamente.
    """
    print("\n--- AGREGAR ADMIN NUEVO ---")
    admin_dao = AdminDao() # Necesitamos hablar con la base de datos de admins
    
    # Pedimos el nombre completo
    nombre = input("Nombres y Apellidos del nuevo administrador: ").strip()
    if not nombre:
        print("❌ ERROR: El nombre no puede estar vacío.")
        return False

    # Revisamos si ya existe alguien con ese nombre de usuario (el nombre es el usuario en este contexto)
    if admin_dao.find_admin_by_username(nombre):
        print(f"⚠️ ¡Cuidado! Ya existe un admin con el nombre '{nombre}'. Elige otro.")
        return False

    # Generamos el código automáticamente
    existing_admins = admin_dao.get_all_admin_users() # Para asegurar unicidad
    codigo_generado = generar_codigo_trabajador(nombre, existing_admins)
    print(f"✔️ Código de trabajador generado: {codigo_generado}") # ¡Lo mostramos!

    # Pedimos la cédula (debe tener 13 números y 1 letra)
    cedula = input("Cédula (13 números y 1 letra, ej: 0012345678901A): ").strip()
    if not (len(cedula) == 14 and cedula[:-1].isdigit() and cedula[-1].isalpha()):
        print("❌ ERROR: La cédula no tiene el formato correcto (13 números + 1 letra).")
        return False
    cedula = cedula[:-1] + cedula[-1].upper() # La letra siempre en mayúscula

    # Pedimos el teléfono (8 números y que empiece bien)
    telefono = input("Teléfono (8 números, empieza con 2, 5, 7 u 8): ").strip()
    if not (len(telefono) == 8 and telefono.isdigit() and telefono.startswith(('2', '5', '7', '8'))):
        print("❌ ERROR: El número de teléfono no es válido.")
        return False

    # Pedimos la contraseña (no puede estar vacía)
    clave_input = getpass.getpass("Contraseña: ") 
    if not clave_input:
        print("❌ ERROR: La contraseña no puede estar vacía.")
        return False

    hashed_password = _hash_password(clave_input) # "Encriptamos" la contraseña
    
    # Creamos el objeto del nuevo admin
    # ¡Usamos el codigo_generado aquí!
    new_admin = Admin(nombre, codigo_generado, cedula, telefono, hashed_password)
    
    # Lo intentamos agregar. El programa nos dirá si funcionó.
    if admin_dao.add(new_admin): 
        print(f"✅ ¡Admin '{nombre}' agregado con éxito! Tu usuario para iniciar sesión es: {codigo_generado}")
        return True
    else:
        print("❌ Algo falló al agregar el admin.")
        return False

def seleccionar_tipo_login() -> bool:
    """
    Muestra las opciones de cómo quieres iniciar sesión como admin.
    """
    print("\n" + "="*60)
    print("          SISTEMA DE AUTENTICACIÓN")
    print("="*60)
    print("Elige cómo quieres entrar al sistema:")
    print("1. Login Básico (la contraseña se ve)")
    print("2. Login con getpass (la contraseña se oculta)")
    print("3. Login con asteriscos (ves * al escribir)")
    print("4. Ver los usuarios administradores (por si los olvidaste)")
    print("5. ¡Agregar un admin nuevo!")
    print("="*50)
    
    while True:
        opcion = input("Escribe el número de tu opción (1-5): ").strip()
        
        if opcion == "1":
            return login_basico()
        elif opcion == "2":
            return login_con_getpass()
        elif opcion == "3":
            return login_con_asteriscos()
        elif opcion == "4":
            mostrar_usuarios_disponibles() # Muestra y luego te deja elegir otra opción
            continue 
        elif opcion == "5":
            agregar_nuevo_admin() # Agrega y luego te deja elegir otra opción
            continue 
        else:
            print("🛑 ¡Esa opción no existe! Elige 1, 2, 3, 4 o 5.")

def inicializar_auth() -> bool:
    """
    Función principal para empezar con el login de admins.
    Primero revisa que tengamos admins y luego te da las opciones.
    """
    crear_admin_iniciales() # Asegura que tengamos admins (o te avisa si no hay)
    return seleccionar_tipo_login() # Inicia el menú de login
