# Sistema de Cifrado sobre Topología WAN (Equipos Físicos)

**Materia:** Administración y Seguridad de Redes  
**Proyecto:** Transmisión y Descifrado Seguro de Mensajes y Archivos `.txt` sobre Enlace WAN Serial  
**Algoritmos de Cifrado:** César, Vigenère y Vernam (One-Time Pad)  
**Entorno:** 2 Laptops, 2 Switches Cisco Catalyst 2960, 2 Routers Cisco (1941/2811) y Cable Serial V.35

---

## 1. Descripción General del Proyecto

Esta práctica demuestra la interconexión de dos redes de área local independientes (**LAN 1** y **LAN 2**) conectadas mediante dos routers Cisco a través de un **enlace WAN serial físico** (que emula la nube de telecomunicaciones).

Sobre esta infraestructura se ejecuta una aplicación web distribuida en **Python Flask**:
1. **Laptop 1 (Emisor - PC 1):** El usuario escribe un texto o carga un archivo `.txt`, selecciona un algoritmo de cifrado (**César**, **Vigenère** o **Vernam**), introduce la clave $K$ y transmite el paquete cifrado a través de los routers.
2. **Laptop 2 (Receptor - PC 2):** Recibe el paquete cifrado en tiempo real a través del enlace WAN, introduce la clave $K$, descifra el mensaje original y lo exporta a un archivo `.txt` con verificación ✔.

---

## 2. Topología de Red y Direccionamiento IP

```
[ Laptop 1 ] ──(RJ-45)──► [ Switch 1 ] ──(RJ-45)──► [ Router 1 ]
192.168.10.10             Puerto Fa0/1    Puerto Fa0/24  Gig0/0 (192.168.10.1)
                                                               │
                                                 [ CABLE SERIAL V.35 (NUBE WAN) ]
                                                 R1 Se0/0/0 (DCE - Clock: 64000) -> 10.0.0.1/30
                                                 R2 Se0/0/0 (DTE)                -> 10.0.0.2/30
                                                               │
[ Laptop 2 ] ◄──(RJ-45)── [ Switch 2 ] ◄──(RJ-45)── [ Router 2 ]
192.168.20.10             Puerto Fa0/1    Puerto Fa0/24  Gig0/0 (192.168.20.1)
```

### Tabla Maestra de Direccionamiento IP:

| Dispositivo | Interfaz | Dirección IP | Máscara | Gateway | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Laptop 1 (Emisor)** | Adaptador Ethernet | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` | LAN 1 |
| **Router 1 (R1)** | `GigabitEthernet 0/0` | `192.168.10.1` | `255.255.255.0` | N/A | Gateway de LAN 1 |
| **Router 1 (R1)** | `Serial 0/0/0` | `10.0.0.1` | `255.255.255.252` | N/A | Lado DCE (`clock rate 64000`) |
| **Router 2 (R2)** | `Serial 0/0/0` | `10.0.0.2` | `255.255.255.252` | N/A | Lado DTE |
| **Router 2 (R2)** | `GigabitEthernet 0/0` | `192.168.20.1` | `255.255.255.0` | N/A | Gateway de LAN 2 |
| **Laptop 2 (Receptor)** | Adaptador Ethernet | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` | LAN 2 (Puerto 5000) |

---

## 3. Conexiones Físicas (Puerto a Puerto)

| # | Desde (Dispositivo y Puerto) | Hacia (Dispositivo y Puerto) | Tipo de Cable |
| :-: | :--- | :--- | :--- |
| **1** | **Laptop 1** (Puerto RJ-45) | **Switch 1** (`Fa0/1`) | Cable de Red UTP Directo (RJ-45) |
| **2** | **Switch 1** (`Fa0/24`) | **Router 1** (`Gig0/0`) | Cable de Red UTP Directo (RJ-45) |
| **3** | **Router 1** (`Serial0/0/0` - Extremo **DCE**) | **Router 2** (`Serial0/0/0` - Extremo **DTE**) | **Cable Serial V.35 / Smart Serial** |
| **4** | **Router 2** (`Gig0/0`) | **Switch 2** (`Fa0/24`) | Cable de Red UTP Directo (RJ-45) |
| **5** | **Switch 2** (`Fa0/1`) | **Laptop 2** (Puerto RJ-45) | Cable de Red UTP Directo (RJ-45) |

---

## 4. Algoritmos de Cifrado Implementados

