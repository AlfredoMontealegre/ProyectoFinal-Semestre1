
import os

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
      ==================
""")
    opcion1()
    

def pedirNombre():
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
            return nombre_completo
        
    

def pedirId():
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
        
        else:
            opcion = opcion.lower()
            
            if opcion == "a": 
                comprarArticulo()
                break
            
            elif opcion == "b":
                verCredito()
                break
            
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
    nombre_completo = pedirNombre()
    cedula = pedirId()
    cls()
    print("✅ Registro Completado.")
    print(f"Cliente: {nombre_completo}")
    print(f"Cédula de Identidad: {cedula}")
    input("Presiona Enter para continuar...")
    cls()
    menu(nombre_completo)
    
    
    
    
main()
