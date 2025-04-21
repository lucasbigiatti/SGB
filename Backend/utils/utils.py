# utils/utils.py

def validar_telefono(telefono):
    if len(telefono) == 10 and telefono.isdigit():
        return True
    return False