1. **Cifrado César (Sustitución Monoalfabética):**  
   Desplaza cada letra del alfabeto un número fijo de posiciones $k$ ($C_i = (P_i + k) \pmod{26}$).
2. **Cifrado Vigenère (Sustitución Polialfabética):**  
   Utiliza una palabra clave periódica para variar el desplazamiento en cada letra ($C_i = (P_i + K_{i \pmod m}) \pmod{26}$).
3. **Cifrado Vernam (One-Time Pad / Flujo XOR):**  
   Aplica la operación lógica binaria XOR ($\oplus$) entre el mensaje y una clave aleatoria de igual longitud ($C_i = P_i \oplus K_i$). La salida se codifica en **Hexadecimal** para garantizar una transmisión íntegra sin caracteres de control por HTTP.

---

## 5. Guía Rápida Paso a Paso para Realizar la Práctica

### Paso 1: Conectar el Hardware
Conecta los cables según la tabla de la Sección 3. Asegúrate de conectar el extremo **DCE** del cable serial en el **Router 1**.

### Paso 2: Configurar los Routers Cisco
Conéctate por cable de consola a cada router y copia los comandos correspondientes:
- Para **Router 1**: copia el contenido de [`network_configs/R1_Router1.txt`](network_configs/R1_Router1.txt)
- Para **Router 2**: copia el contenido de [`network_configs/R2_Router2.txt`](network_configs/R2_Router2.txt)

### Paso 3: Configurar las Laptops en Windows
En cada laptop presiona `Win + R`, escribe `ncpa.cpl` y configura la IP fija en el adaptador Ethernet:
- **Laptop 1:** IP `192.168.10.10` | Máscara `255.255.255.0` | Gateway `192.168.10.1`
- **Laptop 2:** IP `192.168.20.10` | Máscara `255.255.255.0` | Gateway `192.168.20.1`

> [!CAUTION]
> **Paso Crítico en Laptop 2 (Firewall de Windows):**  
> En Laptop 2, presiona `Win + R`, escribe `firewall.cpl` y **desactiva temporalmente el Firewall de Windows Defender** (o permite el puerto TCP 5000) para que reciba las peticiones de Laptop 1.

### Paso 4: Probar Conectividad Física (Ping)
En la consola (`cmd`) de Laptop 1 ejecuta:
```cmd
ping 192.168.20.10
```
Si responde con `4 paquetes recibidos`, el tráfico está atravesando la WAN con éxito.

### Paso 5: Iniciar la Aplicación Web
1. **En Laptop 2 (Receptor):**
   - Haz doble clic en `iniciar_app.bat`.
   - Abre el navegador en: `http://localhost:5000/receiver`.
2. **En Laptop 1 (Emisor):**
   - Haz doble clic en `iniciar_app.bat`.
   - Abre el navegador en: `http://localhost:5000/sender`.
   - En **Destino en la Red**, pulsa el botón `[🏢 Red Física (192.168.20.10)]` (o verifica que tenga `http://192.168.20.10:5000/api/receive`).
   - Escribe el mensaje o sube un `.txt`, elige el cifrado, pon la clave $K$, presiona **Ejecutar Cifrado** y luego **Transmitir a PC 2**.
3. **En Laptop 2:**
   - Aparecerá el paquete recibido en la bandeja.
   - Pulsa **Cargar**, escribe la clave $K$, presiona **Descifrar Mensaje** y descarga el archivo `.txt` descifrado ✔.

---

## 6. Estructura del Proyecto

```
Practica_cifrado/
├── ciphers/                       # Algoritmos criptográficos en Python
│   ├── caesar.py                  # Cifrado César
│   ├── vigenere.py                # Cifrado Vigenère
│   └── vernam.py                  # Cifrado Vernam (OTP con XOR)
├── network_configs/               # Configuraciones Cisco y guía de equipos
│   ├── GUIA_EQUIPOS_REALES.md     # Guía detallada completa paso a paso
│   ├── R1_Router1.txt             # Script CLI para Router 1 (Serial DCE)
│   ├── R2_Router2.txt             # Script CLI para Router 2 (Serial DTE)
│   ├── SW1_Switch1.txt            # Script CLI para Switch 1
│   └── SW2_Switch2.txt            # Script CLI para Switch 2
├── static/                        # Estilos CSS e interactividad JS
│   ├── css/style.css
│   └── js/app.js
├── templates/                     # Vistas web HTML (Flask)
│   ├── index.html                 # Topología interactiva
│   ├── layout.html                # Barra de navegación común
│   ├── sender.html                # Interfaz PC 1 (Emisor)
│   └── receiver.html              # Interfaz PC 2 (Receptor)
├── app.py                         # Servidor web Flask y API REST
├── iniciar_app.bat                # Lanzador de un clic para Windows
├── requirements.txt               # Dependencias de Python (Flask, requests)
└── README.md                      # Documentación oficial del proyecto
```

