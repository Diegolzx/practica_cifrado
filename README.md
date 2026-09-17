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
- Para **Router 1**: copia el contenido de [`network_configs/R1_Router1.txt`](file:///c:/Users/diego/OneDrive/Documentos/Practica_cifrado/network_configs/R1_Router1.txt)
- Para **Router 2**: copia el contenido de [`network_configs/R2_Router2.txt`](file:///c:/Users/diego/OneDrive/Documentos/Practica_cifrado/network_configs/R2_Router2.txt)

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
