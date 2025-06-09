from datetime import datetime, timedelta

def calcular_dias_restantes():
    # Obtener la fecha actual
    hoy = datetime.now().date()
    print(f"Fecha de hoy: {hoy.strftime('%d/%m/%Y')}")
    
    # Mostrar opciones al usuario
    print("\nOpciones de plazo para pagar:")
    print("1. 15 días")
    print("2. 30 días")
    
    try:
        # Solicitar la opción al usuario
        opcion = int(input("Seleccione una opción (1 o 2): "))
        
        if opcion == 1:
            dias_plazo = 15
        elif opcion == 2:
            dias_plazo = 30
        else:
            print("Opción no válida. Por favor seleccione 1 o 2.")
            return
        
        # Calcular fecha de vencimiento
        fecha_vencimiento = hoy + timedelta(days=dias_plazo)
        
        # Calcular días restantes
        dias_restantes = (fecha_vencimiento - hoy).days
        
        # Mostrar resultados
        print(f"\nResumen:")
        print(f"- Fecha de compra: {hoy.strftime('%d/%m/%Y')}")
        print(f"- Plazo seleccionado: {dias_plazo} días")
        print(f"- Fecha de vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')}")
        print(f"- Días restantes para pagar: {dias_restantes} días")
        
    except ValueError:
        print("Error: Por favor ingrese un número válido (1 o 2).")


    calcular_dias_restantes()