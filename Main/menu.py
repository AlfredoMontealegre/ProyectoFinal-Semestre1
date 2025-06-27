import Dao.funciones as dao
import Models.clases as mod
import os
import sys
import json
import bcrypt


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

def RegistroSesion():
    cls()
    print("""
          ------> REGISTRO DE NUEVO USUARIO <------
          """)
    nombre_completo = validar_input("Nombres y Apellidos: ", 'str')
    telefono_num = validar_input("Ingrese su número telefónico: ", 'tel')
    cedula_id = validar_input("Digite su número de cédula (sin guiones): ", 'cedula')
    
    usuarios_existentes = clientes.get_all_clientes() 
    
    for user_data in usuarios_existentes: 
        if user_data.id == cedula_id: 
            print("❌ ERROR: Ya existe una cuenta con esta cédula. Intente iniciar sesión.")
            input("Presione Enter para continuar...")
            return None 
        
    password = validar_input("Cree su contraseña: ", permitir_char_password=True)
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    nuevo_cliente = mod.Cliente(nombre_completo, cedula_id, telefono_num, password_hashed)
    clientes.add(nuevo_cliente) 
    
    print("\n¡¡Registro Exitoso!! Ahora puedes iniciar sesión.")
    input("Presione enter para continuar...")
    return nuevo_cliente

def InicioSesion():
    cls()
    print("""
          ====== INICIAR SESIÓN ======
          """) 

    cedula_input = validar_input("Ingrese su usuario (Cédula) sin guiones y espacios: ", 'cedula')
    password_input = validar_input("Ingrese su Contraseña: ", permitir_char_password=True)
    
    usuarios_cargados = clientes.get_all_clientes() 
    
    for user_data in usuarios_cargados: 
        if user_data.cedula == cedula_input:
            if user_data.password_hashed and bcrypt.checkpw(password_input.encode('utf-8'), user_data.password_hashed.encode('utf-8')):
                print(f"¡Bienvenido {user_data.nombre}!") 
                input("Presione Enter para continuar...")
                return user_data 
            else:
                print("\n❌ Cédula o contraseña incorrecta. Intente de nuevo.")
                input("Presione Enter para continuar...")
                return None
        
    print("\n❌ Cédula o contraseña incorrecta. Intente de nuevo.")
    input("Presione Enter para continuar...")
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
        elif tipo == 'tel':
            if not entrada.isdigit() or len(entrada) != 8 or not entrada.startswith(("8", "7", "5", "2")):
                print("🟡 El número ingresado no es válido. Debe tener 8 dígitos y comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                continue
        elif tipo == 'cedula':
            if not entrada.isalnum():
                print("❌ ERROR. La cédula solo puede contener letras y números.")
                continue
            
            letras = sum(1 for char in entrada if char.isalpha())
            numeros = sum(1 for char in entrada if char.isdigit())
            if numeros != 13 or letras != 1 or (numeros + letras) != len(entrada):
                print("❌ ERROR. Datos de cédula inválidos (debe tener 13 números y 1 letra).")
                continue
        return entrada


def obtenerOpcionBienvenida(main_menu=True):
    while True:
        respuesta = input(">>> ").strip()
        
        if not respuesta:
            print("⚠️ CAMPO VACÍO. Intente nuevamente.")
        elif not respuesta.isdigit():
            print("❌ Error. Datos no permitidos. Ingrese un número.")
        else:
            if main_menu: 
                if respuesta in ["1", "2"]:
                    return respuesta
                elif respuesta == "3":
                    return "salir_principal"
                else:
                    print("🛑 Ingrese una opción válida (1, 2 o 3).")
            else: 
                if respuesta in ["1", "2"]:
                    return respuesta
                elif respuesta == "3":
                    return "regresar"
                elif respuesta == "4":
                    return "salir_principal"
                else:
                    print("🛑 Ingrese una opción válida (1, 2, 3 o 4).")
            
def obtenerOpcionDeAccion():
    while True:
        opcion = input("--> ").strip()
        
        if not opcion:
            print("⚠️ CAMPO VACÍO. Intente Nuevamente.")         
        elif not opcion.isalpha() or opcion.lower() not in ["a", "b", "c"]:
            print("❌ ERROR. Opción no válida. Ingrese una letra (A, B o C).") 
        else:
            if opcion.lower() == "a":
                comprarArticulo()
                return "menu_continue"
            elif opcion.lower() == "b":
                verCredito()
                return "menu_continue"
            elif opcion.lower() == "c":
                print("Ha salido de la sesión.") 
                return "salir_sesion"

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
        accion = obtenerOpcionBienvenida(main_menu=True) 

        if accion == "1": 
            usuario_logeado = InicioSesion()
            if usuario_logeado: 
                while True: 
                    cls()
                    menu(usuario_logeado.nombre) 
                    opcion_elegida = obtenerOpcionDeAccion()
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
                sub_accion = obtenerOpcionBienvenida(main_menu=False) 

                if sub_accion == "1":
                    RegistroSesion() 
                elif sub_accion == "2":
                    print("\nComprando como invitado (solo pago al contado).")
                    input("Presiona Enter para ir a los productos...")
                    comprarArticulo() 
                    break 
                
                elif sub_accion == "regresar":
                    break 
                
                elif sub_accion == "salir_principal":
                    print("¡Gracias por usar el programa! Saliendo...") 
                    sys.exit()
                else:
                    continue

        elif accion == "salir_principal": 
            print("¡Gracias por usar el programa! Saliendo...") 
            sys.exit()
        else:
            continue
                

main()

