from ciphers import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    vernam_encrypt, vernam_decrypt, generate_vernam_key
)

def test_all():
    print("--- Probando Cifrado César ---")
    msg_caesar = "Hola Mundo! Redes y Seguridad 2026."
    k_caesar = 3
    enc_caesar = caesar_encrypt(msg_caesar, k_caesar)
    dec_caesar = caesar_decrypt(enc_caesar, k_caesar)
    print(f"Original : {msg_caesar}")
    print(f"Cifrado  : {enc_caesar}")
    print(f"Descifrado: {dec_caesar}")
    assert dec_caesar == msg_caesar, "Error en César"
    print("[OK] Cesar OK\n")

    print("--- Probando Cifrado Vigenère ---")
    msg_vig = "Ataque al router por la tarde!"
    k_vig = "CLAVE"
    enc_vig = vigenere_encrypt(msg_vig, k_vig)
    dec_vig = vigenere_decrypt(enc_vig, k_vig)
    print(f"Original : {msg_vig}")
    print(f"Cifrado  : {enc_vig}")
    print(f"Descifrado: {dec_vig}")
    assert dec_vig == msg_vig, "Error en Vigenère"
    print("[OK] Vigenere OK\n")

    print("--- Probando Cifrado Vernam (One-Time Pad XOR) ---")
    msg_vernam = "Mensaje ultrasecreto para PC2"
    k_vernam = generate_vernam_key(len(msg_vernam))
    enc_vernam = vernam_encrypt(msg_vernam, k_vernam)
    dec_vernam = vernam_decrypt(enc_vernam, k_vernam)
    print(f"Original  : {msg_vernam}")
    print(f"Clave Vernam: {k_vernam}")
    print(f"Cifrado(Hex): {enc_vernam}")
    print(f"Descifrado: {dec_vernam}")
    assert dec_vernam == msg_vernam, "Error en Vernam"
    print("[OK] Vernam OK\n")

    print("TODAS LAS PRUEBAS DE CIFRADO PASARON EXITOSAMENTE!")

if __name__ == "__main__":
    test_all()
