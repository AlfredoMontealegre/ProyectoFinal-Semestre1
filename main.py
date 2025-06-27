# main.py
# Este es el punto de entrada principal para el sistema Global Tools.
# Permite al usuario seleccionar si desea acceder como Administrador o como Cliente,
# y delega el control a los módulos de aplicación respectivos.

import sys
import os

# Importa los módulos de aplicación separados para cada rol
import auth # Contiene la lógica de autenticación específica para Administradores
import admin_app # La aplicación completa para el rol de Administrador
import client_app # La aplicación completa para el rol de Cliente

def cls():
    """
    Limpia la consola. Detecta el sistema operativo para usar el comando adecuado.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_initial_choice_menu():
    """
    Muestra el menú inicial al usuario para que elija su rol
    (Administrador o Cliente).
    """
    print("\n" + "=" * 50)
    print("         BIENVENIDO A GLOBAL TOOLS S.A.")
    print("=" * 50)
    print("Por favor, seleccione su rol para continuar:")
    print("1. Administrador del Sistema")
    print("2. Cliente (Usuario Común)")
    print("3. Salir del Programa")
    print("=" * 50)

def main():
    """
    Función principal que controla el flujo de la aplicación Global Tools.
    Inicia mostrando el menú de selección de rol y dirige al usuario
    a la aplicación correspondiente después de la autenticación (si aplica).
    """
    while True:
        cls() # Limpia la pantalla al inicio de cada iteración del menú principal
        display_initial_choice_menu() # Muestra las opciones de rol
        choice = input("Seleccione una opción (1-3): ").strip() # Captura la elección del usuario

        if choice == '1': # Opción: Administrador del Sistema
            cls()
            print("--- ACCESO DE ADMINISTRADOR ---")
            # Se delega el proceso de autenticación de administradores al módulo `auth`.
            # `auth.inicializar_auth()` manejará la solicitud de credenciales
            # y los intentos de login, así como la creación de usuarios administradores por defecto.
            if auth.inicializar_auth(): 
                # Si el login de administrador es exitoso (auth.inicializar_auth retorna True),
                # se inicia la aplicación del administrador.
                admin_app.run_admin_app() 
            else:
                # Si el login de administrador falla después de los intentos permitidos,
                # `auth.inicializar_auth` ya imprime un mensaje de salida y, en última instancia,
                # `sys.exit()` termina el programa si se agotaron los intentos.
                # Si el usuario eligió salir del menú de login de admin, simplemente
                # continuaremos el bucle para volver al menú de selección de rol principal.
                continue 

        elif choice == '2': # Opción: Cliente (Usuario Común)
            cls()
            print("--- ACCESO DE CLIENTE ---")
            # Se delega completamente la lógica de la aplicación de cliente al módulo `client_app`.
            # `client_app.run_client_app()` manejará su propio menú de bienvenida,
            # opciones de registro/login de clientes y el ciclo de acciones.
            client_app.run_client_app()
            # Cuando el usuario elige salir de `client_app.run_client_app()`, el control
            # regresa a este punto, y el bucle `while True` de `main()` continúa,
            # volviendo a mostrar el menú de selección de rol inicial.

        elif choice == '3': # Opción: Salir del Programa
            print("👋 ¡Gracias por usar el programa! Saliendo...")
            sys.exit() # Termina la ejecución del programa.
        else:
            print("🛑 ERROR: Opción no válida. Por favor, seleccione 1, 2 o 3.")
            input("Presione ENTER para continuar...")

# Asegura que la función main() se ejecute solo cuando el script es ejecutado directamente.
main()

