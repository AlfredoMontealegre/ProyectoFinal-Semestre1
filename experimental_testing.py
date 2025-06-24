productos = ['Adaptador', 'Atornillador', 'Alicate', 'Ambientador', 'Clavo', 'Conector LED', 'Cinta Transparente',
             'Escalera', 'Extension', 'Foco Led', 'Interruptor', 'Lima', 'Mangera', 'Motosierra',
             'Navaja Multiusos', 'Regadera', 'Taladro', 'Yeso', 'Tijeras', 'Ventilador']

precios = [350, 1100, 350, 180, 12.50, 48.50, 50, 3100, 170, 170, 180, 125, 300, 3400, 1300, 200, 1500, 1200, 500, 470]

# testing
num = int(input("Ingrese un numero, porfavor: "))
print(f"{productos[num - 1]} C${precios[num - 1]}")