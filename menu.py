# Proyecto Final
## PM-001 - Menu
# Prototipo 1 de como puede ser el menu, (estado incompleto)

import time
import os

def definir(usuario, comprar, estado, saludo):
    return f"Bienvenido {usuario}, seleccione una opcion {comprar} o {estado}"

def main():
    print("="*25)
    print("Bienvenido a Control de Credito")
    print("="*25)
    usuario = str(input("Ingrese su nombre: "))
    os.system("cls||clear")
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

main()
