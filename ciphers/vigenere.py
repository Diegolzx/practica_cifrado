"""
Módulo de Cifrado y Descifrado Vigenère.
Aplica sustitución polialfabética usando una palabra clave repetida.
"""

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Cifra un texto plano utilizando el cifrado Vigenère con la clave proporcionada.
    """
    clean_key = "".join([c for c in key if c.isalpha()]).upper()
    if not clean_key:
        raise ValueError("La clave para Vigenère debe contener al menos una letra del alfabeto.")

    result = []
    key_index = 0
    key_len = len(clean_key)

    for char in plaintext:
        if 'A' <= char <= 'Z':
            shift = ord(clean_key[key_index % key_len]) - ord('A')
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            key_index += 1
        elif 'a' <= char <= 'z':
            shift = ord(clean_key[key_index % key_len]) - ord('A')
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
            
    return "".join(result)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Descifra un texto cifrado con Vigenère usando la clave proporcionada.
    """
    clean_key = "".join([c for c in key if c.isalpha()]).upper()
    if not clean_key:
        raise ValueError("La clave para Vigenère debe contener al menos una letra del alfabeto.")

    result = []
    key_index = 0
    key_len = len(clean_key)

    for char in ciphertext:
        if 'A' <= char <= 'Z':
            shift = ord(clean_key[key_index % key_len]) - ord('A')
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            key_index += 1
        elif 'a' <= char <= 'z':
            shift = ord(clean_key[key_index % key_len]) - ord('A')
            result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
            
    return "".join(result)
