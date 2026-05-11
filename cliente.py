#----------------------------------------------
# estudiante: Jesus Armando Fonseca Pardo
# (mejoras de validación y excepciones agregadas
#  por el equipo durante la integración)
# grupo: 443
# programa: programación
# archivo: cliente.py
# descripción:
#   Clase Cliente que permite registrar y validar
#   información básica de un cliente dentro del sistema,
#   con manejo robusto de excepciones personalizadas
#   y encapsulación de datos.
#----------------------------------------------

import re
from entidad_base import EntidadBase
from excepciones import ClienteInvalidoError
from logger_config import registrar_evento, registrar_error


class Cliente(EntidadBase):
    """Cliente registrado en el sistema Software FJ.

    Hereda de EntidadBase y aplica encapsulación con properties.
    Lanza ClienteInvalidoError cuando los datos no cumplen las reglas.
    """

    # Patrones de validación (expresiones regulares)
    _PATRON_CORREO = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")

    def __init__(self, nombre, documento, correo):
        # Generamos un identificador automático con el documento
        super().__init__(f"CLI-{documento}")
        # Usamos los setters para forzar las validaciones
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        registrar_evento(
            f"Cliente creado: {self.__nombre} (doc {self.__documento})")

    # --------- Encapsulación: getters y setters ---------

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre no puede estar vacío y debe tener al menos 3 caracteres
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # El documento debe ser numérico
        if not str(valor).isdigit():
            raise ClienteInvalidoError(
                f"El documento debe contener solo números (recibido: {valor}).")
        if not (6 <= len(str(valor)) <= 12):
            raise ClienteInvalidoError(
                "El documento debe tener entre 6 y 12 dígitos.")
        self.__documento = str(valor)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # El correo debe tener formato válido
        if not self._PATRON_CORREO.match(str(valor)):
            raise ClienteInvalidoError(
                f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor

    # --------- Métodos requeridos por EntidadBase ---------

    def descripcion(self):
        """Devuelve una descripción legible del cliente."""
        return (f"Cliente[{self._id}] {self.__nombre} | "
                f"Doc: {self.__documento} | Correo: {self.__correo}")

    def validar(self):
        """Verifica que los campos del cliente sean coherentes."""
        return bool(self.__nombre and self.__documento and self.__correo)

    def mostrar(self):
        """Método original de Jesús, mantenido para compatibilidad."""
        return (f"Cliente: {self.__nombre}, "
                f"Documento: {self.__documento}, "
                f"Correo: {self.__correo}")


# --------- Bloque de prueba (solo se ejecuta si corres este archivo) ---------
if __name__ == "__main__":
    try:
        # Prueba con datos válidos
        cliente1 = Cliente("Jesús Armando Fonseca", "12345678", "jesus@gmail.com")
        print(cliente1.mostrar())
    except ClienteInvalidoError as e:
        registrar_error(str(e))
        print(f"Error: {e}")
