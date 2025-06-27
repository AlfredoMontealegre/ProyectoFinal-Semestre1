# Desarrollo de programa para manejo de datos de la empresa

import Dao.funciones as dao
import Models.clases as models
import os
import sys
import bcrypt


users = dao.AdminDao()
clientes = dao.ClienteDao()
productos = dao.ProductDao()

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
                ----------------- ¿Qué desea realizar? -----------------
        
                [1] Crear una cuenta nueva (Requiere código de trabajdor)
                [2] Regresar al menú principal
                [3] Salir del programa
          """)

def menu(user_name):
    print(f"""
        ==================================================
        --------- ¡¡Bienvenido {user_name.upper()}!! ---------
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

def registrar_usuario():
    cls()
    print("""
          ------ REGISTRO DE NUEVO TRABAJADOR ------
          """)
    nombre_completo = validar_input("Nombre y Apellidos: ", 'str')
    codigo = validar_input("Ingrese su código de trabajador: ", 'codigo')
    telefono = validar_input("Ingrese su número telefónico: ", 'tel')
    cedula = validar_input("Digite su número de Cédula (sin guiones): ", 'cedula')
    
    usuario_existentes = users.get_all_user_admin()
    
    for user in usuario_existentes:
        if user.cedula == cedula:
            print("❌ ERROR: Ya existe una cuenta con esta cédula. Intente iniciar sesión.")
            input("Presione ENTER para continuar...")
            return None
        if user.codigo == codigo: 
            print("❌ ERROR: Ya existe una cuenta con este código de trabajador. Intente con uno diferente.")
            input("Presione ENTER para continuar...")
            return None
        
    password = validar_input("Cree su contraseña: ", permitir_char_password=True)
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    nuevo_trabajador = models.Admin(nombre_completo, codigo, cedula, telefono)
    nuevo_trabajador.password_hashed = password_hashed
    users.add(nuevo_trabajador)
    
    
    print("\n¡¡Registro Existoso. Ahora puede inciar Sesión.")
    input("Presiona ENTER para continuar...")
    return nuevo_trabajador

def iniciar_sesion():
    print("""
          ====== INICIAR SESIÓN ======
          """)
    
    codigo_input = validar_input("Ingrese el código de trabajador: ", 'codigo')
    password_input = validar_input("Contraseña: ", permitir_char_password=True)
    
    usuarios_cargados = users.get_all_user_admin()
    
    for user_data in usuarios_cargados:
        if user_data.codigo == codigo_input:
            if user_data.codigo and bcrypt.checkpw(password_input.encode('utf-8'), user_data.password_hashed.encode('utf-8')):
                print(f"¡¡Bienvenido {user_data.nombre.title()}!!")
                input("Presiona ENTER para continuar...")
                return user_data
            
            else:
                print("\n❌ Codigo o Contraseña incorrectos. Intente Nuevamente.")
                input("Presione Enter para continuar...")
                return None
    
    print("\n❌ Codigo o Contraseña Incorrectos. Intente nuevamente.")
    input("Presione ENTER para continuar...")
    return None
    
def ver_clientes():
    cls()
    print("---- LISTA DE CLIENTES ---- ")
    cliente_cargados = clientes.get_all_clientes()
    if not cliente_cargados:
        print("No hay clientes Registrados.")
    
    else:
        for c in cliente_cargados:
            print(f"|  Nombre: {c.nombre.title()}  |  Cédula: {c.cedula}  |  Teléfono: {c.telefono}  |")
    input("Presione ENTER para continuar...")

def agregar_clientes():
    cls()
    print("---- AGREGAR CLIENTE ----")
    nombre = validar_input("Nombre del Cliente: ", 'str').strip().title()
    cedula = validar_input("Cédula del Cliente: ", 'cedula')
    telefono = validar_input("Teléfono del Cliente: ", 'tel')
    password = validar_input("Contraseña del Cliente: ", permitir_char_password=True)
    
    clientes_actuales = clientes.get_all_clientes()
    for c in clientes_actuales:
        if c.cedula == cedula:
            print(f"❌ ERROR: Ya existe un cliente con la cédula '{cedula}'.")
            input("Presione ENTER para continuar...")
            return
        
    
    passsword_hasheada = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    
    nuevo_cliente = models.Cliente(nombre, cedula, telefono, passsword_hasheada)
    clientes.add(nuevo_cliente)
    
    print(f"✔️ Cliente '{nombre}' agregado con éxito.")
    input("Presione ENTER para continuar...")    