---

## 7. Explicación técnica del funcionamiento

La práctica separa tres responsabilidades: la red entrega paquetes IP, Flask expone las operaciones HTTP y los módulos de `ciphers/` transforman el contenido. Los routers nunca cifran ni descifran: solo consultan sus rutas y reenvían el tráfico entre las dos LAN.

### Flujo completo PC 1 -> PC 2

1. En `/sender`, el usuario escribe un mensaje o carga un archivo `.txt`.
2. El navegador envía `POST /api/encrypt` con `plaintext`, `algorithm` y `key`.
3. `app.py` selecciona `caesar_encrypt`, `vigenere_encrypt` o `vernam_encrypt` y devuelve el texto cifrado.
4. `POST /api/send-packet` construye un JSON con algoritmo, `ciphertext`, fecha, origen, nombre del archivo y, opcionalmente, `key_shared`.
5. `requests.post()` publica el JSON en `http://192.168.20.10:5000/api/receive`. El sistema operativo usa el gateway `192.168.10.1`, R1 reenvía hacia `10.0.0.2` y R2 entrega el paquete a la LAN 2.
6. PC 2 valida `ciphertext` y lo inserta en `INBOX`, una lista temporal en memoria.
7. `/receiver` consulta `GET /api/inbox` cada 2,5 segundos, muestra los paquetes y permite seleccionar uno.
8. El receptor introduce la clave y el navegador llama a `POST /api/decrypt`.
9. El texto plano se muestra y `POST /api/download-txt` lo devuelve como archivo `text/plain` UTF-8.

La bandeja se pierde al detener Flask y no es una base de datos. `POST /api/inbox/clear` la vacía manualmente.

### API principal

| Método y ruta | Función |
|---|---|
| `GET /`, `GET /sender`, `GET /receiver` | Vistas web |
| `POST /api/encrypt` | Cifra texto plano |
| `POST /api/decrypt` | Descifra texto cifrado |
| `GET /api/generate-key` | Genera una clave según algoritmo y longitud |
| `POST /api/send-packet` | Envía el paquete HTTP desde PC 1 |
| `POST /api/receive` | Recibe y guarda el paquete en PC 2 |
| `GET /api/inbox` | Devuelve la bandeja temporal |
| `POST /api/inbox/clear` | Limpia la bandeja |
| `POST /api/download-txt` | Genera la descarga del texto descifrado |

El servidor se inicia con `host='0.0.0.0'` y puerto `5000`; esto permite conexiones desde la otra laptop. `localhost` solo sirve para acceder desde la misma computadora.

---

## 8. Topología y direccionamiento explicado

PC 1 pertenece a `192.168.10.0/24` y usa R1 como gateway. PC 2 pertenece a `192.168.20.0/24` y usa R2 como gateway. Como ambas redes no son directamente adyacentes, cada router necesita una ruta estática hacia la LAN remota:

- R1: `ip route 192.168.20.0 255.255.255.0 10.0.0.2`.
- R2: `ip route 192.168.10.0 255.255.255.0 10.0.0.1`.

El enlace `10.0.0.0/30` tiene cuatro direcciones: red `10.0.0.0`, R1 `10.0.0.1`, R2 `10.0.0.2` y broadcast `10.0.0.3`. En el montaje físico, R1 es DCE y suministra `clock rate 64000`; R2 es DTE. Los switches trabajan como conexión de capa 2 entre cada laptop y su router.

La vista gráfica muestra una nube Frame Relay con DLCI `102 <-> 201`, útil como representación de una nube en simulador. Los scripts incluidos configuran una conexión serial física directa DCE/DTE, no una nube Frame Relay; ambas representaciones describen el transporte WAN, pero no deben configurarse como si fueran la misma variante.

---

## 9. Cifrados implementados

### César

Convierte la clave a entero y desplaza cada letra, conservando mayúsculas, minúsculas, espacios, números y signos:

