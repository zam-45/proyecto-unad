class Servicios:
    def __init__(self,servicio="",precio_base=0.0):
        self.servicio=servicio.lower()
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo")
        self.precio_base = precio_base 
    
    def validar_servicio(self):

        if self.servicio in ["reserva de salas","alquiler de equipos","asesorias especializadas"]:
            return self.servicio
        else:
            raise ValueError(f"Error: El servicio '{self.servicio}' no es reconocido por Software FJ.")
    
    def calcular_costo(self):
        return self.precio_base
    
    def describir_sercicio(self):
        return self.servicio

persona1=Servicios("reserva de salas",2000)
persona1.validar_servicio()



    