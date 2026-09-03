import os
import time
import requests
from flask import Flask, render_template, request, jsonify, send_file, Response
import io

from ciphers import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    vernam_encrypt, vernam_decrypt, generate_vernam_key
)

app = Flask(__name__)

# Almacenamiento en memoria para mensajes recibidos (Bandeja de entrada de PC 2)
INBOX = []

@app.route('/')
def index():
    """Vista principal con selector de rol (Emisor, Receptor, o Simulador Completo)."""
    return render_template('index.html')

@app.route('/sender')
def sender_view():
    """Interfaz para PC 1 (Emisor)."""
    return render_template('sender.html')

@app.route('/receiver')
def receiver_view():
    """Interfaz para PC 2 (Receptor)."""
    return render_template('receiver.html')

# ==============================================================================
# ENDPOINTS DE CIFRADO Y DESCIFRADO
# ==============================================================================

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.get_json() or {}
    plaintext = data.get('plaintext', '')
    algorithm = data.get('algorithm', 'caesar').lower()
    key = data.get('key', '')

    if not plaintext:
        return jsonify({'success': False, 'error': 'El texto plano no puede estar vacío.'}), 400

    try:
        if algorithm == 'caesar':
            ciphertext = caesar_encrypt(plaintext, key)
        elif algorithm == 'vigenere':
            ciphertext = vigenere_encrypt(plaintext, key)
        elif algorithm == 'vernam':
            if not key or len(key) < len(plaintext):
                key = generate_vernam_key(len(plaintext))
            ciphertext = vernam_encrypt(plaintext, key)
        else:
            return jsonify({'success': False, 'error': f'Algoritmo desconocido: {algorithm}'}), 400

        return jsonify({
            'success': True,
            'algorithm': algorithm,
            'key': key,
            'ciphertext': ciphertext,
            'length': len(plaintext)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.get_json() or {}
    ciphertext = data.get('ciphertext', '')
    algorithm = data.get('algorithm', 'caesar').lower()
    key = data.get('key', '')

    if not ciphertext:
        return jsonify({'success': False, 'error': 'El texto cifrado no puede estar vacío.'}), 400

    try:
        if algorithm == 'caesar':
            plaintext = caesar_decrypt(ciphertext, key)
        elif algorithm == 'vigenere':
            plaintext = vigenere_decrypt(ciphertext, key)
        elif algorithm == 'vernam':
            plaintext = vernam_decrypt(ciphertext, key)
        else:
            return jsonify({'success': False, 'error': f'Algoritmo desconocido: {algorithm}'}), 400

        return jsonify({
            'success': True,
            'algorithm': algorithm,
            'key': key,
            'plaintext': plaintext
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/generate-key', methods=['GET'])
def api_generate_key():
    length = int(request.args.get('length', 16))
    algo = request.args.get('algorithm', 'vernam').lower()
    if algo == 'vernam':
        key = generate_vernam_key(max(1, length))
    elif algo == 'caesar':
        import random
        key = str(random.randint(1, 25))
    elif algo == 'vigenere':
        import random, string
        key = "".join(random.choice(string.ascii_uppercase) for _ in range(max(4, min(10, length))))
    else:
        key = ""
    return jsonify({'success': True, 'key': key})


# ==============================================================================
# ENDPOINTS DE TRANSMISIÓN DE RED (PC1 -> Red -> PC2)
# ==============================================================================

@app.route('/api/send-packet', methods=['POST'])
def api_send_packet():
    """
    Se ejecuta en PC 1 (Emisor):
    Toma el payload cifrado y lo envía vía HTTP POST al endpoint /api/receive de PC 2.
    """
    data = request.get_json() or {}
    target_url = data.get('target_url', 'http://192.168.20.10:5000/api/receive')
    
    payload = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'source_ip': request.remote_addr,
        'algorithm': data.get('algorithm', 'caesar'),
        'ciphertext': data.get('ciphertext', ''),
        'key_shared': data.get('key_shared', ''),  # Opcional si se comparte clave o se mantiene secreta
        'file_name': data.get('file_name', 'mensaje.txt'),
        'notes': data.get('notes', 'Paquete cifrado transmitido a traves de la topologia WAN')
    }

    if not payload['ciphertext']:
        return jsonify({'success': False, 'error': 'No hay datos cifrados para enviar.'}), 400

    try:
        # Enviar petición HTTP POST a través de los routers y la nube
        start_t = time.time()
        resp = requests.post(target_url, json=payload, timeout=8)
        elapsed_ms = round((time.time() - start_t) * 1000, 2)

        if resp.status_code == 200:
            return jsonify({
                'success': True,
                'message': f'Paquete enviado exitosamente a {target_url}',
                'latency_ms': elapsed_ms,
                'target_response': resp.json() if resp.headers.get('content-type') == 'application/json' else resp.text
            })
        else:
            return jsonify({
                'success': False,
                'error': f'PC 2 respondió con código de estado HTTP {resp.status_code}: {resp.text}'
            }), 502
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': f'No se pudo conectar con PC 2 en {target_url}. Verifica que PC 2 tenga el servidor activo, las IPs estén bien configuradas y el enrutamiento funcione.'
        }), 504
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/receive', methods=['POST'])
def api_receive():
    """
    Se ejecuta en PC 2 (Receptor):
    Recibe el paquete que viajó por la red y lo almacena en la bandeja de entrada.
    """
    data = request.get_json() or {}
    if not data or 'ciphertext' not in data:
        return jsonify({'success': False, 'error': 'Payload inválido.'}), 400

    message_item = {
        'id': len(INBOX) + 1,
        'received_at': time.strftime('%H:%M:%S'),
        'source_ip': request.remote_addr,
        'algorithm': data.get('algorithm', 'Desconocido'),
        'ciphertext': data.get('ciphertext', ''),
        'key_shared': data.get('key_shared', ''),
        'file_name': data.get('file_name', 'mensaje.txt'),
        'notes': data.get('notes', '')
    }

    INBOX.insert(0, message_item)
    return jsonify({
        'success': True,
        'message': 'Mensaje recibido exitosamente en PC 2',
        'item_id': message_item['id']
    })


@app.route('/api/inbox', methods=['GET'])
def api_inbox():
    """Retorna los mensajes recibidos en PC 2."""
    return jsonify({'success': True, 'messages': INBOX})


@app.route('/api/inbox/clear', methods=['POST'])
def api_clear_inbox():
    """Limpia la bandeja de entrada de PC 2."""
    global INBOX
    INBOX = []
    return jsonify({'success': True, 'message': 'Bandeja limpiada correctamente.'})


@app.route('/api/download-txt', methods=['POST'])
def api_download_txt():
    """Permite descargar el mensaje descifrado como archivo .txt."""
    data = request.get_json() or {}
    content = data.get('content', '')
    filename = data.get('filename', 'mensaje_descifrado.txt')
    if not filename.endswith('.txt'):
        filename += '.txt'

    buffer = io.BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )


if __name__ == '__main__':
    # Escucha en todas las interfaces de red (0.0.0.0) en el puerto 5000
    # para que la otra PC o los routers puedan enrutar el tráfico hasta él.
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] Iniciando servidor de Práctica de Cifrado en http://0.0.0.0:{port}")
    print(f"[*] Para Emisor (PC 1): http://localhost:{port}/sender")
    print(f"[*] Para Receptor (PC 2): http://localhost:{port}/receiver")
    app.run(host='0.0.0.0', port=port, debug=True)
