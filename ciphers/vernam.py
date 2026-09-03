"""
Módulo de Cifrado y Descifrado Vernam (One-Time Pad).
Aplica la operación XOR bit a bit entre los caracteres del texto y la clave.
Para asegurar la transmisión limpia por la red y exportación a .txt,
el resultado cifrado se codifica en formato Hexadecimal.
"""
import secrets
import string

def generate_vernam_key(length: int) -> str:
    """Genera una clave aleatoria segura de longitud 'length'."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def vernam_encrypt(plaintext: str, key: str) -> str:
    """
    Cifra el texto plano usando la clave Vernam mediante operación XOR.
    Retorna una cadena hexadecimal representativa del ciphertext.
    """
    if not key:
        raise ValueError("La clave para Vernam no puede estar vacía.")

    if len(key) < len(plaintext):
        raise ValueError(
            f"Para el cifrado Vernam (One-Time Pad), la clave debe tener al menos la misma "
            f"longitud que el mensaje (Mensaje: {len(plaintext)} caracteres, Clave: {len(key)})."
        )

    # XOR entre los códigos de caracteres UTF-8/ASCII
    p_bytes = plaintext.encode('utf-8')
    k_bytes = key[:len(plaintext)].encode('utf-8')

    cipher_bytes = bytes([p ^ k for p, k in zip(p_bytes, k_bytes)])
    return cipher_bytes.hex()

def vernam_decrypt(ciphertext_hex: str, key: str) -> str:
    """
    Descifra un texto cifrado en hexadecimal usando la clave Vernam mediante XOR.
    """
    if not key:
        raise ValueError("La clave para Vernam no puede estar vacía.")

    try:
        cipher_bytes = bytes.fromhex(ciphertext_hex.strip())
    except ValueError:
        raise ValueError("El texto cifrado de Vernam debe ser una cadena hexadecimal válida.")

    if len(key.encode('utf-8')) < len(cipher_bytes):
        raise ValueError(
            f"La longitud de la clave ({len(key)}) es menor que la longitud del mensaje cifrado ({len(cipher_bytes)})."
        )

    k_bytes = key.encode('utf-8')[:len(cipher_bytes)]
    plain_bytes = bytes([c ^ k for c, k in zip(cipher_bytes, k_bytes)])

    try:
        return plain_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # En caso de caracteres directos
        return plain_bytes.decode('latin-1')
