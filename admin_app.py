# admin_app.py
# Este módulo contiene la lógica y los menús para el rol de Administrador en el sistema Global Tools.
# Permite gestionar el inventario de productos y la información de los clientes.

import os
import sys
import random # Importamos random para generar números aleatorios

import Dao.funciones as dao # Importa las funciones DAO para interactuar con la persistencia
import Models.clases as models # Importa las clases de modelos (Cliente, Admin, Product)
import auth # Importa el módulo de autenticación para administradores (login, hash de contraseña)

# Instancias globales de los DAOs para facilitar el acceso desde las funciones del menú.
# Se inicializan al inicio del script.
users_dao = dao.AdminDao()    # DAO para usuarios administradores
clientes_dao = dao.ClienteDao() # DAO para clientes
productos_dao = dao.ProductDao() # DAO para productos

def cls():
    """
    Limpia la consola. Detecta el sistema operativo para usar el comando adecuado.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Funciones de validación de entrada específicas para admin_app ---
def admin_validar_input(mensaje: str, tipo: str = 'str', permitir_char_password: bool = False) -> str:
    """
    Función de validación de entrada de usuario adaptada para el contexto del administrador.
    Asegura que el formato de la entrada sea correcto según el tipo especificado.

    Args:
        mensaje (str): El mensaje (prompt) a mostrar al usuario.
        tipo (str): El tipo de validación a aplicar ('str', 'codigo', 'tel', 'cedula').
        permitir_char_password (bool): Si es True y tipo es 'str', permite cualquier carácter
                                       (usado para contraseñas).

    Returns:
        str: La entrada del usuario validada y formateada (ej. capitalizada para nombres).
    """
    while True:
        entrada = input(mensaje).strip() # Lee la entrada y elimina espacios al inicio/final
           
        if not entrada:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
            continue
        
        if tipo == 'str':
            if not permitir_char_password:
                # Permite espacios y letras, pero no otros caracteres si no es password
                if not entrada.replace(" ", "").isalpha():
                    print("❌ ERROR: Ingrese un dato válido (solo letras).")
                    continue
            return entrada.title() # Retorna la cadena con la primera letra de cada palabra en mayúscula
        
        elif tipo == 'codigo':
            # Este tipo de validación ya no se usará directamente para la generación,
            # pero se mantiene por si hay otras partes del código que lo necesiten.
            # El formato ahora se generará automáticamente.
            if not entrada.isalnum():
                print("🟡 ERROR: El código de trabajador no es válido (ej. atorresp07). Solo debe contener letras y números.")
                continue
            
            letras = ''.join(filter(str.isalpha, entrada))
            numeros = ''.join(filter(str.isdigit, entrada))

            if len(letras) != 8 or len(numeros) != 2 or (len(letras) + len(numeros)) != len(entrada):
                print("❌ ERROR: El formato del código de trabajador es incorrecto (debe tener 8 letras seguidas de 2 números, ej: atorresp07).")
                continue
            return entrada 
        
        elif tipo == 'tel':
            # Formato esperado para teléfono: 8 dígitos numéricos, iniciando con 2, 5, 7 o 8
            if not entrada.isdigit() or len(entrada) != 8 or not entrada.startswith(("8", "7", "5", "2")):
                print("🟡 ERROR: El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                continue
            return entrada 
        
        elif tipo == 'cedula':
            # Formato esperado para cédula: 13 números seguidos de 1 letra (ej: 0012345678901A)
            if not len(entrada) == 14:
                print("❌ ERROR: La cédula debe tener exactamente 14 caracteres (13 números y 1 letra al final).")
                continue
            
            numeros_parte = entrada[:-1] # Los primeros 13 caracteres (números)
            letra_parte = entrada[-1]    # El último caracter (letra)
            
            if not numeros_parte.isdigit() or not letra_parte.isalpha():
                print("❌ ERROR: La cédula debe tener 13 números seguidos de 1 letra (ej: 0012345678901A).")
                continue
            
            return numeros_parte + letra_parte.upper() # Asegura que la letra final esté en mayúscula
        
        return entrada # Para el caso de permitir_char_password, retorna la entrada tal cual

# --- Funciones para mostrar Menús ---

def display_main_menu():
    """
    Muestra el menú principal de opciones para el administrador.
    """
    print("""
          ==================================================
          --------- ¡¡Bienvenido!! ---------
          --------------------------------------------------
          ----------- ¿Qué desea realizar hoy? ------------
          
                    [1] Control de Inventario
                    [2] Control de Clientes
                    [3] Salir de la sesión
                    [4] Salir del programa
          ==================================================
          """)

def display_inventory_menu():
    """
    Muestra el submenú de control de inventario.
    """
    print("""
          ------ CONTROL DE INVENTARIO ------
          
            [1] Ver Todos los Productos
            [2] Agregar Nuevo Producto
            [3] Editar Producto Existente
            [4] Eliminar Producto
            [5] Buscar Producto por Nombre
            [6] Regresar al menú principal
            [7] Salir del programa
          
          -----------------------------------
          """)

def display_clients_menu():
    """
    Muestra el submenú de gestión de clientes.
    """
    print("""
        ----------- GESTIÓN DE CLIENTES -----------
          
            [1] Ver Todos los Clientes Registrados
            [2] Editar Información de Cliente
            [3] Eliminar Cliente
            [4] Agregar Cliente Manualmente
            [5] Buscar Cliente por Cédula/Nombre
            [6] Regresar al menú principal
            [7] Salir del programa
        
        -------------------------------------------
          """)

# --- Funciones de Operación de Datos (Integradas con DAOs) ---

def generar_codigo_trabajador(nombre_completo: str) -> str:
    """
    Genera un código de trabajador único basado en la inicial de los dos nombres
    y las iniciales de los dos apellidos, más dos números aleatorios.
    Formato: I_N1 + I_N2 + I_A1 + I_A2 + 2NumerosRandom.
    Si alguna parte (ej. segundo nombre) no existe, se usa 'x' como placeholder.
    Asegura que el código generado sea único en el sistema de administradores.
    
    Args:
        nombre_completo (str): El nombre completo del trabajador (ej. "Juan Jose Perez Lopez").
        
    Returns:
        str: El código de trabajador único generado.
    """
    partes = nombre_completo.split() # Divide el nombre completo en una lista de palabras
    
    iniciales = []
    
    # Inicial del Primer Nombre
    iniciales.append(partes[0][0].lower() if len(partes) > 0 else 'x')

    # Inicial del Segundo Nombre
    # Se considera la segunda palabra como segundo nombre si no es una preposición común
    # y hay suficientes partes en el nombre completo.
    if len(partes) > 1 and partes[1].lower() not in ['de', 'del', 'la', 'las', 'los', 'y']:
        iniciales.append(partes[1][0].lower())
    else:
        iniciales.append('x') # Placeholder si no hay segundo nombre o es una preposición

    # Inicial del Primer Apellido
    # Se asume que el primer apellido es la penúltima palabra si hay al menos dos palabras.
    if len(partes) >= 2:
        # Se busca el primer apellido. Si el nombre tiene más de 2 palabras (ej: Juan de la Cruz Lopez),
        # se asume que el apellido es la penúltima palabra.
        if len(partes) > 2 and partes[-2].lower() in ['de', 'del', 'la', 'las', 'los', 'y']:
            # Si la penúltima palabra es una preposición, se busca el antepenúltimo
            if len(partes) > 3:
                iniciales.append(partes[-3][0].lower())
            else:
                iniciales.append('x')
        else:
            iniciales.append(partes[-2][0].lower())
    else:
        iniciales.append('x') # Placeholder si no hay suficientes partes para un apellido

    # Inicial del Segundo Apellido
    # Se asume que el segundo apellido es la última palabra si hay al menos tres palabras.
    if len(partes) >= 3:
        iniciales.append(partes[-1][0].lower())
    else:
        iniciales.append('x') # Placeholder si no hay suficientes partes para un segundo apellido

    # Une las iniciales para formar la base del código. Se toman las primeras 4 iniciales.
    codigo_base = "".join(iniciales[:4])

    # Asegurar unicidad añadiendo dos números aleatorios
    while True:
        numeros_random = str(random.randint(0, 99)).zfill(2) # Genera un número aleatorio de 00 a 99
        codigo_generado = f"{codigo_base}{numeros_random}" # Concatena las iniciales con los números
        
        # Verifica si el código generado ya existe en la lista de administradores
        if not any(admin.codigo == codigo_generado for admin in users_dao.get_all_admin_users()):
            return codigo_generado # Si es único, lo retorna
        # Si no es único, el bucle continúa para generar otro código con nuevos números aleatorios

def register_admin_user_via_menu():
    """
    Permite al administrador registrar un nuevo usuario administrador en el sistema.
    Ahora el código de trabajador se genera automáticamente basado en el nombre y apellidos.
    """
    cls()
    print("""
          ------ REGISTRO DE NUEVO TRABAJADOR ------
          """)
    
    # Se pide el nombre completo y el programa genera el código
    nombre_completo = admin_validar_input("Nombre y Apellidos: ", 'str')
    
    # Generar automáticamente el código de trabajador
    codigo_generado = generar_codigo_trabajador(nombre_completo)
    print(f"✔️ Código de trabajador generado: {codigo_generado}")

    telefono = admin_validar_input("Ingrese su número telefónico (8 dígitos, inicia con 2,5,7,8): ", 'tel')
    cedula = admin_validar_input("Digite su número de Cédula (13 números + 1 letra): ", 'cedula')
    
    password = admin_validar_input("Cree su contraseña: ", permitir_char_password=True)
    
    # Se crea el objeto Admin con la contraseña hasheada usando la función de auth.py
    nuevo_trabajador = models.Admin(
        nombre=nombre_completo,
        codigo=codigo_generado, # Asignar el código generado automáticamente
        cedula=cedula,
        telefono=telefono,
        password_hashed=auth._hash_password(password)
    )

    # El método add del AdminDao se encarga de las validaciones de duplicados (cedula) y la persistencia
    # El código ya está validado como único por generar_codigo_trabajador
    if users_dao.add(nuevo_trabajador):
        print(f"\n✅ ¡¡Registro Exitoso. Su nombre de usuario (código) es: {codigo_generado}!!")
    else:
        print("\n❌ Error al registrar trabajador. Verifique los datos o si ya existe un usuario con esa cédula.")
    
    input("Presiona ENTER para continuar...")

def view_clients():
    """
    Muestra una lista formateada de todos los clientes registrados en el sistema.
    Utiliza el método `show()` de `ClienteDao`.
    """
    cls()
    clientes_dao.show() # Delega la visualización al DAO
    input("Presione ENTER para continuar...")

def add_client_manual():
    """
    Permite al administrador agregar un nuevo cliente al sistema manualmente.
    Incluye validaciones para la cédula y otros campos.
    """
    cls()
    print("---- AGREGAR CLIENTE MANUALMENTE ----")
    
    while True:
        cedula = admin_validar_input("Cédula del cliente (13 números + 1 letra): ", 'cedula')
        # Verificar si la cédula ya existe para evitar duplicados
        if not any(c.cedula == cedula for c in clientes_dao.get_all_clientes()):
            break
        else:
            print(f"❌ ERROR: Ya existe un cliente con la cédula '{cedula}'.")
            input("Presione ENTER para continuar...")
            return

    nombre = admin_validar_input("Nombre del Cliente: ", 'str')
    telefono = admin_validar_input("Teléfono del Cliente (8 dígitos, inicia con 2,5,7,8): ", 'tel')
    
    nuevo_cliente = models.Cliente(nombre, cedula, telefono)
    clientes_dao.add(nuevo_cliente) # El DAO se encarga de agregar y guardar
    
    print(f"✅ Cliente '{nombre}' agregado con éxito.")
    input("Presione ENTER para continuar...")

def edit_client():
    """
    Permite al administrador editar la información de un cliente existente.
    El cliente se identifica por su cédula.
    """
    cls()
    print("---- EDITAR CLIENTE EXISTENTE ----")
    cedula_a_editar = admin_validar_input("Ingrese la cédula del cliente que desea editar: ", 'cedula')
    
    cliente_encontrado = None
    # Busca el cliente por cédula exacta
    for c in clientes_dao.get_all_clientes():
        if c.cedula == cedula_a_editar:
            cliente_encontrado = c
            break
            
    if not cliente_encontrado:
        print(f"❌ No se encontró un cliente con la cédula '{cedula_a_editar}'")
        input("Presiona ENTER para continuar...")
        return
    
    print(f"\n--- Cliente actual: {cliente_encontrado.nombre} (Cédula: {cliente_encontrado.cedula}) ---")
    print(f"1. Nombre actual: {cliente_encontrado.nombre}")
    print(f"2. Teléfono actual: {cliente_encontrado.telefono}")
    print("--------------------------------------------------")
    
    print("\nDeje en blanco si no deseas cambiar el valor.")
    print("Los datos en paréntesis son los actuales.")
    
    cambios_realizados = False
    
    # Edición del nombre
    nuevo_nombre = input(f"Nuevo Nombre ({cliente_encontrado.nombre}): ").strip()
    if nuevo_nombre:
        if not nuevo_nombre.replace(" ", "").isalpha():
            print("❌ ERROR: Ingrese un dato válido (solo letras). No se actualizó el nombre.")
        else:
            cliente_encontrado.nombre = nuevo_nombre.title() # Asegura formato de título
            cambios_realizados = True
    
    # Edición del teléfono
    nuevo_telefono = input(f"Nuevo Teléfono ({cliente_encontrado.telefono}): ").strip()
    if nuevo_telefono:
        if not (nuevo_telefono.isdigit() and len(nuevo_telefono) == 8 and nuevo_telefono.startswith(('8','7', '5', '2'))):
            print("🟡 ERROR: El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2, 5, 7 u 8. No se actualizó el teléfono.")
        else:
            cliente_encontrado.telefono = nuevo_telefono
            cambios_realizados = True
    
    # Edición de la contraseña (si el cliente tiene una y se permite)
    if cliente_encontrado.password_hashed is not None:
        nuevo_password = input(f"Nueva Contraseña (Enter para mantener la actual): ").strip()
        if nuevo_password:
            # Hashear la nueva contraseña antes de asignarla
            cliente_encontrado.password_hashed = auth._hash_password(nuevo_password)
            print("✔️ Contraseña del cliente actualizada.")
            cambios_realizados = True

    if cambios_realizados:
        clientes_dao.update_clientes_list() # Persiste los cambios en el archivo
        print(f"✅ Cliente con cédula '{cedula_a_editar}' actualizado con éxito y guardado.")
    else:
        print("No se realizaron cambios.")
    
    input("Presione ENTER para continuar...")

def delete_client():
    """
    Permite al administrador eliminar un cliente existente por su número de cédula.
    """
    cls()
    print("---- ELIMINAR CLIENTE ----")
    cedula_a_eliminar = admin_validar_input("Ingrese la cédula del cliente que desea eliminar: ", 'cedula')
    
    # El método delete_cliente del DAO ya imprime mensajes de éxito/error.
    if clientes_dao.delete_cliente(cedula_a_eliminar):
        print(f"✅ Cliente con cédula '{cedula_a_eliminar}' eliminado con éxito.")
    else:
        print(f"❌ ERROR: Cliente con cédula '{cedula_a_eliminar}' no encontrado.")
    input("Presione ENTER para continuar...")

def search_client():
    """
    Permite al administrador buscar clientes por cédula o parte del nombre.
    Muestra los clientes encontrados en un formato de tabla.
    """
    cls()
    print("---- BUSCAR CLIENTE ----")
    query = input("Ingrese Cédula o parte del Nombre del Cliente a buscar: ").strip()
    found_clients = clientes_dao.find_cliente(query)
    
    if found_clients:
        print("\n---- CLIENTES ENCONTRADOS ----")
        # Imprime un encabezado para la tabla de resultados
        print(f"{'Cédula':<15} {'Nombre':<25} {'Teléfono':<15}")
        print("-" * 55)
        for cliente in found_clients:
            print(f"{cliente.cedula:<15} {cliente.nombre:<25} {cliente.telefono:<15}")
        print("-" * 55)
    else:
        print(f"❌ No se encontraron clientes que coincidan con '{query}'.")
    
    input("Presione ENTER para continuar...")

def view_products():
    """
    Muestra una lista formateada de todos los productos en el inventario.
    Utiliza el método `show()` de `ProductDao`.
    """
    cls()
    productos_dao.show() # Delega la visualización al DAO
    input("Presiona ENTER para continuar...")

def add_product():
    """
    Permite al administrador agregar un nuevo producto al inventario.
    Incluye validaciones para el nombre, precio y stock.
    """
    cls()
    print("---- AGREGAR PRODUCTO ---- ")
    
    while True:
        nombre_producto = admin_validar_input("Nombre del Producto: ", 'str')
        # Verificar si el producto ya existe (insensible a mayúsculas/minúsculas)
        if not any(p.producto.lower() == nombre_producto.lower() for p in productos_dao.get_all_products()):
            break
        else:
            print(f"❌ ERROR: Ya existe un producto con el nombre '{nombre_producto}'.")
            input("Presione ENTER para continuar...")
            return
    
    while True:
        try:
            precio = float(input("Precio del producto: ").strip())
            if precio <= 0:
                print("❌ ERROR: El precio debe ser un número positivo.")
                continue
            break
        except ValueError:
            print("❌ ERROR: Ingrese un precio numérico válido.")
    
    while True:
        try:
            stock = int(float(input("Stock del producto: ").strip())) # Convertir a float primero por seguridad
            if stock < 0:
                print("❌ ERROR: El stock no puede ser negativo.")
                continue
            break
        except ValueError:
            print("❌ ERROR: Ingrese un número entero para el stock.")
        
    nuevo_producto = models.Product(nombre_producto, precio, stock)
    productos_dao.add(nuevo_producto) # El DAO se encarga de agregar y guardar
    print(f"✅ Producto '{nombre_producto}' agregado con éxito.") # Confirmación adicional
    input("Presione ENTER para continuar...")

def edit_product():
    """
    Permite al administrador editar la información de un producto existente (precio y stock).
    El producto se identifica por su nombre.
    """
    cls()
    print("---- EDITAR PRODUCTO ----")
    producto_a_editar_nombre = admin_validar_input("Ingrese el nombre del producto a editar: ", 'str').lower()
    
    productos_cargados = productos_dao.get_all_products()
    # Filtra productos que contengan la cadena de búsqueda en su nombre
    productos_encontrados = [p for p in productos_cargados if producto_a_editar_nombre in p.producto.lower()]

    if not productos_encontrados:
        print(f"❌ No se encontró ningún producto que coincida con '{producto_a_editar_nombre}'")
        input("Presione Enter para continuar...")
        return
    
    producto_seleccionado = None
    if len(productos_encontrados) > 1:
        # Si se encuentran múltiples productos, pide al usuario que seleccione uno
        print("\nSe encontraron múltiples productos con nombres similares:")
        for i, p in enumerate(productos_encontrados):
            print(f"[{i+1}] {p}")
        while True:
            try:
                seleccion = int(input("Seleccione el número del producto a editar: "))
                if 1 <= seleccion <= len(productos_encontrados):
                    producto_seleccionado = productos_encontrados[seleccion - 1]
                    break
                else:
                    print("🛑 Opción inválida. Intente de nuevo.")
            except ValueError:
                print("❌ Entrada inválida. Ingrese un número.")
    else:
        producto_seleccionado = productos_encontrados[0] # Si solo hay uno, lo selecciona automáticamente

    print(f"\n--- Producto Actual: {producto_seleccionado.producto} ---")
    print(f"Precio Actual: {producto_seleccionado.precio:.2f}")
    print(f"Stock Actual: {producto_seleccionado.stock}")
    print("-----------------------------------------------------------")
    
    print("\nDeje en blanco si no desea cambiar el valor.")
    
    cambios_realizados = False
    
    # Edición del precio
    nuevo_precio_str = input(f"Nuevo Precio ({producto_seleccionado.precio:.2f}): ").strip()
    if nuevo_precio_str:
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio <= 0:
                print("❌ ERROR: El precio debe ser un número positivo. No se actualizó el precio.")
            else:
                producto_seleccionado.precio = nuevo_precio
                cambios_realizados = True
        except ValueError:
            print("❌ ERROR: Ingrese un precio numérico válido. No se actualizó el precio.")
    
    nuevo_stock_str = input(f"Nuevo Stock ({producto_seleccionado.stock}): ").strip()
    if nuevo_stock_str:
        try:
            nuevo_stock = int(float(nuevo_stock_str))
            if nuevo_stock < 0:
                print("❌ ERROR: El stock no puede ser negativo.")
            else:
                producto_seleccionado.stock = nuevo_stock
                cambios_realizados = True
        except ValueError:
            print("❌ ERROR: Ingrese un número entero para el stock.")
    
    if cambios_realizados:
        productos_dao.update_products_list() # Persiste los cambios en el archivo
        print(f"✅ Producto '{producto_seleccionado.producto}' actualizado con éxito y guardado.")
    else:
        print("No se realizaron cambios.")
    
    input("Presione ENTER para continuar...")

def delete_product():
    """
    Permite al administrador eliminar un producto existente por su nombre.
    """
    cls()
    print("---- ELIMINAR PRODUCTO ----")
    nombre_producto_a_eliminar = admin_validar_input("Ingresa el nombre del producto que desea eliminar: ", 'str')
    
    # El método delete_product del DAO ya imprime mensajes de éxito/error.
    if productos_dao.delete_product(nombre_producto_a_eliminar):
        print(f"✅ Producto '{nombre_producto_a_eliminar}' eliminado con éxito.")
    else:
        print(f"❌ ERROR: Producto '{nombre_producto_a_eliminar}' no encontrado.")
    input("Presione enter para continuar...")

def search_product():
    """
    Permite al administrador buscar productos por una parte de su nombre.
    Muestra los productos encontrados en un formato de tabla.
    """
    cls()
    print("---- BUSCAR PRODUCTO ----")
    query = admin_validar_input("Ingrese parte o el nombre completo del producto: ", 'str')
    found_products = productos_dao.find_product(query)
    
    if found_products:
        print("--- PRODUCTOS ENCONTRADOS ---")
        # Imprime un encabezado para la tabla de resultados
        print(f"{'Producto':<25} {'Precio':<10} {'Stock':<8}")
        print("-" * 45)
        for p in found_products:
            print(f"{p.producto:<25} {p.precio:<10.2f} {p.stock:<8}")
        print("-" * 45)
    else:
        print(f"❌ No se encontraron productos que coincidan con '{query}'.")    
    input("Presione ENTER para continuar...")

# --- Lógica principal del bucle de la aplicación del administrador ---

def run_admin_app():
    """
    Ejecuta el ciclo principal de la aplicación para el rol de administrador.
    Este bucle se ejecuta después de que un administrador ha iniciado sesión exitosamente.
    """
    current_admin_user = None # Esta variable podría ser usada si se necesitara el objeto Admin logeado

    # Bucle principal del menú del administrador
    while True:
        cls() # Limpia la pantalla al inicio de cada iteración del menú
        print("         ------ [ADMIN USER] ------")
        display_main_menu() # Muestra el menú principal del administrador
        
        opcion_elegida = input("Seleccione una opción (1-4): ").strip() # Captura la opción del usuario
        
        if opcion_elegida == '1': # Opción: Control de Inventario
            while True:
                cls() # Limpia la pantalla antes de mostrar el submenú de inventario
                display_inventory_menu() # Muestra el submenú de inventario
                opc_inventario = input("Seleccione una opción (1-7): ").strip()
                
                if opc_inventario == '1':
                    view_products() # Ver productos
                    cls() # Limpia después de la acción
                elif opc_inventario == '2':
                    add_product() # Agregar producto
                    cls() # Limpia después de la acción
                elif opc_inventario == '3':
                    edit_product() # Editar producto
                    cls() # Limpia después de la acción
                elif opc_inventario == '4':
                    delete_product() # Eliminar producto
                    cls() # Limpia después de la acción
                elif opc_inventario == '5':
                    search_product() # Buscar producto
                    cls() # Limpia después de la acción
                elif opc_inventario == '6':
                    print("⬅️  Regresando al menú principal de Admin...")
                    break # Sale del bucle del submenú de inventario
                elif opc_inventario == '7':
                    print("👋  ¡Gracias por usar el programa! Saliendo...")
                    sys.exit() # Sale del programa completamente
                else:
                    print("🛑 Ingrese una opción válida (1-7).")
                    input("Presione ENTER para continuar...")
                    cls() # Limpia después de un error

        elif opcion_elegida == '2': # Opción: Control de Clientes
            while True:
                cls() # Limpia la pantalla antes de mostrar el submenú de clientes
                display_clients_menu() # Muestra el submenú de clientes
                opc_clientes = input("Seleccione una opción (1-7): ").strip()
                
                if opc_clientes == '1':
                    view_clients() # Ver clientes
                    cls() # Limpia después de la acción
                elif opc_clientes == '2':
                    edit_client() # Editar cliente
                    cls() # Limpia después de la acción
                elif opc_clientes == '3':
                    delete_client() # Eliminar cliente
                    cls() # Limpia después de la acción
                elif opc_clientes == '4':
                    add_client_manual() # Agregar cliente manualmente
                    cls() # Limpia después de la acción
                elif opc_clientes == '5':
                    search_client() # Buscar cliente
                    cls() # Limpia después de la acción
                elif opc_clientes == '6':
                    print("⬅️  Regresando al menú principal de Admin...")
                    break # Sale del bucle del submenú de clientes
                elif opc_clientes == '7':
                    print("👋  ¡Gracias por usar el programa! Saliendo...")
                    sys.exit() # Sale del programa completamente
                else:
                    print("🛑 Ingrese una opción válida (1-7).")
                    input("Presione ENTER para continuar...")
                    cls() # Limpia después de un error
        
        elif opcion_elegida == '3': # Opción: Salir de la sesión
            print("\n🚪  Cerrando sesión de administrador...")
            break # Sale de este bucle (run_admin_app), lo que lleva de vuelta al menú inicial de login en main.py

        elif opcion_elegida == '4': # Opción: Salir del programa completamente
            print("👋  ¡Gracias por usar el programa! Saliendo...")
            sys.exit() # Sale del programa

        else:
            print("🛑 Ingrese una opción válida (1-4).")
            input("Presione ENTER para continuar...")
            cls() # Limpia después de un error