```text
C_i = (P_i + k) mod 26
P_i = (C_i - k) mod 26
```

Solo existen 26 desplazamientos, por lo que es un cifrado didáctico y no protege información real. Implementación: [ciphers/caesar.py](ciphers/caesar.py).

### Vigenère

Limpia la clave para conservar letras, la convierte a mayúsculas y la repite sobre las letras del mensaje. Los caracteres no alfabéticos no consumen posiciones de clave:

```text
C_i = (P_i + K_(i mod m)) mod 26
P_i = (C_i - K_(i mod m)) mod 26
```

Una clave corta y repetida sigue siendo vulnerable al análisis de frecuencias. Implementación: [ciphers/vigenere.py](ciphers/vigenere.py).

### Vernam / XOR

Codifica el mensaje y la clave como bytes UTF-8 y aplica XOR byte a byte. El resultado se convierte a hexadecimal para que viaje limpiamente dentro del JSON:

```text
C_i = P_i XOR K_i
P_i = C_i XOR K_i
```

La clave debe ser al menos tan larga como el mensaje. Si falta o es demasiado corta, la API genera una clave con `secrets`. Para que sea un One-Time Pad real, la clave debe ser aleatoria, tener la misma longitud en bytes, mantenerse secreta y no reutilizarse. La opción de adjuntar `key_shared` es útil para la demostración, pero expone la clave a cualquiera que observe el paquete. Implementación: [ciphers/vernam.py](ciphers/vernam.py).

---

## 10. Instalación, comprobación y diagnóstico

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

También se puede ejecutar `iniciar_app.bat`, que crea el entorno virtual si no existe y arranca la aplicación. En PC 2 abrir `http://localhost:5000/receiver`; en PC 1 abrir `http://localhost:5000/sender` y seleccionar como destino `http://192.168.20.10:5000/api/receive`.

Antes de probar HTTP, ejecutar desde PC 1:

```text
ping 192.168.10.1
ping 10.0.0.2
ping 192.168.20.10
```

Si el ping falla, revisar cableado, IP, gateway, `no shutdown`, el `clock rate` del DCE y las rutas estáticas. Si el ping funciona pero no llega el paquete, comprobar que Flask escuche en `0.0.0.0:5000` y que el firewall de PC 2 permita TCP 5000. Es preferible crear una regla de entrada específica en Windows en lugar de desactivar todo el firewall.

Las pruebas se ejecutan desde la raíz:

```powershell
python test_ciphers.py
python test_app_endpoints.py
```

`test_ciphers.py` verifica el ciclo cifrar-descifrar de los tres algoritmos. `test_app_endpoints.py` verifica la API de cifrado, descifrado, recepción, bandeja y descarga.

---

## 11. Archivos más importantes

- [`app.py`](app.py): servidor Flask, vistas, API y bandeja temporal.
- [`ciphers/caesar.py`](ciphers/caesar.py), [`ciphers/vigenere.py`](ciphers/vigenere.py), [`ciphers/vernam.py`](ciphers/vernam.py): implementación criptográfica.
- [`templates/sender.html`](templates/sender.html): captura, cifrado y transmisión desde PC 1.
- [`templates/receiver.html`](templates/receiver.html): consulta, selección, descifrado y descarga en PC 2.
- [`templates/index.html`](templates/index.html): diagrama y direccionamiento de la topología.
- [`network_configs/R1_Router1.txt`](network_configs/R1_Router1.txt) y [`network_configs/R2_Router2.txt`](network_configs/R2_Router2.txt): configuración de los routers.
- [`network_configs/GUIA_EQUIPOS_REALES.md`](network_configs/GUIA_EQUIPOS_REALES.md): montaje físico y alternativas de WAN.
- [`requirements.txt`](requirements.txt) e [`iniciar_app.bat`](iniciar_app.bat): dependencias y arranque en Windows.

## 12. Alcance de seguridad

Es una práctica didáctica, no una aplicación de producción: Flask se ejecuta con `debug=True`, no hay autenticación, el transporte es HTTP sin TLS, la bandeja vive en memoria y la clave puede viajar dentro del JSON. En un sistema real habría que desactivar debug, usar HTTPS, autenticar los endpoints, validar tamaño y nombres de archivo, persistir los mensajes de forma controlada y acordar la clave mediante un canal seguro.

---

## Derechos de autor

&copy; 2026 Diego Lozano Camargo. Todos los derechos reservados.
