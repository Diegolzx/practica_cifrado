"""
Módulo de Cifrado y Descifrado César.
Permite desplazar caracteres alfabéticos conservando mayúsculas, minúsculas
y preservando caracteres especiales y espacios.
"""

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Cifra un texto plano utilizando el cifrado César con desplazamiento k.
    """
    try:
        shift = int(shift) % 26
    except (ValueError, TypeError):
        raise ValueError("La clave para el cifrado César debe ser un número entero.")

    result = []
    for char in plaintext:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    Descifra un texto cifrado con César aplicando el desplazamiento inverso (-k).
    """
    try:
        shift = int(shift) % 26
    except (ValueError, TypeError):
        raise ValueError("La clave para el cifrado César debe ser un número entero.")
    return caesar_encrypt(ciphertext, -shift)
