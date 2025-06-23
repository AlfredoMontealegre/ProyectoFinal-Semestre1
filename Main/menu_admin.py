# Desarrollo de programa para manejo de datos de la empresa

import Dao.funciones as dao
import Models.clases as models
import os
import sys
import bcrypt
import json

ADMIN_FILENAME = 'user_admin.txt'
ADMIN_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ADMIN_FILENAME)
# Arhivo de usuarios registrados para la visualizacion de los mismos
USER_FILENAME = 'usuarios.txt'
USER_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), USER_FILENAME)

users = dao.AdminDao()
clientes = dao.ClienteDao()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def inicio():
    print("""
          ==================================
          ---------> GLOBAL TOOLS S.A
          -------> [ADMIN USER]
          
          -> ¿Tienes cuenta de trabajador? <-
          
            [1] SI, INICIAR SESIÓN
            [2] NO, AÚN NO ME HAN BRINDADO MI CÓDIGO
            [3] SALIR DEL PROGRAMA
        
          ==================================
          """)

def menu_registrar():
    print("""
                [1] Crear una cuenta nueva (Requiere código de trabajdor)
                [2] Regresar al menú principal
                [3] Salir del programa
          """)

def menu(user):
    print(f"""
        ==================================================
        --------- ¡¡Bienvenido {user.upper()}!! ---------
        --------------------------------------------------
        ----------- ¿Qué desea realizar hoy? ------------
        
                    [1] Control de Inventario
                    [2] Control de Clientes
                    [3] Salir de la sesión
                    [4] Salir del programa
        ==================================================
          """)

def menu_inventario():
    print("""
          ------ CONTROL DE INVENTARIO ------
          
            [1] Ver Todos los Productos
            [2] Agregar Nuevo Producto
            [3] Editar Producto Existente
            [4] Eliminar Producto
            [5] Buscar Producto por ID/Nombre
            [6] Regresar al menú principal
            [7] Salir del programa
        
          -----------------------------------
          """)

def menu_control_clientes():
    print("""
        ----------- GESTIÓN DE CLIENTES -----------
          
            [1] Ver Todos los Clientes Registrados
            [2] Editar Información de Cliente
            [3] Eliminar Cliente
            [4] Agregar Cliente Manualmente (Solo Admin)
            [5] Buscar Cliente por Cédula/Nombre
            [6] Regresar al menú principal
            [7] Salir del programa
        
        -------------------------------------------
          """)
    
def ver_clientes():
    cls()
    print("---- LISTA DE CLIENTES ---- ")
    cliente_cargados = clientes.get_all_clientes()
    if not clientes:
        print("No hay clientes Registrados.")
    
    else:
        for c in cliente_cargados:
            print(c)
    input("Presione ENTER para continuar...")

def agregar_clientes():
    cls()
    print("---- AGREGAR CLIENTE ----")
    nombre = validar_input("Nombre del Cliente: ", 'str')
    cedula = validar_input("Cédula del Cliente: ", 'cedula')
    telefono = validar_input("Teléfono del Cliente: ", 'tel')
    contraseña = validar_input("Contraseña del Cliente: ", permitir_char_password=True)
    
    contraseña_hasheada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode()
    
    nuevo_cliente = {
        "nombre": nombre,
        "cedula": cedula,
        "telefono": telefono,
        "password_hashed": contraseña_hasheada
    }
    
    clientes_actuales = cargar_usuario()
    for c in clientes_actuales:
        if c['cedula'] == cedula:
            print(f"❌ ERROR: Ya existe un cliente con la cédula '{cedula}'.")
            input("Presione ENTER para continuar...")
            return

    clientes_actuales.append(nuevo_cliente)
    guardar_usuario(clientes_actuales)
        
    temp_cliente_obj = models.Cliente(nombre, cedula, telefono)
    temp_cliente_obj.contraseña_hashed = contraseña_hasheada
    clientes.add(temp_cliente_obj)
    
    print(f"✔️ Cliente '{nombre}' agregado con éxito.")
    input("Presione ENTER para continuar...")    

