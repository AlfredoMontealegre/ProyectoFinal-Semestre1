import Dao.funciones as dao
import Models.clases as mod
import os

USER_FILENAME = 'usuarios.txt'

BASE_PATH = "C:\\Users\\atorr\\OneDrive\\Documentos\\Archivo\\"

USER_FILE_PATH = os.path.join(BASE_PATH, USER_FILENAME)

productos = dao.ProdcutDao()
clientes = dao.ClienteDao()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def accionUsuario():
    cls()
    print("""
                  -> GLOBAL TOOLS S.A <-
            
                    ===== Bienvenido =====
            
                  ¿Estás registrado con nosotros?
            
                    [1] SI, INICIAR SESIÓN     
                    [2] NO, AÚN NO ESTOY REGISTRADO
                    [3] Salir del programa
            
        (Para utilizar las opciones de crédito debe tener registro)
            
          """)

def menu(usuario_nombre):
    """Muestra el menú para un usuario que ha iniciado sesión."""
    print(f"""
     ===================
      ------------> [GLOBAL TOOLS S.A, 2025]
      Bienvenido {usuario_nombre}!!

      [-] ¿Qué harás el día de hoy?
      (Presiona la tecla correspondiente para elegir.)
      ------
      Comprar un artículo [A]
      Ver estado de crédito [B]
      Salir de la sesión [C]
      ==================
""") 

def nombre():
    """Solicita y valida el nombre y apellido."""
    while True:
        nombre_pila = input("Nombres: ").strip() 
        if not nombre_pila:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        elif not nombre_pila.replace(" ", "").isalpha():
            print("❌ ERROR. Ingrese un dato válido (solo letras).")
        else:
            break
    
    while True:
        apellido_pila = input("Apellidos: ").strip() 
        if not apellido_pila:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        elif not apellido_pila.replace(" ", "").isalpha():
            print("❌ ERROR. Ingrese un dato válido (solo letras).")
        else:
            break
            
    nombre_completo = nombre_pila + " " + apellido_pila
    cls() 
    return nombre_completo
        
