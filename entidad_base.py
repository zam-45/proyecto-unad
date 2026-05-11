#-------------------------------------------------------------------
# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programación (213023)
# Fase 4 - Componente práctico
# Archivo: entidad_base.py
# Descripción:
#   Clase abstracta que representa cualquier entidad del sistema.
#   Define el contrato común que toda entidad debe cumplir.
#   Cumple con el requisito de la guía: "Una clase abstracta que
#   represente entidades generales del sistema."
#-------------------------------------------------------------------

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ClienteInvalidoError


class EntidadBase(ABC):
    """Clase abstracta que representa una entidad genérica del sistema.

    Atributos:
        _id (str): identificador único de la entidad (encapsulado).
        _fecha_creacion (datetime): fecha y hora de creación.
    """

    def __init__(self, identificador):
        # Validación inmediata del identificador para evitar entidades inválidas
        if not identificador or not isinstance(identificador, str):
            raise ClienteInvalidoError("El identificador no puede estar vacío.")
        self._id = identificador
        self._fecha_creacion = datetime.now()

    # Propiedad de solo lectura para el id
    @property
    def id(self):
        return self._id

    # Propiedad de solo lectura para la fecha de creación
    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # Métodos abstractos: cada subclase DEBE implementarlos
    @abstractmethod
    def descripcion(self):
        """Retorna una descripción textual de la entidad."""
        pass

    @abstractmethod
    def validar(self):
        """Valida la integridad de los datos de la entidad."""
        pass
