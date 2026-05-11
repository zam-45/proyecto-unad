# **********************
# CLASE BASE ABSTRACTA
# **********************

class Servicio:

    """Clase base que representa cualquier servicio del sistema.
 
    Aplica encapsulación con properties.
    Las subclases DEBEN sobreescribir calcular_costo() y descripcion().
    """
 
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        # Validación de tarifa
        if tarifa_base <= 0:
            raise ServicioInvalidoError(
                f"La tarifa base debe ser positiva (recibido: {tarifa_base}).")
        # Encapsulación con doble guion bajo
        self.__id = identificador
        self.__nombre = nombre
        self.__tarifa_base = tarifa_base
        self.__disponible = disponible

 # Propiedades de solo lectura 

    @property
    def id(self):
        return self.__id
 
    @property
    def nombre(self):
        return self.__nombre
 
    @property
    def tarifa_base(self):
        return self.__tarifa_base
 
    @property
    def disponible(self):
        return self.__disponible
 
    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)

    # ABSTRACCION
    def calcular_costo(self, duracion):
        """Calcula el costo base. Cada subclase lo implementa diferente."""
        raise NotImplementedError(
            "Las subclases deben implementar calcular_costo().")
 
    def descripcion(self):
        """Devuelve descripción del servicio. Cada subclase la define."""
        raise NotImplementedError(
            "Las subclases deben implementar descripcion().")
 
    def validar(self):
        """Verifica que el servicio tenga datos coherentes."""
        return bool(self.__nombre) and self.__tarifa_base > 0
 
    #  Cálculo con impuesto y descuento (método compartido) 
 
    def calcular_costo_total(self, duracion, impuesto=0.19, descuento=0.0):
        """Aplica impuesto y descuento sobre el costo base calculado.
 
        Argumentos:
            duracion  : horas o días según el tipo de servicio.
            impuesto  : porcentaje de IVA, por defecto 19%.
            descuento : porcentaje de descuento, por defecto 0%.
        """
        if not 0 <= descuento <= 1:
            raise CalculoCostoError(
                f"El descuento debe estar entre 0 y 1 (recibido: {descuento}).")
        if impuesto < 0:
            raise CalculoCostoError(
                f"El impuesto no puede ser negativo (recibido: {impuesto}).")
 
        costo_base = self.calcular_costo(duracion)
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
 
        if costo_final < 0:
            raise CalculoCostoError("El costo final calculado es negativo.")
 
        return round(costo_final, 2)


# ************
# EXCEPCIONES
# ************

