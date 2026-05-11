# **********************
# CLASE BASE ABSTRACTA
# **********************

class Servicio:

    def __init__(self, nombre, precio_base):

        # ENCAPSULACION
        self.__nombre = nombre
        self.__precio_base = precio_base
        self.__disponible = True

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio_base(self):
        return self.__precio_base

    @property
    def disponible(self):
        return self.__disponible

    def activar(self):
        self.__disponible = True

    def desactivar(self):
        self.__disponible = False

    # ABSTRACCION
    def calcular_costo(self, horas):
        raise NotImplementedError(
            "Las clases hijas deben implementar este metodo"
        )

    def describir(self):
        raise NotImplementedError(
            "Las clases hijas deben implementar este metodo"
        )


# ************
# EXCEPCIONES
# ************

class ServicioError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


# ****************
# RESERVA DE SALA
# *****************

class ReservaSala(Servicio):

    def __init__(self, numero_sala, capacidad, precio_base):

        super().__init__("Sala", precio_base)

        self.__numero_sala = numero_sala
        self.__capacidad = capacidad

    # POLIMORFISMO
    def calcular_costo(self, horas):

        if self.disponible == False:
            raise ServicioNoDisponibleError(
                "La sala no esta disponible"
            )

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores a 0"
            )

        return self.precio_base * horas

    def describir(self):

        return (
            "Sala: " + str(self.__numero_sala) +
            " | Capacidad: " + str(self.__capacidad)
        )


# ******************
# ALQUILER DE EQUIPO
# *******************

class AlquilerEquipo(Servicio):

    def __init__(self, tipo, precio_base):

        super().__init__(tipo, precio_base)

        self.__tipo = tipo

    # POLIMORFISMO
    def calcular_costo(self, horas):

        if self.disponible == False:
            raise ServicioNoDisponibleError(
                "El equipo no esta disponible"
            )

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores a 0"
            )

        # CALCULO DE DIAS SIN IMPORTAR LIBRERIAS
        dias = horas // 24

        if horas % 24 != 0:
            dias += 1

        return dias * self.precio_base

    def describir(self):

        return "Equipo: " + self.__tipo


# **********************
# ASESORIA ESPECIALIZADA
# **********************

class AsesoriaEspecializada(Servicio):

    def __init__(self, area, asesor, precio_base):

        super().__init__(area, precio_base)

        self.__area = area
        self.__asesor = asesor

    # POLIMORFISMO
    def calcular_costo(self, horas):

        if self.disponible == False:
            raise ServicioNoDisponibleError(
                "La asesoria no esta disponible"
            )

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores a 0"
            )

        return horas * self.precio_base

    def describir(self):

        return (
            "Area: " + self.__area +
            " | Asesor: " + self.__asesor
        )


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

print("============== SERVICIOS ==============")

# OPERACION 1
print("\nOperacion 1")
sala = ReservaSala(101, 10, 80000)
print(sala.describir())

# OPERACION 2
print("\nOperacion 2")
equipo = AlquilerEquipo("Laptop", 120000)
print(equipo.describir())

# OPERACION 3
print("\nOperacion 3")
asesoria = AsesoriaEspecializada(
    "Sistemas",
    "Carlos",
    150000
)
print(asesoria.describir())

# OPERACION 4
print("\nOperacion 4")
print("Costo sala:", sala.calcular_costo(3))

# OPERACION 5
print("\nOperacion 5")
print("Costo equipo:", equipo.calcular_costo(30))

# OPERACION 6
print("\nOperacion 6")
print("Costo asesoria:", asesoria.calcular_costo(2))

# OPERACION 7
print("\nOperacion 7")

try:
    print(sala.calcular_costo(-5))

except ServicioError as e:
    print("Error:", e)

# OPERACION 8
print("\nOperacion 8")

try:
    equipo.desactivar()
    print(equipo.calcular_costo(10))

except ServicioNoDisponibleError as e:
    print("Error:", e)

# OPERACION 9
print("\nOperacion 9")

servicios = [sala, equipo, asesoria]

for servicio in servicios:
    print(servicio.describir())

# OPERACION 10
print("\nOperacion 10")

extra = ServicioExtra("Servicio Premium", 100000)

print(
    "Con descuento:",
    extra.calcular_descuento(2, 0.10)
)

print(
    "Con IVA:",
    extra.calcular_iva(2)
)