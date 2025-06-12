import Dao.funciones as dao
import Models.clases as mod
import os

producutos = dao.ProdcutDao()
clientes = dao.ClienteDao()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

    
def menu(usuario):
    print(f"""
     ===================
      ------------> [Plazo de Credito, 2025]
      Bienvenido {usuario}!!

      [-] Que haras el dia de hoy?
      (Presiona la tecla correspondiente para elegir.)
      ------
      Comprar un articulo [A]
      Ver estado de credito [B]
      Salir del programa [C]
      ==================
""")
    opcion1()
    

def nombre():
    while True:
        nombre = input("Nombres: ").strip()
    
        if not nombre:
            print("⚠️  CAMPO VACÍO. Intente Nuevamente.")

        elif not nombre.replace(" ", "").isalpha():
            print("❌ ERROR. Ingrese un dato valido.")
    
        else:
            break
      
    while True:
        apellido = input("apellidos: ").strip()
    
        if not apellido:
            print("⚠️  CAMPO VACÍO. Intente Nuevamente.")

        elif not apellido.replace(" ", "").isalpha():
            print("❌ ERROR. Ingrese un dato valido.")
    
        else:
            nombre_completo = nombre + " " + apellido
            cls()
            break
    return nombre_completo
        

def telefono():
     
    while True:
            telefono = (input("Ingrese su número telefonico: ")).strip()
            
            if not telefono:
                print("⚠️  CAMPO VACÍO. Intente Nuevamente.")
            
            elif not telefono.isdigit():
                print("❌ ERROR. Datos de número de telefono invalidos.") 
            
            else:
                if len(telefono) != 8:
                    print("🟡 Revise los digitos de su teléfono.")
                
                elif not telefono.startswith(("8", "7", "5", "2")):
                    print("🟡 El número ingresado no es válido. Los números deben comenzar con 2 (fijos), 5, 7 u 8 (móviles).")
                
                else:
                    return telefono
        
def IdCedula():
     while True:
        cedula = input("Digite su número de cédula: ").strip()

        if not cedula:
            print("⚠️  CAMPO VACÍO. Intente Nuevamente.")
                
        else:
           solo_cedula = cedula.replace("-", "").replace(" ", "")
           
           letras = [letra for letra in solo_cedula if letra.isalpha()]
           numeros = [num for num in solo_cedula if num.isdigit()]
           
           if len(numeros) != 13:
               print("🟡 Revise los digitos de su cédula.")
        
           elif len(letras) != 1:
               print("🟡 La cédula solo puede contener una letra.")
            
           elif len(numeros) + len(letras) != len(solo_cedula):
               print("❌ ERROR. Datos de cédula invalidos.")
            
           else:
                return cedula
    

def opcion1():
    while True:
        opcion = input("--> ").strip()
        
        if not opcion:
            print("⚠️  CAMPO VACÍO. Intente Nuevamente.")            
        
        elif not opcion.isalpha():
            print("❌ ERROR. Opción no valida.")
        
        elif opcion.lower() == "a":
            comprarArticulo()
            return "menu_continue"
            
        elif opcion.lower() == "b":
            verCredito()
            return "menu_continue"
        
        elif opcion.lower() == "c":
            print("Ha salido del programa.")
            return "salir"
            
        else:
            print("🛑 Ingrese una opción valida.")

def comprarArticulo():
    input

def verCredito():
    input


                
def main():
    
    cls()
    print(" Registro de cliente ".center(40, "="))
    print(" Ingrese los siguientes datos ".center(40, "="))
    comprador = nombre()
    identificacion = IdCedula()
    contacto = telefono()
    cliente = mod.Cliente(comprador, identificacion, contacto)
    clientes.add(cliente)
    
    cls()
    print("✅ Registro Completado.")
    
    
    
    while True:
        cls()
        menu(comprador)
        accion = opcion1
        
        if accion == "salir":
            break
    
    
    
    
main()
