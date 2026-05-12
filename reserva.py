#-------------------------------------------------------------------
# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programación (213023)
# Estudiante: Jeferson Rangel
# Fase 4 - Componente práctico
# Archivo: reserva.py
# Descripción:
#   Clase Reserva que integra cliente, servicio, duración y estado.
#   Implementa confirmación, cancelación y procesamiento con
#   manejo robusto de excepciones.
#   Cumple con el requisito de la guía: "Una clase Reserva que
#   integre cliente, servicio, duración y estado, e implemente
#   confirmación, cancelación y procesamiento con manejo de
#   excepciones."
#-------------------------------------------------------------------

from datetime import datetime
from cliente import Cliente
from servicios import Servicio, AlquilerEquipo
from excepciones import (ReservaError, ServicioNoDisponibleError,
                         CalculoCostoError, SoftwareFJError)
from logger_config import registrar_evento, registrar_error


class Reserva:
    """Representa una reserva que vincula un cliente con un servicio."""

    # Estados válidos del ciclo de vida de la reserva
    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, identificador, cliente, servicio, duracion):
        # Validaciones iniciales
        if not isinstance(cliente, Cliente):
            raise ReservaError("Se requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Se requiere un objeto Servicio válido.")
        if duracion <= 0:
            raise ReservaError("La duración debe ser mayor que cero.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible.")
        self._id = identificador
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._fecha_reserva = datetime.now()
        registrar_evento(f"Reserva {self._id} creada para "
                         f"{cliente.nombre} -> {servicio.nombre}")

    # Propiedades de solo lectura
    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    # ---------- Operaciones con manejo de excepciones ----------

    def confirmar(self):
        """Confirma la reserva. Usa try/except/else."""
        try:
            if self._estado != "PENDIENTE":
                raise ReservaError(
                    f"No se puede confirmar una reserva en estado "
                    f"'{self._estado}'.")
        except ReservaError as e:
            # Registramos el error y relanzamos para que el llamador lo gestione
            registrar_error(f"Error al confirmar reserva {self._id}: {e}")
            raise
        else:
            # El bloque 'else' se ejecuta solo si NO hubo excepción
            self._estado = "CONFIRMADA"
            registrar_evento(f"Reserva {self._id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada."""
        if self._estado == "PROCESADA":
            raise ReservaError(
                "No se puede cancelar una reserva ya procesada.")
        self._estado = "CANCELADA"
        registrar_evento(f"Reserva {self._id} cancelada.")

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Procesa la reserva: calcula el costo total y actualiza estado.

        Demuestra try/except/finally y el encadenamiento de excepciones
        con 'raise ... from ...'.
        """
        costo_total = 0.0
        try:
            if self._estado != "CONFIRMADA":
                raise ReservaError(
                    "Solo se pueden procesar reservas confirmadas.")
            # Cálculo polimórfico: el servicio decide cómo calcular
            costo_total = self._servicio.calcular_costo_total(
                self._duracion, impuesto, descuento)
            # Si es alquiler de equipo, descontamos del stock
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.reducir_stock()
            self._estado = "PROCESADA"
        except CalculoCostoError as e:
            # ENCADENAMIENTO de excepciones: nueva excepción con causa original
            registrar_error(f"Error de cálculo en reserva {self._id}: {e}")
            raise ReservaError(
                "No se pudo procesar la reserva por cálculo inválido.") from e
        except SoftwareFJError as e:
            registrar_error(f"Error procesando reserva {self._id}: {e}")
            raise
        finally:
            # El bloque 'finally' se ejecuta SIEMPRE (con o sin error)
            registrar_evento(f"Procesamiento finalizado para reserva "
                             f"{self._id} | estado: {self._estado}")
        return costo_total

    def __str__(self):
        return (f"Reserva[{self._id}] Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | "
                f"Duración: {self._duracion} | Estado: {self._estado}")
