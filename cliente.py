#----------------------------------------------
# estudiante: Jesus Armando Fonseca Pardo
# grupo: 443
# programa: programación
# archivo: cliente.py
# descripción: 
# clase cliente que permite registrar y validar
# información basica de un cliente dentro del sistema.
#----------------------------------------------


class Cliente:
    def __init__(self, nombre, documento, correo):
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    def validar(self):
        if self.nombre == "":
            print("El nombre está vacío")

        if not self.documento.isdigit():
            print("El documento debe ser número")

        if "@" not in self.correo:
            print("Correo inválido")

    def mostrar(self):
        return f"Cliente: {self.nombre}, Documento: {self.documento}, Correo: {self.correo}"


# prueba
cliente1 = Cliente("jesus", "12345", "jesus@gmail.com")
cliente1.validar()
print(cliente1.mostrar())