class ClienteDao:
    def __init__(self):
        self.clientes = []
        
    def add(self, cliente):
        self.clientes.append(cliente)
    
    def show(self):
        for cliente in self.clientes:
            print(cliente)


class ProdcutDao:
    def __init__(self):
        self.products = []
    
    def add(self, prodcut):
        self.products.append(prodcut)
    
    def show(self):
        for product in self.products:
            print(product)  
            