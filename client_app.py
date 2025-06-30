# client_app.py
# Este módulo contiene la lógica y los menús para el rol de Cliente en el sistema Global Tools.
# Permite a los usuarios registrarse, iniciar sesión, comprar artículos y verificar su crédito.

import os
import sys
import bcrypt # Necesitamos bcrypt aquí para el hash de contraseñas de clientes
import datetime # Para manejar fechas y cálculos de vencimiento
import uuid # Para generar IDs únicos para las facturas
try:
    import pwinput # Librería de terceros para mostrar asteriscos al escribir contraseña
except ImportError:
    pwinput = None # Si pwinput no está instalado, la funcionalidad no estará disponible

import Dao.funciones as dao # Importa las funciones DAO para interactuar con la persistencia
import Models.clases as models # Importa las clases de modelos (Cliente, Admin, Product, Factura)

# Instancias globales de los DAOs para facilitar el acceso desde las funciones del menú.
clientes_dao = dao.ClienteDao()    # DAO para clientes
productos_dao = dao.ProductDao() # DAO para productos
facturas_dao = dao.FacturaDao() # Nuevo DAO para facturas

def cls():
    """
    Limpia la consola. Detecta el sistema operativo para usar el comando adecuado.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Funciones de validación de entrada específicas para client_app ---
def client_validar_input(mensaje: str, tipo: str = 'str') -> str:
    """
    Función de validación de entrada de usuario adaptada para el contexto del cliente.
    Asegura que el formato de la entrada sea correcto según el tipo especificado.

    Args:
        mensaje (str): El mensaje (prompt) a mostrar al usuario.
        tipo (str): El tipo de validación a aplicar ('str', 'tel', 'cedula', 'int_pos', 'float_pos', 'password').

    Returns:
        str: La entrada del usuario validada y formateada (ej. capitalizada para nombres).
    """
    while True:
        entrada = ""
        if tipo == 'password':
            if pwinput:
                entrada = pwinput.pwinput(mensaje, mask="*").strip()
            else:
                entrada = input(mensaje).strip()
                print("⚠️ Advertencia: 'pwinput' no está instalado. La contraseña será visible.")
        else:
            entrada = input(mensaje).strip()

        if not entrada:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
            continue

        if tipo == 'str':
            # Solo aplica esta validación y formato si no es una contraseña
            if not entrada.replace(" ", "").isalpha():
                print("❌ ERROR. Ingrese un dato válido (solo letras).")
                continue
            return entrada.title()
        
        elif tipo == 'tel':
            # Formato esperado para teléfono: 8 dígitos numéricos, iniciando con 2, 5, 7 o 8
            if not entrada.isdigit() or len(entrada) != 8 or not entrada.startswith(("8", "7", "5", "2")):
                print("🟡 El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                continue
            return entrada
        
        elif tipo == 'cedula':
            # Formato esperado para cédula: 13 números seguidos de 1 letra (ej: 0012345678901A)
            if not len(entrada) == 14:
                print("❌ ERROR. La cédula debe tener exactamente 14 caracteres (13 números y 1 letra al final).")
                continue
            
            numeros_parte = entrada[:-1] # Los primeros 13 caracteres (números)
            letra_parte = entrada[-1]    # El último caracter (letra)
            
            if not numeros_parte.isdigit() or not letra_parte.isalpha():
                print("❌ ERROR. La cédula debe tener 13 números seguidos de 1 letra (ej: 0012345678901A).")
                continue
            
            return numeros_parte + letra_parte.upper() # Asegura que la letra final esté en mayúscula
        
        elif tipo == 'int_pos':
            try:
                valor = int(entrada)
                if valor <= 0:
                    print("❌ ERROR: Ingrese un número entero positivo.")
                    continue
                return str(valor)
            except ValueError:
                print("❌ ERROR: Ingrese un número entero válido.")
                continue
        
        elif tipo == 'float_pos':
            try:
                valor = float(entrada)
                if valor <= 0:
                    print("❌ ERROR: Ingrese un número positivo.")
                    continue
                return str(valor)
            except ValueError:
                print("❌ ERROR: Ingrese un número numérico válido.")
                continue
        
        elif tipo == 'password': # Tipo específico para contraseñas
            return entrada # Retorna la contraseña tal cual, sin modificar
        
        # Fallback en caso de que el tipo no se maneje explícitamente (no debería ocurrir si los tipos son controlados)
        return entrada


# --- Funciones para mostrar Menús ---

def display_welcome_menu_client():
    """
    Muestra el menú de bienvenida inicial para los clientes, ofreciendo opciones
    para iniciar sesión, registrarse o continuar como invitado.
    """
    print("""
          -------------------> GLOBAL TOOLS S.A <-------------------
          
          ==================== ¡Bienvenido! ====================
          
          ¿Estás registrado con nosotros?
          
            [1] SI, INICIAR SESIÓN     
            [2] NO, AÚN NO ESTOY REGISTRADO / COMPRAR COMO INVITADO
            [3] Salir del programa
          
          (Para utilizar las opciones de crédito debe tener registro)
          
          """)

def display_client_actions_menu(usuario_nombre: str):
    """
    Muestra el menú de acciones disponibles para un cliente que ha iniciado sesión.
    
    Args:
        usuario_nombre (str): El nombre del cliente logeado para personalizar el saludo.
    """
    print(f"""
     ===========================================
      ------------> [GLOBAL TOOLS S.A, 2025]
      Bienvenido {usuario_nombre}!!

      [-] ¿Qué harás el día de hoy?
      (Presiona la tecla correspondiente para elegir.)
      ------
      [A] Comprar un artículo
      [B] Ver estado de crédito
      [C] Salir de la sesión
      ===========================================
    """) 

# --- Funciones de Autenticación de Clientes ---

def register_client_session():
    """
    Permite al usuario registrar una nueva cuenta de cliente.
    Solicita los datos necesarios y hashea la contraseña antes de guardar el cliente.
    """
    cls()
    print("""
          ------> REGISTRO DE NUEVO USUARIO (CLIENTE) <------
          """)
    nombre_completo = client_validar_input("Nombres y Apellidos: ", 'str')
    telefono_num = client_validar_input("Ingrese su número telefónico (8 dígitos, inicia con 2,5,7,8): ", 'tel')
    cedula_id = client_validar_input("Digite su número de cédula (13 números + 1 letra): ", 'cedula')
    
    # Verifica si la cédula ya existe para evitar registros duplicados
    usuarios_existentes = clientes_dao.get_all_clientes() 
    for user_data in usuarios_existentes: 
        if user_data.cedula == cedula_id: 
            print("❌ ERROR: Ya existe una cuenta con esta cédula. Intente iniciar sesión.")
            input("Presione Enter para continuar...")
            return None # Retorna None para indicar que el registro falló
        
    password = client_validar_input("Cree su contraseña: ", 'password') # Se cambió a tipo 'password'
    # Hashea la contraseña usando bcrypt antes de crear el objeto Cliente
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Crea una nueva instancia del modelo Cliente
    nuevo_cliente = models.Cliente(nombre_completo, cedula_id, telefono_num, password_hashed)
    clientes_dao.add(nuevo_cliente) # Usa el DAO para agregar y persistir el nuevo cliente
    
    print("\n¡¡Registro Exitoso!! Ahora puedes iniciar sesión.")
    input("Presione enter para continuar...")
    return nuevo_cliente # Retorna el objeto Cliente registrado

def login_client_session():
    """
    Permite al usuario iniciar sesión como cliente.
    Verifica las credenciales (cédula y contraseña) contra los datos almacenados.
    Incluye un límite de 3 intentos de inicio de sesión.
    """
    cls()
    print("""
          ====== INICIAR SESIÓN (CLIENTE) ======
          """) 

    usuarios_cargados = clientes_dao.get_all_clientes() # Carga todos los clientes para verificar
    intentos_maximos = 3

    for intento in range(1, intentos_maximos + 1):
        print(f"\n--- Intento {intento}/{intentos_maximos} ---")
        cedula_input = client_validar_input("Ingrese su usuario (Cédula, 13 números + 1 letra) sin guiones y espacios: ", 'cedula')
        password_input = client_validar_input("Ingrese su Contraseña: ", 'password') # Se cambió a tipo 'password'
        
        cliente_encontrado = None
        for user_data in usuarios_cargados: 
            if user_data.cedula == cedula_input:
                cliente_encontrado = user_data
                break
        
        if cliente_encontrado:
            # Si el cliente fue encontrado, verifica su contraseña
            # Comprueba si tiene una contraseña hasheada y si coincide con la entrada
            if cliente_encontrado.password_hashed and bcrypt.checkpw(password_input.encode('utf-8'), cliente_encontrado.password_hashed.encode('utf-8')):
                print(f"¡Bienvenido {cliente_encontrado.nombre}!") 
                input("Presione Enter para continuar...")
                return cliente_encontrado # Retorna el objeto Cliente logeado
            else:
                print("❌ Cédula o contraseña incorrecta. Intente de nuevo.")
                if intento < intentos_maximos:
                    print(f"Te quedan {intentos_maximos - intento} intentos.")
        else: # Si no se encontró ningún cliente con la cédula
            print("❌ Cédula o contraseña incorrecta. Intente de nuevo.")
            if intento < intentos_maximos:
                print(f"Te quedan {intentos_maximos - intento} intentos.")
    
    print("\n🛑 Has agotado tus intentos de inicio de sesión. Regresando al menú principal.")
    input("Presiona ENTER para continuar...")
    return None # Retorna None si el usuario no existe o se agotan los intentos

# --- Funciones de Acciones de Cliente ---

def buy_item(current_client_cedula: str = "INVITADO"):
    """
    Implementa la lógica para que el cliente compre artículos.
    Permite seleccionar productos, cantidades, y elegir entre pago al contado o a crédito.
    Genera y guarda una factura por la compra.
    
    Args:
        current_client_cedula (str): La cédula del cliente logeado, o "INVITADO" si no hay login.
    """
    cls()
    print("""
          ------> COMPRAR ARTÍCULO <------
          """)
    
    productos_disponibles = productos_dao.get_all_products()
    if not productos_disponibles:
        print("[INFO] No hay productos disponibles en este momento.")
        input("Presione Enter para continuar...")
        return

    # Mostrar productos disponibles
    productos_dao.show()

    carrito = []
    subtotal = 0.0

    while True:
        producto_nombre = input("Ingrese el nombre del producto que desea comprar (o 'fin' para terminar): ").strip().title()
        if producto_nombre.lower() == 'fin':
            break

        producto_seleccionado = None
        for p in productos_disponibles:
            if p.producto.title() == producto_nombre:
                producto_seleccionado = p
                break

        if not producto_seleccionado:
            print(f"❌ Producto '{producto_nombre}' no encontrado. Intente de nuevo.")
            continue

        while True:
            try:
                cantidad_str = client_validar_input(f"Cantidad de '{producto_seleccionado.producto}' (Stock: {producto_seleccionado.stock}): ", 'int_pos')
                cantidad = int(cantidad_str)
                if cantidad > producto_seleccionado.stock:
                    print(f"❌ No hay suficiente stock. Solo quedan {producto_seleccionado.stock} unidades.")
                else:
                    break
            except ValueError:
                print("❌ Cantidad inválida. Ingrese un número entero.")

        carrito.append({
            'producto': producto_seleccionado.producto,
            'cantidad': cantidad,
            'precio_unitario': producto_seleccionado.precio
        })
        subtotal += cantidad * producto_seleccionado.precio
        producto_seleccionado.stock -= cantidad # Reduce el stock en memoria
        print(f"✔️ '{cantidad}' de '{producto_seleccionado.producto}' añadido al carrito.")
        
        # Opcional: Actualizar el archivo de productos después de cada adición al carrito
        # productos_dao.update_products_list() 
        # Es mejor actualizar al final de la compra para evitar escrituras excesivas

    if not carrito:
        print("[INFO] No se seleccionaron productos. Compra cancelada.")
        input("Presione Enter para continuar...")
        return

    print("\n--- RESUMEN DE COMPRA ---")
    for item in carrito:
        print(f"{item['producto']} (x{item['cantidad']}) - ${item['cantidad'] * item['precio_unitario']:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")

    tipo_pago = ""
    dias_credito = None
    fecha_vencimiento = None
    recargo_credito_porcentaje = 0.0
    monto_recargo_credito = 0.0
    total_final_pagar = subtotal

    while True:
        print("\nSeleccione tipo de pago:")
        print("1. Contado")
        print("2. Crédito (15 o 30 días) - Solo para clientes registrados")
        opcion_pago = input("Ingrese opción (1 o 2): ").strip()

        if opcion_pago == '1':
            tipo_pago = 'contado'
            print(f"\nTotal a pagar al contado: ${total_final_pagar:.2f}")
            break
        elif opcion_pago == '2':
            if current_client_cedula == "INVITADO":
                print("❌ No puede pagar a crédito como invitado. Por favor, regístrese o elija pago al contado.")
                continue
            
            tipo_pago = 'credito'
            recargo_credito_porcentaje = 0.10 # 10% de recargo
            monto_recargo_credito = subtotal * recargo_credito_porcentaje
            total_final_pagar = subtotal + monto_recargo_credito

            while True:
                dias_str = input("Días de crédito (15 o 30): ").strip()
                if dias_str in ['15', '30']:
                    dias_credito = int(dias_str)
                    fecha_vencimiento = datetime.datetime.now() + datetime.timedelta(days=dias_credito)
                    break
                else:
                    print("❌ Días de crédito inválidos. Elija 15 o 30.")
            
            print(f"\nSubtotal: ${subtotal:.2f}")
            print(f"Recargo por crédito ({recargo_credito_porcentaje*100:.0f}%): ${monto_recargo_credito:.2f}")
            print(f"Total a pagar a crédito: ${total_final_pagar:.2f}")
            print(f"Fecha de vencimiento: {fecha_vencimiento.strftime('%Y-%m-%d')}")
            break
        else:
            print("❌ Opción de pago inválida.")

    confirmar = input("\n¿Confirmar compra? (s/n): ").strip().lower()
    if confirmar == 's':
        # Generar ID de factura único
        id_factura = str(uuid.uuid4())[:8].upper() # Tomar los primeros 8 caracteres del UUID
        
        # Crear la instancia de Factura
        nueva_factura = models.Factura(
            id_factura=id_factura,
            cliente_cedula=current_client_cedula,
            productos_comprados=carrito,
            subtotal=subtotal,
            tipo_pago=tipo_pago,
            recargo_credito_porcentaje=recargo_credito_porcentaje,
            monto_recargo_credito=monto_recargo_credito,
            total_pagar=total_final_pagar,
            dias_credito=dias_credito,
            fecha_vencimiento=fecha_vencimiento
        )
        
        facturas_dao.add(nueva_factura) # Guardar la factura

        # Guardar los cambios de stock en los productos
        productos_dao.update_products_list()
        
        print("\n" + "="*40)
        print("          ¡COMPRA REALIZADA CON ÉXITO!")
        print("="*40)
        print(nueva_factura) # Muestra la factura generada
        print("="*40)
        input("Presione Enter para continuar...")
    else:
        print("[INFO] Compra cancelada.")
        input("Presione Enter para continuar...")

def view_credit_status(client_cedula: str):
    """
    Permite a un cliente ver el estado de sus facturas, especialmente las de crédito.
    Calcula recargos por mora si aplica.
    
    Args:
        client_cedula (str): La cédula del cliente para el cual se verán las facturas.
    """
    cls()
    print(f"""
          ------> ESTADO DE CRÉDITO Y FACTURAS PARA {client_cedula} <------
          """)
    
    facturas_cliente = facturas_dao.find_facturas_by_client_cedula(client_cedula)
    
    if not facturas_cliente:
        print("[INFO] No tienes facturas registradas.")
    else:
        print("\n--- Tus Facturas ---")
        for factura in facturas_cliente:
            print("\n" + "="*40)
            print(factura) # Muestra la factura completa
            
            if factura.tipo_pago == 'credito' and not factura.pagado:
                print("\n  --- Estado de Crédito ---")
                hoy = datetime.datetime.now()
                
                # Calcular días de atraso solo si la factura está vencida y no pagada
                if factura.fecha_vencimiento and hoy > factura.fecha_vencimiento:
                    dias_atraso = (hoy - factura.fecha_vencimiento).days
                    if dias_atraso > 0: # Solo aplica recargo si hay días de atraso reales
                        recargo_por_mora_diario = 0.02 # 2% por día
                        # El recargo se calcula sobre el monto pendiente (total_pagar - monto_abonado)
                        monto_pendiente_sin_mora = factura.total_pagar - factura.monto_abonado
                        monto_recargo_mora = monto_pendiente_sin_mora * recargo_por_mora_diario * dias_atraso
                        
                        print(f"  VENCIDA hace {dias_atraso} días.")
                        print(f"  Recargo por mora acumulado: ${monto_recargo_mora:.2f}")
                        print(f"  Monto pendiente + mora: ${monto_pendiente_sin_mora + monto_recargo_mora:.2f}")
                    else: # Aún no está vencida pero la fecha de emisión ya pasó la de vencimiento por un cálculo exacto
                          # pero aún no se cumple el día completo de atraso
                        print(f"  Crédito Activo. La fecha de vencimiento es hoy o ya pasó pero aún no hay mora.")
                        print(f"  Monto pendiente: ${factura.total_pagar - factura.monto_abonado:.2f}")
                else:
                    # Cálculo de días restantes (positivo si aún no vence, 0 si vence hoy)
                    if factura.fecha_vencimiento:
                        dias_restantes = (factura.fecha_vencimiento - hoy).days + 1 # +1 para incluir el día de vencimiento
                        if dias_restantes < 0: dias_restantes = 0 # Asegurar que no sea negativo si es muy reciente el vencimiento
                    else:
                        dias_restantes = 'N/A'

                    print(f"  Crédito Activo. Días restantes: {dias_restantes}")
                    print(f"  Monto pendiente: ${factura.total_pagar - factura.monto_abonado:.2f}")
            elif factura.pagado:
                print("  --- Estado de Pago: PAGADA ---")
            
            print("="*40)
            
    input("Presione Enter para continuar...")

# --- Lógica principal del bucle de la aplicación del cliente ---

def run_client_app():
    """
    Ejecuta el ciclo principal de la aplicación para el rol de cliente.
    Gestiona el flujo entre el menú de bienvenida, registro/login y acciones de cliente.
    """
    current_client_logged = None # Variable para almacenar el objeto Cliente logeado

    while True:
        cls() # Limpia la pantalla al inicio de cada iteración del menú
        display_welcome_menu_client() # Muestra el menú de bienvenida para clientes
        
        accion_elegida = input("Seleccione una opción (1-3): ").strip() # Captura la opción del usuario

        if accion_elegida == "1": # Opción: SI, INICIAR SESIÓN
            current_client_logged = login_client_session() # Intenta logear al cliente
            if current_client_logged: 
                # Si el login es exitoso, entra al bucle de acciones de cliente
                while True: 
                    cls() # Limpia la pantalla antes de mostrar el menú de acciones
                    display_client_actions_menu(current_client_logged.nombre) # Muestra el menú de acciones
                    opcion_accion = input("--> ").strip().lower() # Captura la opción (A, B, C)
                    
                    if opcion_accion == "a":
                        buy_item(current_client_logged.cedula) # Llama a la función de comprar con la cédula del cliente
                        cls() # Limpia después de la acción
                    elif opcion_accion == "b":
                        view_credit_status(current_client_logged.cedula) # Llama a la función de ver crédito con la cédula del cliente
                        cls() # Limpia después de la acción
                    elif opcion_accion == "c":
                        print("Ha salido de la sesión.") 
                        input("Presione ENTER para continuar...")
                        current_client_logged = None # Reinicia el cliente logeado
                        break # Sale del bucle de acciones, volviendo al menú de bienvenida
                    else:
                        print("❌ ERROR. Opción no válida. Ingrese una letra (A, B o C).")
                        input("Presione ENTER para continuar...")
                        cls() # Limpia después de un error
            else:
                continue # Si el login falla, vuelve al menú de bienvenida
        
        elif accion_elegida == "2": # Opción: NO, AÚN NO ESTOY REGISTRADO / Comprar como invitado
            while True: 
                cls() # Limpia la pantalla antes de mostrar el submenú de registro/invitado
                print("""
                    ¿Qué desea hacer?

                    [1] Crear una cuenta nueva (Requiere contraseña)
                    [2] Comprar como invitado (Solo pago al contado)
                    [3] Regresar al menú principal
                    [4] Salir del programa

                    """)
                sub_accion = input("Seleccione una opción (1-4): ").strip()

                if sub_accion == "1": # Crear una cuenta nueva
                    register_client_session() # Llama a la función de registro de cliente
                    # Después del registro, el usuario puede querer iniciar sesión o ir al menú principal
                    cls() # Limpia después de la acción
                    break # Rompe el sub-bucle, volviendo al menú de bienvenida para que pueda logearse
                elif sub_accion == "2": # Comprar como invitado
                    print("\nComprando como invitado (solo pago al contado).")
                    input("Presiona Enter para ir a los productos...")
                    buy_item("INVITADO") # Llama a la función de comprar en modo invitado
                    cls() # Limpia después de la acción
                    break # Sale del sub-bucle, volviendo al menú de bienvenida
                elif sub_accion == "3": # Regresar al menú principal
                    print("[INFO] Volviendo al menú principal de clientes...")
                    break # Rompe el sub-bucle, volviendo al menú de bienvenida
                elif sub_accion == "4": # Salir del programa
                    print("¡Gracias por usar el programa! Saliendo...") 
                    sys.exit() # Sale del programa
                else:
                    print("🛑 Ingrese una opción válida (1-4).")
                    input("Presione ENTER para continuar...")
                    cls() # Limpia después de un error
        
        elif accion_elegida == "3": # Opción: Salir del programa desde el menú de bienvenida
            print("¡Gracias por usar el programa! Saliendo...") 
            sys.exit() # Sale del programa
        
        else:
            print("🛑 Ingrese una opción válida (1-3).")
            input("Presione ENTER para continuar...")
            cls() # Limpia después de un error