class ServicioInvalidoError(Exception):
    """Se activa si los parámetros del servicio son incorrectos."""
    def __init__(self, mensaje="Error: Parámetros del servicio incorrectos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
 
 
class ServicioNoDisponibleError(Exception):
    """Si el servicio solicitado no está disponible o sin stock."""
    def __init__(self, mensaje="Error: El servicio no está disponible."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
 
 
class CalculoCostoError(Exception):
    """Cuando falla el cálculo de costos o impuestos."""
    def __init__(self, mensaje="Error: Fallo calculando el costo total."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# ****************
# RESERVA DE SALA
# *****************

 
class ReservaSala(Servicio):
    """Reserva de salas de reunión, cobrada por horas."""
 
    def __init__(self, identificador, nombre, tarifa_base, capacidad,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser positiva.")
        self.__capacidad = capacidad
 
    def calcular_costo(self, duracion):
        """Costo lineal: tarifa por hora × horas reservadas."""
        if duracion <= 0:
            raise ServicioInvalidoError("La duración debe ser mayor que cero.")
        return self.tarifa_base * duracion
 
    def descripcion(self):
        return (f"[Sala {self.id}] {self.nombre} | "
                f"Capacidad: {self.__capacidad} personas | "
                f"Tarifa: ${self.tarifa_base}/h")

# ******************
# ALQUILER DE EQUIPO
# *******************

class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos, cobrado por días."""
 
    def __init__(self, identificador, nombre, tarifa_base, stock,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if stock < 0:
            raise ServicioInvalidoError("El stock no puede ser negativo.")
        self.__stock = stock
 
    def calcular_costo(self, duracion):
        """Si supera 7 días se aplica un recargo del 10%."""
        if duracion <= 0:
            raise ServicioInvalidoError(
                "Los días de alquiler deben ser positivos.")
        recargo = 1.10 if duracion > 7 else 1.0
        return self.tarifa_base * duracion * recargo
 
    def descripcion(self):
        return (f"[Equipo {self.id}] {self.nombre} | "
                f"Stock: {self.__stock} | "
                f"Tarifa: ${self.tarifa_base}/día")
 
    def reducir_stock(self):
        """Descuenta una unidad del inventario al confirmar el alquiler."""
        if self.__stock <= 0:
            raise ServicioNoDisponibleError(
                f"No hay stock disponible para '{self.nombre}'.")
        self.__stock -= 1


# **********************
# ASESORIA ESPECIALIZADA
# **********************

class AsesoriaTecnica(Servicio):
    """Asesoría especializada cobrada por hora, con tarifa premium."""
 
    def __init__(self, identificador, nombre, tarifa_base, area,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not area:
            raise ServicioInvalidoError(
                "Debe indicar el área de experticia.")
        self.__area = area
 
    def calcular_costo(self, duracion):
        """Tarifa premium (+20%) si la asesoría es de 5 horas o más."""
        if duracion <= 0:
            raise ServicioInvalidoError(
                "La duración de la asesoría debe ser mayor que cero.")
        factor = 1.20 if duracion >= 5 else 1.0
        return self.tarifa_base * duracion * factor
 
    def descripcion(self):
        return (f"[Asesoría {self.id}] {self.nombre} | "
                f"Área: {self.__area} | "
                f"Tarifa: ${self.tarifa_base}/h")


# ***********************
# METODOS SOBRECARGADOS
# ***********************

class ServicioExtra(Servicio):

    def calcular_costo(self, horas):
        return horas * self.precio_base

    def describir(self):
        return self.nombre

    # SOBRECARGA CON DESCUENTO
    def calcular_descuento(self, horas, descuento=0):

        total = self.calcular_costo(horas)

        return total - (total * descuento)

    # SOBRECARGA CON IVA
    def calcular_iva(self, horas, iva=0.19):

        total = self.calcular_costo(horas)

        return total + (total * iva)


# =========================================================
# PRUEBAS DEL SISTEMA
# =========================================================

if __name__ == "__main__":
 
    print("=" * 55)
    print("   PRUEBAS DEL MÓDULO SERVICIO")
    print("=" * 55)
 
    # Prueba 1: Sala válida
    print("\n[1] Crear sala válida")
    sala = ReservaSala("SAL001", "Sala Ejecutiva", 50000, 12)
    print("   ", sala.descripcion())
 
    # Prueba 2: Equipo válido
    print("\n[2] Crear equipo válido")
    equipo = AlquilerEquipo("EQU001", "Proyector 4K", 80000, stock=2)
    print("   ", equipo.descripcion())
 
    # Prueba 3: Asesoría válida
    print("\n[3] Crear asesoría válida")
    asesoria = AsesoriaTecnica("ASE001", "Consultoría Cloud",
                               120000, "AWS / Azure")
    print("   ", asesoria.descripcion())
 
    # Prueba 4: Costo sala (3 horas)
    print("\n[4] Costo sala 3 horas")
    print(f"    ${sala.calcular_costo(3):,.2f}")
 
    # Prueba 5: Costo equipo con recargo (10 días)
    print("\n[5] Costo equipo 10 días (con recargo)")
    print(f"    ${equipo.calcular_costo(10):,.2f}")
 
    # Prueba 6: Costo asesoría premium (6 horas)
    print("\n[6] Costo asesoría 6 horas (tarifa premium)")
    print(f"    ${asesoria.calcular_costo(6):,.2f}")
 
    # Prueba 7: Costo total con IVA y descuento
    print("\n[7] Costo total sala con IVA 19% y descuento 10%")
    print(f"    ${sala.calcular_costo_total(3, impuesto=0.19, descuento=0.10):,.2f}")
 
    # Prueba 8: Tarifa negativa (debe fallar)
    print("\n[8] Tarifa negativa (debe lanzar excepción)")
    try:
        ReservaSala("SAL999", "Sala Fantasma", -5000, 10)
    except ServicioInvalidoError as e:
        print(f"    Excepción controlada: {e}")
 
    # Prueba 9: Descuento inválido (debe fallar)
    print("\n[9] Descuento mayor a 100% (debe lanzar excepción)")
    try:
        sala.calcular_costo_total(3, descuento=1.5)
    except CalculoCostoError as e:
        print(f"    Excepción controlada: {e}")
 
    # Prueba 10: Reducir stock hasta agotarse
    print("\n[10] Reducir stock hasta agotarse")
    try:
        equipo.reducir_stock()
        equipo.reducir_stock()
        equipo.reducir_stock()  # aquí debe fallar
    except ServicioNoDisponibleError as e:
        print(f"    Excepción controlada: {e}")
 
    print("\n" + "=" * 55)
    print("   Módulo probado sin errores inesperados.")
    print("=" * 55)