def telefono():
    while True:
        telefono_num = input("Ingrese su número telefónico: ").strip()
        if not telefono_num:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        elif not telefono_num.isdigit():
            print("❌ ERROR. Datos de número de teléfono inválidos (solo dígitos).") 
        elif len(telefono_num) != 8:
            print("🟡 Revise los dígitos de su teléfono (debe tener 8 dígitos).")
        elif not telefono_num.startswith(("8", "7", "5", "2")):
            print("🟡 El número ingresado no es válido. Los números deben comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
        else:
            return telefono_num
        
def IdCedula():
    while True:
        cedula = input("Digite su número de cédula (sin guiones): ").strip()
        if not cedula:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        else:
            solo_cedula = cedula.replace(" ", "") 
            
            letras = [char for char in solo_cedula if char.isalpha()]
            numeros = [char for char in solo_cedula if char.isdigit()]
            
            if len(numeros) != 13:
                print("🟡 Revise los dígitos de su cédula (debe tener 13 números).")
            elif len(letras) != 1:
                print("🟡 La cédula solo puede contener una letra.")
            elif (len(numeros) + len(letras)) != len(solo_cedula):
                print("❌ ERROR. Datos de cédula inválidos (solo números y una letra).")
            else:
                return cedula


def GuardarUsuario(cliente_obj, password_str): 
    with open(USER_FILE_PATH, 'a', encoding='utf-8') as file:

        file.write(f"{cliente_obj.id},{cliente_obj.nombre},{cliente_obj.telefono},{password_str}\n")

def cargarUsuario():
    usuarios = [] 
    

    if os.path.exists(USER_FILE_PATH):
        with open(USER_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                parts = [p.strip() for p in parts] 
                
                if len(parts) == 4:
                    cedula, nombre, telefono, password = parts
                    usuarios.append({
                        "cedula": cedula, 
                        "nombre": nombre, 
                        "telefono": telefono, 
                        "password": password
                    })
    return usuarios
    
def RegistroSesion():
    cls()
    print("""
          ------> REGISTRO DE NUEVO USUARIO <------
          """)
    nombre_completo = nombre()
    telefono_num = telefono()
    cedula_id = IdCedula()
    
    usuarios_existentes = cargarUsuario() 
    
    for user_data in usuarios_existentes: 
        if user_data["cedula"] == cedula_id: 
            print("❌ ERROR: Ya existe una cuenta con esta cédula. Intente iniciar sesión.")
            input("Presione Enter para continuar...")
            return None 
        
    while True:
        password = input("Cree su contraseña: ").strip()
        if not password:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        else:
            break

    nuevo_cliente = mod.Cliente(nombre_completo, cedula_id, telefono_num)
    
    clientes.add(nuevo_cliente) 
   
    GuardarUsuario(nuevo_cliente, password)
    
    print("\n¡¡Registro Exitoso!! Ahora puedes iniciar sesión.")
    input("Presione enter para continuar...")
    return nuevo_cliente

def InicioSesion():
    cls()
    print("""
          ====== INICIAR SESIÓN ======
          """) 

    while True: 
        cedula_input = input("Ingrese su usuario (Cédula) sin guiones y espacios: ").strip()
        if not cedula_input:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        else:
            break 
        
    while True:
        password_input = input("Ingrese su Contraseña: ").strip()
        if not password_input:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")
        else:
            break 
    
    usuarios_cargados = cargarUsuario() 
    
    for user_data in usuarios_cargados: 
        if user_data["cedula"] == cedula_input and user_data["password"] == password_input:
            print(f"¡Bienvenido {user_data['nombre']}!") 
            input("Presione Enter para continuar...")
            return mod.Cliente(user_data['nombre'], user_data['cedula'], user_data['telefono']) 
        
    print("\n❌ Cédula o contraseña incorrecta. Intente de nuevo.")
    input("Presione Enter para continuar...")
    return None 

def opcion1(main_menu=True):
    while True:
        respuesta = input(">>> ").strip()

        if not respuesta:
            print("⚠️ CAMPO VACÍO. Intente nuevamente.")
        elif not respuesta.isdigit():
            print("❌ Error. Datos no permitidos. Ingrese un número.")
        else:
            if main_menu: 
                if respuesta == "1" or respuesta == "2": 
                    return respuesta
                elif respuesta == "3": 
                    return "salir_principal"
                else:
                    print("🛑 Ingrese una opción válida (1, 2 o 3).")
            else: 
                if respuesta == "1" or respuesta == "2":
                    return respuesta
                elif respuesta == "3":
                    return "regresar"
                elif respuesta == "4":
                    return "salir_principal"
                else:
                    print("🛑 Ingrese una opción válida (1, 2, 3 o 4).") 
            
def opcion2():
    while True:
        opcion = input("--> ").strip()
        
        if not opcion:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")         
        elif not opcion.isalpha():
            print("❌ ERROR. Opción no válida. Ingrese una letra (A, B o C).") 
        elif opcion.lower() == "a":
            comprarArticulo()
            return "menu_continue"
        elif opcion.lower() == "b":
            verCredito()
            return "menu_continue"
        elif opcion.lower() == "c":
            print("Ha salido de la sesión.") 
            return "salir_sesion"
        else:
            print("🛑 Ingrese una opción válida (A, B o C).") 

def comprarArticulo():
    cls()
    print("""
          ------> Comprar Artículo (Modo Contado/Crédito) <------
          """)
    input("Presione Enter para continuar...")
    
def verCredito():
    cls()
    print("""
          ------> Ver Estado de Crédito <------
          """)
    input("Presione Enter para continuar...")
    
    
def main():
    while True:
        accionUsuario()
        accion = opcion1(main_menu=True) 

        if accion == "1": 
            usuario_logeado = InicioSesion()
            if usuario_logeado: 
                while True: 
                    cls()
                    menu(usuario_logeado.nombre) 
                    opcion_elegida = opcion2()
                    if opcion_elegida == "salir_sesion":
                        break 
            else:
                continue 

        elif accion == "2": 
            while True: 
                cls()
                print("""
                            ¿Qué desea hacer?

                [1] Crear una cuenta nueva (Requiere contraseña)
                [2] Comprar como invitado (Solo pago al contado)
                [3] Regresar al menú principal
                [4] Salir del programa

                """)
                sub_accion = opcion1(main_menu=False) 

                if sub_accion == "1":
                    RegistroSesion() 
                elif sub_accion == "2":
                    print("\nComprando como invitado (solo pago al contado).")
                    input("Presiona Enter para ir a los productos...")
                    comprarArticulo() 
                    break 
                
                elif sub_accion == "3":
                    break 
                
                elif sub_accion == "4":
                    print("¡Gracias por usar el programa! Saliendo...")
                    return 

        elif accion == "salir_principal": 
            print("¡Gracias por usar el programa! Saliendo...")
            return 
main()