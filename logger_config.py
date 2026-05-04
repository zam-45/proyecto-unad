# --- ARCHIVO: logger_config.py ---
import logging

# Configuramos el archivo de texto donde se guardará todo
logging.basicConfig(
    filename='registro_errores.txt', 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_evento(mensaje):
    """Función simple para guardar eventos normales (como una reserva exitosa)."""
    logging.info(mensaje)
    print(f"[LOG INFO]: {mensaje}")

def registrar_error(mensaje):
    """Función para guardar cuando algo sale mal (excepciones)."""
    logging.error(mensaje)
    print(f"[LOG ERROR]: {mensaje}")