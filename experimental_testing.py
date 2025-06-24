productos = ['Adaptador', 'Atornillador', 'Alicate', 'Ambientador', 'Clavo', 'Conector LED', 'Cinta Transparente',
             'Escalera', 'Extension', 'Foco Led', 'Interruptor', 'Lima', 'Mangera', 'Motosierra',
             'Navaja Multiusos', 'Regadera', 'Taladro', 'Yeso', 'Tijeras', 'Ventilador']

precios = [350, 1100, 350, 180, 12.50, 48.50, 50, 3100, 170, 170, 180, 125, 300, 3400, 1300, 200, 1500, 1200, 500, 470]


# Unidades y Cantidades
# testing
num = int(input("Ingrese un numero, porfavor: "))
item = (productos[num - 1])
precio_item = (precios[num - 1])
print(f"Has elegido: {item} C${precio_item}")

cant = int(input(f"Ingrese la cantidad de: {productos[num - 1]} a llevar: "))

converter = int(precio_item)
total = (cant * converter)
print(f"Por la cantidad de {cant} de {item} el precio es: {total}.")