def editar_cliente():
    cls()
    print("---- EDITAR CLIENTE EXISTENTE ----")
    usuario_a_editar = validar_input("Ingrese la cédula del usuario que desea editar: ", 'cedula')
    cliente_actual = cargar_usuario()
    cliente_encontrado = None
    for i, c in enumerate(cliente_actual):
        if c['cedula'] == usuario_a_editar:
            cliente_encontrado = c
            indice_cliente= i
            break
        
    if not cliente_encontrado:
        print(f"❌ No se encontró un cliente con la cédula '{usuario_a_editar}'")
        input("Presiona ENTER para continuar...")
        return
    print(f"\n--- Cliente actual: {cliente_encontrado['nombre']} (Cédula: {cliente_encontrado['cedula']}) ---")
    print(f"1. Nombre actual: {cliente_encontrado['nombre']}")
    print(f"2. Teléfono actual: {cliente_encontrado['telefono']}")
    print("--------------------------------------------------")
    
    print("\nDeje en blanco si no deseas cambiar el valor.")
    
    cambios_realizados = False
    
    nuevo_nombre = validar_input(f"Nuevo Nombre {cliente_encontrado['nombre']}: ", 'str')
    if nuevo_nombre:
        cliente_encontrado['nombre'] = nuevo_nombre
        cambios_realizados = True
    
    nuevo_telefono = validar_input(f"Nuevo Teléfono {cliente_encontrado['telefono']}: ", 'tel')
    if nuevo_telefono:
        cliente_encontrado['telefono'] = nuevo_telefono
        cambios_realizados = True
    
    nueva_contraseña = validar_input(f"Nueva Contraseña: ", permitir_char_password=True)
    if nueva_contraseña:
        nueva_contraseña_hasheada = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cliente_encontrado['contraseña_hash'] = nueva_contraseña_hasheada
        print("✔️ Contraseña del cliente actualizada.")
        cambios_realizados = True

    if cambios_realizados:
        cliente_actual[indice_cliente] = cliente_encontrado
        guardar_usuario(cliente_actual)
        
        cliente_en_dao = None 
        for c in clientes.clientes:
            if c.cedula == usuario_a_editar:
                cliente_en_dao = c
                break
        
        if cliente_en_dao:
            cliente_en_dao.nombre = cliente_encontrado['nombre']
            cliente_en_dao.telefono = cliente_encontrado['telefono']
            print("✔️ Información del cliente actualizada en memoria.")
        
        else:
            print("⚠️ Cliente no encontrado en la lista en memoria del DAO. Reinicia para sincronizar.")

        print(f"✔️ Cliente con cédula '{usuario_a_editar}' actualizado con éxito.")
    
    else:
        print("No se realizaron cambios.")
    
    input("Presione ENTER para continuar...")

def eliminar_cliente():
    cls()
    print("---- ELIMINAR CLIENTE ----")
    usuario_a_eliminar = validar_input("Ingrese la cédula del cliente que desea eliminar: ", 'cedula')
    clientes_actuales = cargar_usuario()
    clientes_restantes = [c for c in clientes_actuales if c['cedula']]
    
    if len(clientes_restantes) < len(clientes_actuales):
        guardar_usuario(clientes_restantes)
        clientes.delete_cliente(usuario_a_eliminar)
        print(f"✔️ Cliente con cédula '{usuario_a_eliminar}' eliminado con éxito.")
    
    else:
        print(f"❌ ERROR: Cliente con cédula '{usuario_a_eliminar}' no encontrado.")
    input("Presione ENTER para continuar...")

def ver_clientes():
    cls()
    print("---- LISTA DE CLIENTES ----")
    clientes_cargados = clientes.get_all_clientes()
    if not clientes_cargados:
        print("No hay clientes Registrados.")
    else:
        for c in clientes_cargados:
            print(c)
    
    input("Presione ENTER para continuar...")

def buscar_cliente():
    cls()
    print("---- BUSCAR CLIENTE ----")
    usuario_a_buscar = input("Ingrese Cédula o parte del Nombre del Cliente a buscar: ").strip()
    clientes_encontrados = clientes.find_cliente(usuario_a_buscar)
    
    if clientes_encontrados:
        print("---- CLIENTES ENCONTRADOS ----")
        for cliente in clientes_encontrados:
            print(cliente)
    
    else:
        print(f"❌ No se encontraron clientes que coincidan con '{usuario_a_buscar}'.")
    
    input("Presione ENTER para continuar...")
    

