# Prototipo de Venta para los inventarios

productos = ['Adaptador', 'Atornillador', 'Alicate', 'Ambientador', 'Clavo', 'Conector LED', 'Cinta Transparente',
              'Escalera', 'Extension', 'Foco Led', 'Interruptor', 'Lima', 'Mangera', 'Motosierra',
              'Navaja Multiusos', 'Regadera', 'Taladro', 'Yeso', 'Tijeras', 'Ventilador']

# 0 - 19 (Valores) | 20 Productos
# Los precios se alinearan de acuerdo a los productos.


print("""====> Bienvenido a la Tienda, que quisiera comprar?
      (Presiona el numero del producto para elegirlo)
      
      1. Adaptador      6. Conector LED
      2. Atornillador   7. Cinta Transparente
      3. Alicate        8. Escalera
      4. Ambientador    9. Extension
      5. Clavo         10. Foco LED                   
           """)

num = int(input("Ingrese el numero de producto: "))


if num <= 0:
    print("[ERROR] Numero no permitido")
elif num > 10:
    print("[ERROR] El numero no esta")
else: print( "----------"
    
    f" Has seleccionado: {productos[num]}")