def editar_cliente():
    cls()
    print("---- EDITAR CLIENTE EXISTENTE ----")
    usuario_a_editar = validar_input("Ingrese la cédula del usuario que desea editar: ", 'cedula')
    
    cliente_encontrado = None
    for c in clientes.get_all_clientes():
        if c.cedula == usuario_a_editar:
            cliente_encontrado = c
            break
        
    if not cliente_encontrado:
        print(f"❌ No se encontró un cliente con la cédula '{usuario_a_editar}'")
        input("Presiona ENTER para continuar...")
        return
    
    print(f"\n--- Cliente actual: {cliente_encontrado.nombre} (Cédula: {cliente_encontrado.cedula}) ---")
    print(f"1. Nombre actual: {cliente_encontrado.nombre}")
    print(f"2. Teléfono actual: {cliente_encontrado.telefono}")
    print("--------------------------------------------------")
    
    print("\nDeje en blanco si no deseas cambiar el valor.")
    print("Los datos en paréntesis son los actuales.")
    
    cambios_realizados = False
    
    nuevo_nombre = input(f"Nuevo Nombre ({cliente_encontrado.nombre})").strip().title()
    if nuevo_nombre:
        if not nuevo_nombre.replace(" ", "").isalpha():
            print("❌ ERROR. Ingrese un dato válido (solo letras). No se actualizó el nombre.")
        else:
            cliente_encontrado.nombre = nuevo_nombre
            cambios_realizados = True
    
    nuevo_telefono = input(f"Nuevo Teléfono ({cliente_encontrado.telefono}): ")
    if nuevo_telefono:
        if not nuevo_telefono.isdigit() and len(nuevo_telefono) == 8 and nuevo_telefono.startswith(('8','7', '5', '2')):
            print("🟡 El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2, 5, 7 u 8. No se actualizó el teléfono.")
        else:
            cliente_encontrado.telefono = nuevo_telefono
            cambios_realizados = True
    
    nuevo_password = input(f"Nueva Contraseña: ")
    if nuevo_password:
        nuevo_password_hasheada = bcrypt.hashpw(nuevo_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cliente_encontrado.password_hashed = nuevo_password_hasheada
        print("✔️ Contraseña del cliente actualizada.")
        cambios_realizados = True

    if cambios_realizados:
        clientes.update_clientes()
        print(f"✔️ Cliente con cédula '{usuario_a_editar}' actualizado con éxito y guardado.")
    
    else:
        print("No se realizaron cambios.")
    
    input("Presione ENTER para continuar...")

def eliminar_cliente():
    cls()
    print("---- ELIMINAR CLIENTE ----")
    usuario_a_eliminar = validar_input("Ingrese la cédula del cliente que desea eliminar: ", 'cedula')
    
    if clientes.delete_cliente(usuario_a_eliminar):
        print(f"✔️ Cliente con cédula '{usuario_a_eliminar}' eliminado con éxito.")
    
    else:
        print(f"❌ ERROR: Cliente con cédula '{usuario_a_eliminar}' no encontrado.")
    input("Presione ENTER para continuar...")

def buscar_cliente():
    cls()
    print("---- BUSCAR CLIENTE ----")
    usuario_a_buscar = input("Ingrese Cédula o parte del Nombre del Cliente a buscar: ").strip()
    clientes_encontrados = clientes.find_cliente(usuario_a_buscar)
    
    if clientes_encontrados:
        print("---- CLIENTES ENCONTRADOS ----")
        for cliente in clientes_encontrados:
            print(f"|  Nombre: {cliente.nombre}  |  Cédula: {cliente.cedula}  |  Teléfono: {cliente.telefono}  |")
    
    else:
        print(f"❌ No se encontraron clientes que coincidan con '{usuario_a_buscar}'.")
    
    input("Presione ENTER para continuar...")

def ver_productos():
    cls()
    print("---- TODOS LOS PRODCUTOS ----")
    productos.show()
    input("Presiona ENTER para continuar...")

def agregar_producto():
    cls()
    print("---- AGREGAR PRODCUTO ---- ")
    nombre_producto = validar_input("Nombre del Producto: ", 'str').strip.title()
    
    for p in productos.get_all_products():
        if p.producto.lower() == nombre_producto.lower():
            print(f"❌ ERROR: Ya existe un producto con el nombre '{nombre_producto}'.")
            input("Presione ENTER para continuar...")
            return
    while True:
        try:
            precio_str = input("Precio del prodcuto: ").strip()
            precio = float(precio_str)
        
            if precio <= 0:
                print("❌ ERROR: El precio debe ser un número positivo.")
                continue
            break
        
        except ValueError:
            print("❌ ERROR: Ingrese un precio numérico válido.")
    while True:
        try:
            stock_str = input("Stock del producto: ").strip()
            stock = int(float(stock_str))
        
            if stock < 0:
                print("❌ ERROR: El stock no puede ser negativo.")
                continue
            break
        except ValueError:
            print("❌ ERROR: Ingrese un número entero para el stock.")
        
    nuevo_producto = models.Product(nombre_producto, precio, stock)
    productos.add(nuevo_producto)
    print(f"✔️ Producto '{nombre_producto}' agregado con éxito.")
    input("Presione ENTER para continuar...")

def editar_producto():
    cls()
    print("---- EDITAR PRODCUTO ----")
    producto_a_editar = validar_input("Ingrese el nombre del prodcuto a editar: ", 'str')
    productos_encontrados = productos.find_product(producto_a_editar)
    
    if not productos_encontrados:
        print(f"❌ No se encontró ningún producto que coincida con '{producto_a_editar}'")
        input("Presione Enter para continuar...")
        return
    
    if len(productos_encontrados) > 1:
        print("\nSe encontraron múltiples productos con nombres similares:")
        for i, p in enumerate(productos_encontrados):
            print(f"[{i+1}] {p}")
        while True:
            try:
                seleccion = int(input("Seleccione el número del producto a editar: "))
                if 1 <= seleccion <= len(productos_encontrados):
                    productos_encontrados = productos_encontrados[seleccion - 1]
                    break
                else:
                    print("Opción inválida. Intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingrese un número.")
    else:
        productos_encontrados = productos_encontrados[0]

    print(f"\n--- Prodcuto Actual: {productos_encontrados.producto}---")
    print(f"Precio Actual: {productos_encontrados.precio}")
    print(f"Stock Actual: {productos_encontrados.stock}")
    print("-----------------------------------------------------------")
    
    print("\nDeje en blanco si no desea cambiar el valor.")
    
    cambios_realizados = False
    
    nuevo_precio_str = input("Nuevo Precio: ").strip()
    if nuevo_precio_str:
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio <= 0:
                print("❌ ERROR: El precio debe ser un número positivo. No se actualizó el precio.")
            else:
                productos_encontrados.precio = nuevo_precio
                cambios_realizados = True
        except ValueError:
            print("❌ ERROR: Ingrese un precio numérico válido. No se actualizó el precio.")
    
    nuevo_stock_str = input("Nuevo Stock: ").strip()
    if nuevo_stock_str:
        try:
            nuevo_stock = int(float(nuevo_stock_str))
            if nuevo_stock < 0:
                print("❌ ERROR: El stock no puede ser negativo. No se actualizó el stock.")
            else:
                productos_encontrados.stock = nuevo_stock
                cambios_realizados = True
        except ValueError:
            print("❌ ERROR: Ingrese un número entero para el stock. No se actualizó el stock.")
    
    if cambios_realizados:
        productos.update_products()
        print(f"✔️ Producto '{productos_encontrados.producto}' actualizado con éxito y guardado.")
    else:
        print("No se realizaron cambios.")
    
    input("Presione ENTER para continuar...")

def eliminar_producto():
    cls()
    print("---- ELIMINAR PRODUCTO ----")
    nombre_producto_a_eliminar = validar_input("Ingresa el nombre del prodcuto que desea eliminar: ", 'str')
    
    if productos.delete_products(nombre_producto_a_eliminar):
        print(f"✔️ Producto '{nombre_producto_a_eliminar}' eliminado con éxito.")
    else:
        print(f"❌ ERROR: Producto '{nombre_producto_a_eliminar}' no encontrado.")
    input("Presione enter para continuar...")

def buscar_producto():
    cls()
    print("---- BUSCAR  PRODCUTO ----")
    producto_a_buscar = validar_input("Ingrese parte o el nombre completo del producto: ", 'str')
    producto_encontrado = productos.find_product(producto_a_buscar)
    
    if producto_encontrado:
        print("--- PRODUCTOS ENCONTRADOS ---")
        for p in producto_encontrado:
            print(p)
    else:
         print(f"❌ No se encontraron productos que coincidan con '{producto_encontrado}'.")    
    input("Presione ENTER para continuar...")
    
def validar_input(mensaje, tipo='str', permitir_char_password=False):
    while True:
        entrada = input(mensaje).lower().strip()
         
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
            
            name = sum(1 for char in entrada if char.isalpha())
            codigo_unico = sum(1 for char in entrada if char.isdigit())
            
            if name != 8 or codigo_unico != 2 or (name + codigo_unico) != len(entrada):
                print("El formato del código de trabajador es incorrecto (debe tener 8 letras seguidas de 2 números).")
                continue
        
        elif tipo == 'tel':
            if not entrada.isdigit() or len(entrada) != 8 or not entrada.startswith(("8", "7", "5", "2")):
                print("🟡 El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                continue
            
        elif tipo == 'cedula':
            if not len(entrada) == 14:
                print("❌ ERROR. La cédula debe tener 14 caracteres (13 números y 1 letra al final).")
                continue
            
            numeros = entrada[:-1]
            letras = entrada[-1]
            
            return numeros + letras.upper()
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
                        while True:
                            cls()
                            menu_inventario()
                            opc_inventario = obtener_opcion_submenu(tipo_menu='menu_inventario')
                            
                            if opc_inventario == '1':
                                ver_productos()
                            elif opc_inventario == '2':
                                agregar_producto()
                            elif opc_inventario == '3':
                                editar_producto()
                            elif opc_inventario == '4':
                                eliminar_producto()
                            elif opc_inventario == '5':
                                buscar_producto()
                            elif opc_inventario == 'regresar':
                                break
                            elif opc_inventario == 'salir_principal':
                                salir_programa()
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
                
