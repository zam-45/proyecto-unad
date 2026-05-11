#-------------------------------------------------------------------
# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programación (213023)
# Estudiante: Jeferson Rangel
# Fase 4 - Componente práctico
# Archivo: servicio.py
# Descripción:
#   Clase abstracta Servicio y sus 3 subclases especializadas:
#   ReservaSala, AlquilerEquipo, AsesoriaTecnica.
#   Cumple con el requisito de la guía: "Una clase abstracta
#   Servicio y al menos tres servicios especializados que hereden
#   de ella, implementando polimorfismo y métodos sobrescritos
#   para calcular costos, describir servicios y validar parámetros."
#-------------------------------------------------------------------

from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import (ServicioInvalidoError, ServicioNoDisponibleError,
                         CalculoCostoError)
from logger_config import registrar_evento


# ===================================================================
#  CLASE ABSTRACTA: Servicio
# ===================================================================
class Servicio(EntidadBase):
    """Clase abstracta que representa cualquier servicio ofrecido."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        # Validamos la tarifa: no puede ser negativa ni cero
        if tarifa_base <= 0:
            raise ServicioInvalidoError(
                f"La tarifa base debe ser positiva (recibido: {tarifa_base}).")
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible

    # Propiedades encapsuladas
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # Método abstracto: cada servicio calcula su costo de forma diferente
    @abstractmethod
    def calcular_costo(self, duracion):
        """Calcula el costo base del servicio. Cada subclase lo implementa."""
        pass

    # Método sobrecargado: aplica impuestos y descuentos opcionales
    # En Python la sobrecarga se simula con parámetros por defecto.
    def calcular_costo_total(self, duracion, impuesto=0.19, descuento=0.0):
        """Versión avanzada que aplica impuesto y descuento.

        Argumentos:
            duracion (float): horas o días según el servicio.
            impuesto (float): porcentaje de IVA, por defecto 19%.
            descuento (float): porcentaje de descuento, por defecto 0%.
        """
        # Validaciones de los parámetros
        if not 0 <= descuento <= 1:
            raise CalculoCostoError(
                f"El descuento debe estar entre 0 y 1 (recibido: {descuento}).")
        if impuesto < 0:
            raise CalculoCostoError(
                f"El impuesto no puede ser negativo (recibido: {impuesto}).")
        # Cálculo polimórfico: cada subclase ejecuta su propia versión
        costo_base = self.calcular_costo(duracion)
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        if costo_final < 0:
            raise CalculoCostoError("El costo final calculado es negativo.")
        return round(costo_final, 2)

    def validar(self):
        return bool(self._nombre) and self._tarifa_base > 0


# ===================================================================
#  SUBCLASE 1: ReservaSala
# ===================================================================
class ReservaSala(Servicio):
    """Servicio de reserva de salas de reunión cobrado por horas."""

    def __init__(self, identificador, nombre, tarifa_base, capacidad,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser positiva.")
        self._capacidad = capacidad
        registrar_evento(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion):
        # Para salas el costo es lineal: tarifa por horas
        if duracion <= 0:
            raise ServicioInvalidoError("La duración debe ser mayor que cero.")
        return self._tarifa_base * duracion

    def descripcion(self):
        return (f"[Sala {self._id}] {self._nombre} | Capacidad: "
                f"{self._capacidad} personas | Tarifa: ${self._tarifa_base}/h")


# ===================================================================
#  SUBCLASE 2: AlquilerEquipo
# ===================================================================
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos por días."""

    def __init__(self, identificador, nombre, tarifa_base, stock,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if stock < 0:
            raise ServicioInvalidoError("El stock no puede ser negativo.")
        self._stock = stock
        registrar_evento(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion):
        # Si el alquiler supera 7 días, se aplica un recargo del 10%
        if duracion <= 0:
            raise ServicioInvalidoError(
                "Los días de alquiler deben ser positivos.")
        recargo = 1.10 if duracion > 7 else 1.0
        return self._tarifa_base * duracion * recargo

    def descripcion(self):
        return (f"[Equipo {self._id}] {self._nombre} | Stock: {self._stock} | "
                f"Tarifa: ${self._tarifa_base}/día")

    def reducir_stock(self):
        """Reduce el inventario en una unidad al confirmar alquiler."""
        if self._stock <= 0:
            raise ServicioNoDisponibleError(
                f"No hay stock disponible para '{self._nombre}'.")
        self._stock -= 1


# ===================================================================
#  SUBCLASE 3: AsesoriaTecnica
# ===================================================================
class AsesoriaTecnica(Servicio):
    """Servicio de asesoría especializada cobrada por hora."""

    def __init__(self, identificador, nombre, tarifa_base, area,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        if not area:
            raise ServicioInvalidoError("Debe indicar el área de experticia.")
        self._area = area
        registrar_evento(f"Servicio creado: {self.descripcion()}")

    def calcular_costo(self, duracion):
        # Tarifa premium (+20%) si la asesoría es de 5 horas o más
        if duracion <= 0:
            raise ServicioInvalidoError(
                "La duración de la asesoría debe ser > 0.")
        factor = 1.20 if duracion >= 5 else 1.0
        return self._tarifa_base * duracion * factor

    def descripcion(self):
        return (f"[Asesoría {self._id}] {self._nombre} | Área: {self._area} | "
                f"Tarifa: ${self._tarifa_base}/h")
