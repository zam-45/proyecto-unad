

class SoftwareFJError(Exception):
    """Esta es la base de todos nuestros errores. 
    Hereda de 'Exception' para que Python la reconozca."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Se usa cuando los datos del cliente (nombre, ID) están mal."""
    def __init__(self, mensaje="Error: Los datos del cliente no son válidos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ServicioInvalidoError(SoftwareFJError):
    """Se activa si el tipo de servicio o sus parámetros no cuadran."""
    def __init__(self, mensaje="Error: Parámetros del servicio incorrectos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ReservaError(SoftwareFJError):
    """Para problemas generales durante el proceso de reserva."""
    def __init__(self, mensaje="Error: No se pudo procesar la reserva."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ServicioNoDisponibleError(SoftwareFJError):
    """Si el cliente pide algo que ya está ocupado o no existe."""
    def __init__(self, mensaje="Error: El servicio solicitado no está disponible."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class CalculoCostoError(SoftwareFJError):
    """Específico para cuando falle la cuenta de los cobros o impuestos."""
    def __init__(self, mensaje="Error: Hubo un fallo calculando el costo total."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)