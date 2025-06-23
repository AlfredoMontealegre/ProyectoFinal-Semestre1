# Prototipo de Venta para los inventarios

productos = ['Adaptador', 'Atornillador', 'Alicate', 'Ambientador', 'Clavo', 'Conector LED', 'Cinta Transparente',
             'Escalera', 'Extension', 'Foco Led', 'Interruptor', 'Lima', 'Mangera', 'Motosierra',
             'Navaja Multiusos', 'Regadera', 'Taladro', 'Yeso', 'Tijeras', 'Ventilador']

# 0 - 19 (Valores) | 20 Productos
# Los precios se alinearan de acuerdo a los productos.

def mostrar_menu():
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
print(f"Has seleccionado: {producto_seleccionado}")
