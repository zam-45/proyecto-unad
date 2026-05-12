#-------------------------------------------------------------------
# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programación (213023)
# Estudiante: Jeferson Rangel
# Fase 4 - Componente práctico - Prácticas simuladas
# Archivo: main.py
# Descripción:
#   Archivo principal que integra todo el sistema Software FJ.
#   Ejecuta la simulación de 10+ operaciones combinando casos
#   válidos e inválidos, demostrando que el sistema permanece
#   estable ante errores.
#   Cumple el requisito de la guía: "El sistema debe simular al
#   menos 10 operaciones completas, incluyendo registros válidos
#   e inválidos de clientes, creación correcta e incorrecta de
#   servicios, y reservas exitosas y fallidas."
#-------------------------------------------------------------------

import logging
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaTecnica
from reserva import Reserva
from excepciones import (SoftwareFJError, ClienteInvalidoError,
                         ServicioInvalidoError, ReservaError)
from logger_config import registrar_evento, registrar_error


# ===================================================================
#  GESTOR PRINCIPAL DEL SISTEMA
# ===================================================================
class GestorSoftwareFJ:
    """Coordinador central del sistema. Mantiene listas internas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        registrar_evento("Gestor SoftwareFJ inicializado correctamente.")

    def registrar_cliente(self, cliente):
        # Validamos que no exista ya un cliente con el mismo documento
        if any(c.documento == cliente.documento for c in self._clientes):
            raise ClienteInvalidoError(
                f"Ya existe un cliente con documento {cliente.documento}.")
        self._clientes.append(cliente)
        registrar_evento(f"Cliente {cliente.documento} registrado.")

    def registrar_servicio(self, servicio):
        self._servicios.append(servicio)

    def crear_reserva(self, identificador, cliente, servicio, duracion):
        reserva = Reserva(identificador, cliente, servicio, duracion)
        self._reservas.append(reserva)
        return reserva

    def listar_clientes(self):
        return list(self._clientes)

    def listar_servicios(self):
        return list(self._servicios)

    def listar_reservas(self):
        return list(self._reservas)


# ===================================================================
#  SIMULACIÓN DE OPERACIONES (lo que pide la guía)
# ===================================================================
def ejecutar_simulacion():
    """Ejecuta 10+ operaciones combinando casos válidos e inválidos."""
    print("=" * 70)
    print("   SISTEMA SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print("=" * 70)
    gestor = GestorSoftwareFJ()
    exitosos = 0
    fallidos = 0

    # OPERACIÓN 1: Registro de cliente VÁLIDO
    print("\n[1] Registro de cliente VÁLIDO")
    try:
        c1 = Cliente("Ana María Pérez", "1023456789", "ana@correo.com")
        gestor.registrar_cliente(c1)
        print(f"    OK -> {c1.mostrar()}")
        exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        fallidos += 1

    # OPERACIÓN 2: Cliente con correo INVÁLIDO
    print("\n[2] Registro de cliente con correo INVÁLIDO")
    try:
        c_malo = Cliente("Pedro López", "1099887766", "correo_invalido")
        gestor.registrar_cliente(c_malo)
    except ClienteInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        fallidos += 1

    # OPERACIÓN 3: Segundo cliente VÁLIDO
    print("\n[3] Registro de segundo cliente VÁLIDO")
    try:
        c2 = Cliente("Carlos Rodríguez", "1075432198", "carlos@empresa.co")
        gestor.registrar_cliente(c2)
        print(f"    OK -> {c2.mostrar()}")
        exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        fallidos += 1

    # OPERACIÓN 4: Servicio con tarifa INVÁLIDA
    print("\n[4] Creación de servicio con tarifa INVÁLIDA")
    try:
        ReservaSala("SAL999", "Sala Fantasma", -5000, 10)
    except ServicioInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        fallidos += 1

    # OPERACIÓN 5: Tres servicios VÁLIDOS
    print("\n[5] Creación VÁLIDA de tres servicios especializados")
    try:
        sala = ReservaSala("SAL001", "Sala Ejecutiva", 50000, 12)
        equipo = AlquilerEquipo("EQU001", "Proyector 4K", 80000, stock=2)
        asesoria = AsesoriaTecnica("ASE001", "Consultoría Cloud",
                                   120000, "AWS / Azure")
        for s in (sala, equipo, asesoria):
            gestor.registrar_servicio(s)
            print(f"    OK -> {s.descripcion()}")
        exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        fallidos += 1

    # OPERACIÓN 6: Reserva exitosa de sala
    print("\n[6] Reserva EXITOSA de sala con confirmación y procesamiento")
    try:
        r1 = gestor.crear_reserva("RES001", c1, sala, duracion=3)
        r1.confirmar()
        costo = r1.procesar(impuesto=0.19, descuento=0.10)
        print(f"    OK -> {r1} | Costo total: ${costo:,.2f}")
        exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        fallidos += 1

    # OPERACIÓN 7: Reserva con duración INVÁLIDA
    print("\n[7] Intento de reserva con duración INVÁLIDA (cero)")
    try:
        gestor.crear_reserva("RES002", c2, asesoria, duracion=0)
    except ReservaError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        fallidos += 1

    # OPERACIÓN 8: Asesoría con tarifa premium
    print("\n[8] Reserva de asesoría con tarifa PREMIUM (5+ horas)")
    try:
        r3 = gestor.crear_reserva("RES003", c2, asesoria, duracion=6)
        r3.confirmar()
        costo = r3.procesar()
        print(f"    OK -> {r3} | Costo total: ${costo:,.2f}")
        exitosos += 1
    except SoftwareFJError as e:
        print(f"    ERROR -> {e}")
        fallidos += 1

    # OPERACIÓN 9: Procesar SIN confirmar
    print("\n[9] Procesar reserva SIN confirmar (debe fallar)")
    try:
        r4 = gestor.crear_reserva("RES004", c1, equipo, duracion=4)
        r4.procesar()
    except ReservaError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        fallidos += 1

    # OPERACIÓN 10: Descuento INVÁLIDO (encadenamiento)
    print("\n[10] Procesamiento con descuento INVÁLIDO (>100%)")
    try:
        r5 = gestor.crear_reserva("RES005", c2, equipo, duracion=2)
        r5.confirmar()
        r5.procesar(descuento=1.5)
    except ReservaError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")
        if e.__cause__:
            print(f"    Causa original         -> {e.__cause__}")
        fallidos += 1

    # OPERACIÓN EXTRA: Cliente duplicado
    print("\n[EXTRA] Intento de registro de cliente DUPLICADO")
    try:
        dup = Cliente("Otra Persona", "1023456789", "otra@correo.com")
        gestor.registrar_cliente(dup)
    except ClienteInvalidoError as e:
        print(f"    EXCEPCIÓN CONTROLADA -> {e}")

    # Resumen final
    print("\n" + "=" * 70)
    print("   RESUMEN DE LA SIMULACIÓN")
    print("=" * 70)
    print(f"   Operaciones exitosas: {exitosos}")
    print(f"   Excepciones controladas: {fallidos}")
    print(f"   Total de clientes registrados: {len(gestor.listar_clientes())}")
    print(f"   Total de servicios registrados: {len(gestor.listar_servicios())}")
    print(f"   Total de reservas creadas: {len(gestor.listar_reservas())}")
    print("\n   El sistema permaneció ESTABLE durante toda la simulación.")
    print("   Revise el archivo 'registro_errores.txt' para más detalles.")
    print("=" * 70)


# ===================================================================
#  PUNTO DE ENTRADA
# ===================================================================
if __name__ == "__main__":
    try:
        ejecutar_simulacion()
    except Exception as e:
        registrar_error(f"Error inesperado en ejecución principal: {e}")
        print(f"\n[CRÍTICO] El sistema reportó un error: {e}")
    finally:
        registrar_evento("Fin de la ejecución del Sistema Software FJ.")
        logging.shutdown()
