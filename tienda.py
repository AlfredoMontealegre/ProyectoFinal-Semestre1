import os

# Prototipo de Venta para los inventarios

productos = ['Adaptador', 'Atornillador', 'Alicate', 'Ambientador', 'Clavo', 'Conector LED', 'Cinta Transparente',
             'Escalera', 'Extension', 'Foco Led', 'Interruptor', 'Lima', 'Mangera', 'Motosierra',
             'Navaja Multiusos', 'Regadera', 'Taladro', 'Yeso', 'Tijeras', 'Ventilador']

precios = [350, 1100, 350, 180, 12.50, 48.50, 50, 3100, 170, 170, 180, 125, 300, 3400, 1300, 200, 1500, 1200, 500, 470]

# 0 - 19 (Valores) | 20 Productos
# Los precios se alinearan de acuerdo a los productos.

# Un comando para limpiar la pantalla, solo necesitas poner "limpiar_pantalla() en algo y lo hace automaticamente"
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    print("""====> Bienvenido a la Tienda, que quisiera comprar?
      (Presiona el numero del producto para elegirlo)

      1. Adaptador      6. Conector LED         11. Interruptor         16. Regadera 
      2. Atornillador   7. Cinta Transparente   12. Lima                17. Taladro
      3. Alicate        8. Escalera             13. Mangera             18. Yeso
      4. Ambientador    9. Extension            14. Motosierra          19. Tijeras
      5. Clavo         10. Foco LED             15. Navaja Multiusos    20. Ventilador 
           """)

def pedir_seleccion():
    while True:
        seleccion = input("---> Selecciona el número del producto que deseas comprar: ").strip()

        if not seleccion:
            print("❌ [Error] El campo está vacío. Por favor, ingresa un número del 1 al 20.")
            continue

        if not seleccion.isdigit():
            print("❌ [Error] Solo se aceptan números enteros positivos del 1 al 20.")
            continue

        seleccion = int(seleccion)

        if seleccion < 1 or seleccion > len(productos):
            print("❌ [Error] El número debe estar entre 1 y 20.")
            continue

        return seleccion

mostrar_menu()
opcion = pedir_seleccion()
producto_seleccionado = productos[opcion - 1]
print(f"Has seleccionado: {producto_seleccionado} C${precios[opcion - 1]}")
