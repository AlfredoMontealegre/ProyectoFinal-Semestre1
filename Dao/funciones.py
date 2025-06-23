class ClienteDao:
    def __init__(self):
        self.clientes = []
        
    def add(self, cliente):
        if any(c.cedula == cliente.cedula for c in self.clientes):
            print(f"❌ ERROR: Ya existe un cliente con la cédula '{cliente.cedula}")
            return False
        self.clientes.append(cliente)
        print(f"✔️ Cliente '{cliente.nombre}' agregado con éxito (en memoria).")
        return True
    
    def get_all_clientes(self):
        return self.clientes
    
    def update_clientes(self, cedula_cliente, new_data):
        for i, cliente in enumerate(self.cliente):
            if cliente.cedula == cedula_cliente:
                cliente.nombre = new_data.get('nombre', cliente.nombre)
                cliente.telefono = new_data.get('telefono', cliente.telefono)
                print(f"✔️ Cliente con cédula '{cedula_cliente}' actualizado con éxito (en memoria).")
                return True
        print(f"❌ ERROR: Cliente con cédula '{cedula_cliente}' no encontrado.")
        return False    
    
    def delete_cliente(self, cedula_cliente):
        len_inicial = len(self.clientes)
        self.clientes = [c for c in self.clientes if c.cedula != cedula_cliente]
        if len(self.clientes) < len_inicial:
            print(f"✔️ Cliente con cédula '{cedula_cliente}' eliminado con éxito (en memoria).")
            return True
        print(f"❌ ERROR: Cliente con cédula '{cedula_cliente}' no encontrado.")
        return False
    
    def find_cliente(self, query):
        find_cliente = []
        for c in self.clientes:
            if c.cedula == query or query.lower in c.nombre.lower():
                find_cliente.append(c)
        return find_cliente
    

class AdminDao:
    def __init__(self):
        self.users = []
    
    def add(self, user):
        self.users.append(user)
    
    def show(self):
        for user in self.users:
            print(user)
           

class ProductDao:
    def __init__(self):
        self.products = []
    
    def add(self, prodcut):
        self.products.append(prodcut)
    
    def show(self):
        for product in self.products:
            print(product)  
            