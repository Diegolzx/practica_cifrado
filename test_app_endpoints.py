from app import app

def run_integration_tests():
    client = app.test_client()

    print("[*] 1. Probando endpoint /api/encrypt...")
    # Cesar
    res = client.post('/api/encrypt', json={'plaintext': 'Hola Redes', 'algorithm': 'caesar', 'key': '3'})
    assert res.status_code == 200, f"Error en encrypt caesar: {res.data}"
    c_caesar = res.get_json()['ciphertext']
    assert c_caesar == 'Krod Uhghv', f"Ciphertext inesperado: {c_caesar}"
    print("    [OK] Encrypt César correcto.")

    # Vigenere
    res = client.post('/api/encrypt', json={'plaintext': 'Topologia WAN', 'algorithm': 'vigenere', 'key': 'CLAVE'})
    assert res.status_code == 200
    c_vig = res.get_json()['ciphertext']
    print("    [OK] Encrypt Vigenère correcto.")

    # Vernam
    res = client.post('/api/encrypt', json={'plaintext': 'Secreto', 'algorithm': 'vernam', 'key': 'CLAVEDE'})
    assert res.status_code == 200
    c_ver = res.get_json()['ciphertext']
    print("    [OK] Encrypt Vernam correcto.")

    print("\n[*] 2. Probando endpoint /api/decrypt...")
    res_dec = client.post('/api/decrypt', json={'ciphertext': c_caesar, 'algorithm': 'caesar', 'key': '3'})
    assert res_dec.status_code == 200
    assert res_dec.get_json()['plaintext'] == 'Hola Redes'
    print("    [OK] Decrypt César correcto.")

    res_dec_vig = client.post('/api/decrypt', json={'ciphertext': c_vig, 'algorithm': 'vigenere', 'key': 'CLAVE'})
    assert res_dec_vig.status_code == 200
    assert res_dec_vig.get_json()['plaintext'] == 'Topologia WAN'
    print("    [OK] Decrypt Vigenère correcto.")

    res_dec_ver = client.post('/api/decrypt', json={'ciphertext': c_ver, 'algorithm': 'vernam', 'key': 'CLAVEDE'})
    assert res_dec_ver.status_code == 200
    assert res_dec_ver.get_json()['plaintext'] == 'Secreto'
    print("    [OK] Decrypt Vernam correcto.")

    print("\n[*] 3. Probando recepción de red /api/receive en PC 2...")
    res_rx = client.post('/api/receive', json={
        'algorithm': 'caesar',
        'ciphertext': c_caesar,
        'key_shared': '3',
        'file_name': 'prueba.txt'
    })
    assert res_rx.status_code == 200
    print("    [OK] Paquete recibido y almacenado en bandeja de PC 2.")

    print("\n[*] 4. Probando bandeja de entrada /api/inbox...")
    res_inbox = client.get('/api/inbox')
    assert res_inbox.status_code == 200
    msgs = res_inbox.get_json()['messages']
    assert len(msgs) >= 1
    assert msgs[0]['ciphertext'] == c_caesar
    print("    [OK] Bandeja de PC 2 contiene el mensaje esperado.")

    print("\n[*] 5. Probando descarga de archivo .txt...")
    res_dl = client.post('/api/download-txt', json={
        'content': 'Mensaje descifrado exitoso',
        'filename': 'resultado.txt'
    })
    assert res_dl.status_code == 200
    assert b'Mensaje descifrado exitoso' in res_dl.data
    print("    [OK] Descarga de .txt generada correctamente.")

    print("\n[V] TODAS LAS PRUEBAS DE LA APLICACIÓN WEB PASARON CON ÉXITO!")

if __name__ == '__main__':
    run_integration_tests()