def guardar_usuario(user_obj, password_str):
    usuarios = cargar_usuario()

    password_hashed = bcrypt.hashpw(password_str.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    nuevo_trabajador = {
        "codigo": user_obj.codigo,
        "nombre": user_obj.nombre,
        "cedula": user_obj.cedula,
        "telefono": user_obj.telefono,
        "password_hashed": password_hashed
    }
    
    usuarios.append(nuevo_trabajador)
    
    try:
        os.makedirs(os.path.dirname(ADMIN_FILE_PATH), exist_ok=True)
        with open(ADMIN_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4)
            print("Usuario Guardado correctamente.")
    
    except Exception as error:
        print(f"❌ ERROR al guardar el usuario: {error}")

def cargar_usuario():
    usuarios = []
    
    try:
        os.makedirs(os.path.dirname(ADMIN_FILE_PATH), exist_ok=True)
        if os.path.exists(ADMIN_FILE_PATH) and os.path.getsize(ADMIN_FILE_PATH) > 0:
            with open(ADMIN_FILE_PATH, 'r', encoding='utf-8') as file:
                usuarios = json.load(file)
        
        else:
            return []
    
    except json.JSONDecodeError as error:
        print(f"❌ ERROR: El archivo de usuarios está corrupto o mal formado (JSON). Iniciando con lista vacía. Detalle: {error}")
    except Exception as e:
        print(f"❌ ERROR al cargar los usuarios: {e}")
        return []
    return usuarios
                

def registrar_usuario():
    cls()
    print("""
          ------ REGISTRO DE NUEVO TRABAJADOR ------
          """)
    nombre_completo = validar_input("Nombre y Apellidos: ", 'str')
    codigo = validar_input("Ingrese su código de trabajador: ", 'codigo')
    telefono = validar_input("Ingrese su número telefónico: ", 'tel')
    cedula = validar_input("Digite su número de Cédula (sin guiones): ", 'cedula')
    
    usuario_existentes = cargar_usuario()
    
    for user in usuario_existentes:
        if user["cedula"] == cedula:
            print("❌ ERROR: Ya existe una cuenta con esta cédula. Intente iniciar sesión.")
            input("Presione ENTER para continuar...")
            return None
        if user["codigo"] == codigo: 
            print("❌ ERROR: Ya existe una cuenta con este código de trabajador. Intente con uno diferente.")
            input("Presione ENTER para continuar...")
            return None
        
    password = validar_input("Cree su contraseña: ", permitir_char_password=True)
    nuevo_trabajador = models.Admin(nombre_completo, codigo, cedula, telefono)
    
    users.add(nuevo_trabajador)
    guardar_usuario(nuevo_trabajador, password)
    
    print("\n¡¡Registro Existoso. Ahora puede inciar Sesión.")
    input("Presiona ENTER para continuar...")
    return nuevo_trabajador

def iniciar_sesion():
    print("""
          ====== INICIAR SESIÓN ======
          """)
    
    codigo_input = validar_input("Ingrese el código de trabajador: ", 'codigo')
    password_input = validar_input("Contraseña: ", permitir_char_password=True)
    
    usuarios_cargados = cargar_usuario()
    
    for user_data in usuarios_cargados:
        if user_data['codigo'] == codigo_input:
            if bcrypt.checkpw(password_input.encode('utf-8'), user_data['password_hashed'].encode('utf-8')):
                print(f"¡¡Bienvenido {user_data['nombre']}!!")
                input("Presiona ENTER para continuar...")
                return models.Admin(user_data['nombre'], user_data['codigo'], user_data['cedula'], user_data['telefono'])
            
            else:
                print("\n❌ Codigo o Contraseña incorrectos. Intente Nuevamente.")
                input("Presione Enter para continuar...")
                return None
    
    print("\n❌ Codigo o Contraseña Incorrectos. Intente nuevamente.")
    input("Presione ENTER para continuar...")
    return None
    

def validar_input(mensaje, tipo='str', permitir_char_password=False):
    while True:
        entrada = input(mensaje).strip()
    
        if not entrada:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
            continue
    
        if tipo == 'str':
            if not permitir_char_password:
                if not entrada.replace(" ", "").isalpha():
                    print("❌ ERROR. Ingrese un dato válido (solo letras).")
                    continue
        
        elif tipo == 'codigo':
            if not entrada.isalnum():
                print("🟡 El código de trabajador no es válido (ej. atorresp07). Intente nuevamente.")
                continue
            
            inicial_nom = [char for char in entrada if char.isalpha()]
            codigo_unico = [char for char in entrada if char.isdigit()]
            
            if len(inicial_nom) != 8 or len(codigo_unico) != 2 or len(inicial_nom) + len(codigo_unico) != len(entrada):
                print("El formato del código de trabajador es incorrecto (debe tener 8 letras seguidas de 2 números).")
                continue
        
        elif tipo == 'tel':
            if not entrada.isdigit() or len(entrada) != 8 or not entrada.startswith(("8", "7", "5", "2")):
                print("🟡 El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                continue
            
        elif tipo == 'cedula':
            if not entrada.isalnum():
                print("❌ ERROR. La cédula solo puede contener letras y números.")
            
            letras = [char for char in entrada if char.isalpha()]
            numeros = [char for char in entrada if char.isdigit()]
            
            if len(numeros) != 13 or len(letras) != 1 or len(numeros) + len(letras) != len(entrada):
                print("❌ ERROR. Datos de cédula inválidos (debe tener 13 números y 1 letra).")
                continue
        return entrada

def obtener_opcion_menu_principal(main_menu=True):
    while True:
        respuesta = input(">>> ").strip()
        
        if not respuesta:
            print("⚠️  CAMPO VACÍO. Intente nuevamente.")
            continue
        
        elif not respuesta.isdigit():
            print("❌ Error. Datos no permitidos. Ingrese un número.")
            continue
        
        else:
            if main_menu:
                if respuesta in ['1', '2']:
                    return respuesta
                elif respuesta == '3':
                    return 'salir_principal'
                else:
                    print("🛑 Ingrese una opción válida (1, 2 o 3).")
                    continue
                
            else:
                if respuesta == '1':
                    return respuesta
                elif respuesta == '2':
                    return 'regresar'
                elif respuesta == '3':
                    return 'salir_principal'
                else:
                    print("🛑 Ingrese una opción válida (1, 2, o 3).")
                    continue

def obtener_opcion_submenu(tipo_menu='menu_usuario_principal'):
    opcion = input(">>> ").strip()
    
    if not opcion:
        print("⚠️  CAMPO VACÍO. Intente nuevamente.")
    
    elif not opcion.isdigit():
        print("❌ Error. Datos no permitidos. Ingrese un número.")
    
    else:
        if tipo_menu == 'menu_usuario_principal':
            if opcion in ['1', '2']:
                return opcion
            elif opcion == '3':
                return 'regresar'
            elif opcion == '4':
                return 'salir_principal'
            else:
                print("🛑 Ingrese una opción válida (1, 2, 3 o 4).")
            
        elif tipo_menu == 'menu_inventario' or tipo_menu == 'menu_control_clientes':
                if opcion in ['1', '2', '3', '4', '5']:
                    return opcion
                elif opcion == '6':
                    return 'regresar'
                elif opcion == '7':
                    return 'salir_principal'
                else:
                    print("🛑 Ingrese una opción válida (1, 2, 3, 4, 5, 6 o 7).")
          
def salir_programa():
    print("¡Gracias por usar el programa! Saliendo...")
    input("Presione ENTER para continuar...")
    sys.exit()

def main():
    while True:
        cls()
        inicio()
        opcion = obtener_opcion_menu_principal(main_menu=True)
        
        if opcion == '1':
            cls()
            sesion_trabajdor = iniciar_sesion()
            if sesion_trabajdor:
                while True:
                    cls()
                    menu(sesion_trabajdor.nombre)
                    opcion_elegida = obtener_opcion_submenu(tipo_menu='menu_usuario_principal')
                    if opcion_elegida == '1':
                        cls()
                        menu_inventario()
                        input("Presiona ENTER para continuar...")
                    elif opcion_elegida == '2':
                        while True:
                            cls()
                            menu_control_clientes()
                            opc = obtener_opcion_submenu(tipo_menu='menu_control_clientes')
                            if opc == '1':
                                ver_clientes()
                            elif opc == '2':
                                editar_cliente()
                            elif opc == '3':
                                eliminar_cliente()
                            elif opc == '4':
                                agregar_clientes()
                            elif opc == '5':
                                buscar_cliente()
                            elif opc == 'regresar':
                                break
                            elif opc == 'salir_principal':
                                salir_programa()
                            
                    elif opcion_elegida == 'regresar':
                        break
                    elif opcion_elegida == 'salir_principal':
                        salir_programa()
            else:
                continue
        
        elif opcion == '2':
            while True:
                cls()
                menu_registrar()
            
                sub_accion = obtener_opcion_menu_principal(main_menu=False)
            
                if sub_accion == '1':
                    registrar_usuario()
                elif sub_accion == 'regresar':
                    break
                elif sub_accion == 'salir_principal':
                    salir_programa()
                else:
                    continue
        
        elif opcion == 'salir_principal':
            salir_programa()
        
        else:
            continue

main()
                
