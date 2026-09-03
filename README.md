# Práctica de Administración y Seguridad de Redes: Topología WAN y Cifrado (César, Vigenère, Vernam)

Guía completa y detallada para el montaje de la topología en **Cisco Packet Tracer**, la implementación en **equipos físicos (2 laptops + routers)**, y el funcionamiento de la **aplicación web de cifrado y descifrado**.

---

## 1. Diagrama de la Topología y Modelos Exactos de Equipos

![Topología de Red Detallada](topologia_red_detallada.jpg)

La topología reproduce con exactitud el esquema solicitado:
```
[ PC 1 ] ──(Fa0)──► [ Switch 1 ] ──(Gig0/0)──► [ Router 1 ] ──(Se0/0/0)──► ┌──────────────┐
                                                                           │   NUBE WAN   │
[ PC 2 ] ◄──(Fa0)── [ Switch 2 ] ◄──(Gig0/0)── [ Router 2 ] ◄──(Se0/0/0)── └──────────────┘
```

### Modelos de Dispositivos a Elegir en Cisco Packet Tracer:

| Dispositivo | Modelo en Packet Tracer | Nombre / Rol | Módulos Requeridos |
| :--- | :--- | :--- | :--- |
| **PC 1** | `PC-PT` (End Devices) | `PC1` (Emisor / Laptop 1) | Tarjeta FastEthernet por defecto |
| **Switch 1** | `2960-24TT` (Switches) | `SW1` | 24 puertos FastEthernet + 2 Gigabit |
| **Router 1** | `1941` o `2811` (Routers) | `R1` | **Módulo `HWIC-2T`** (para puertos seriales) |
| **Nube WAN** | `Cloud-PT` (WAN Emulation) | `Nube WAN` | Módulo serial por defecto |
| **Router 2** | `1941` o `2811` (Routers) | `R2` | **Módulo `HWIC-2T`** (para puertos seriales) |
| **Switch 2** | `2960-24TT` (Switches) | `SW2` | 24 puertos FastEthernet + 2 Gigabit |
| **PC 2** | `PC-PT` o `Server-PT` | `PC2` (Receptor / Servidor Web) | Tarjeta FastEthernet por defecto |

> [!IMPORTANT]
> **Cómo agregar puertos Seriales a los Routers 1941 en Packet Tracer:**
> 1. Haz clic sobre el router `R1`.
> 2. En la pestaña **Physical**, localiza el interruptor de encendido (botón verde/negro) y haz clic para **apagar el router**.
> 3. En la lista de módulos a la izquierda, selecciona **`HWIC-2T`**.
> 4. Arrastra la tarjeta a la ranura vacía derecha (`Slot 0`).
> 5. Vuelve a hacer clic en el interruptor para **encender el router**.
> 6. Repite el mismo procedimiento en `R2`.

---

## 2. Tabla Maestra de Direccionamiento IP, Puertos y Cableado

| Dispositivo | Interfaz | Dirección IP | Máscara | Gateway | Tipo de Cable | Conecta a |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PC 1** | `FastEthernet0` | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` | **Directo (Cobre - Negro)** | Switch 1 `Fa0/1` |
| **Switch 1** | `Vlan 1` (Gestión) | `192.168.10.2` | `255.255.255.0` | `192.168.10.1` | **Directo (Cobre - Negro)** | Router 1 `Gig0/0` desde `Fa0/24` |
| **Router 1** | `GigabitEthernet0/0`<br>`Serial0/0/0` | `192.168.10.1`<br>`10.0.0.1` | `255.255.255.0`<br>`255.255.255.252` | N/A<br>N/A | Directo a SW1<br>**Serial DTE (Rojo con reloj)** | Conecta a SW1 `Fa0/24`<br>Conecta a Nube `Serial0` |
| **Nube WAN** | `Serial0`<br>`Serial1` | Frame-Relay<br>Frame-Relay | N/A<br>N/A | N/A<br>N/A | Serial DTE | R1 `Serial0/0/0`<br>R2 `Serial0/0/0` |
| **Router 2** | `Serial0/0/0`<br>`GigabitEthernet0/0` | `10.0.0.2`<br>`192.168.20.1` | `255.255.255.252`<br>`255.255.255.0` | N/A<br>N/A | **Serial DTE (Rojo con reloj)**<br>Directo a SW2 | Conecta a Nube `Serial1`<br>Conecta a SW2 `Fa0/24` |
| **Switch 2** | `Vlan 1` (Gestión) | `192.168.20.2` | `255.255.255.0` | `192.168.20.1` | **Directo (Cobre - Negro)** | Router 2 `Gig0/0` desde `Fa0/24` |
| **PC 2** | `FastEthernet0` | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` | **Directo (Cobre - Negro)** | Switch 2 `Fa0/1` |

---

## 3. Conexiones Interfaz por Interfaz (Paso a Paso)

Este apartado detalla exactamente qué puerto físico se conecta con cuál en toda la topología, el cable que debes seleccionar en Cisco Packet Tracer y el propósito de cada enlace:

```
[PC 1]                     [Switch 1]                  [Router 1]                  [Nube WAN]                  [Router 2]                  [Switch 2]                     [PC 2]
┌─────────┐   Cable Cobre  ┌─────────┐   Cable Cobre   ┌─────────┐   Cable Serial  ┌─────────┐   Cable Serial  ┌─────────┐   Cable Cobre   ┌─────────┐   Cable Cobre    ┌─────────┐
│   Fa0   │───────────────►│ Fa0/1   │                 │ Gig0/0  │                 │ Serial0 │                 │ Serial0 │                 │ Fa0/24  │                  │   Fa0   │
│         │                │  Fa0/24 │────────────────►│         │                 │         │                 │         │                 │   Fa0/1 │─────────────────►│         │
│         │                │         │                 │Se0/0/0  │────────────────►│         │                 │Se0/0/0  │                 │         │                  │         │
└─────────┘                └─────────┘                 └─────────┘                 │ Serial1 │────────────────►│         │                 └─────────┘                  └─────────┘
                                                                                   └─────────┘                 │ Gig0/0  │────────────────►│ Fa0/24  │
                                                                                                               └─────────┘                 └─────────┘
```

### Tabla Resumen de Conexión Puerto a Puerto:

| # | Dispositivo Origen | Interfaz Origen | Dispositivo Destino | Interfaz Destino | Herramienta de Cable en Packet Tracer | Color / Icono en PT |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **PC 1** | `FastEthernet 0` | **Switch 1** | `FastEthernet 0/1` | **Copper Straight-Through** (Directo) | Línea continua **Negra** |
| **2** | **Switch 1** | `FastEthernet 0/24` | **Router 1** | `GigabitEthernet 0/0` | **Copper Straight-Through** (Directo) | Línea continua **Negra** |
| **3** | **Router 1** | `Serial 0/0/0` | **Nube WAN** | `Serial 0` | **Serial DTE** | Línea en zigzag **Roja** con reloj |
| **4** | **Nube WAN** | `Serial 1` | **Router 2** | `Serial 0/0/0` | **Serial DTE** | Línea en zigzag **Roja** con reloj |
| **5** | **Router 2** | `GigabitEthernet 0/0` | **Switch 2** | `FastEthernet 0/24` | **Copper Straight-Through** (Directo) | Línea continua **Negra** |
| **6** | **Switch 2** | `FastEthernet 0/1` | **PC 2** | `FastEthernet 0` | **Copper Straight-Through** (Directo) | Línea continua **Negra** |

---

### Explicación Detallada de Cada Conexión:

#### 1. Conexión PC 1 ➔ Switch 1
- **Cable**: *Copper Straight-Through* (Cable directo de cobre, icono de rayo negro sólido).
- **Puerto en PC 1**: `FastEthernet 0` (la tarjeta de red de la laptop).
- **Puerto en Switch 1**: `FastEthernet 0/1` (puerto de acceso LAN para usuarios).
- **Función**: Da acceso a la PC 1 a la red local 1 (`192.168.10.0/24`).

#### 2. Conexión Switch 1 ➔ Router 1
- **Cable**: *Copper Straight-Through* (Cable directo de cobre).
- **Puerto en Switch 1**: `FastEthernet 0/24` (habitualmente el último puerto del switch se usa como enlace de subida o *uplink*).
- **Puerto en Router 1**: `GigabitEthernet 0/0` (la interfaz que sirve como puerta de enlace de la LAN 1).
- **Función**: Conecta todo el tráfico de la red local 1 con su Gateway predeterminado (`192.168.10.1`).

#### 3. Conexión Router 1 ➔ Nube WAN
- **Cable**: *Serial DTE* (Cable serial, icono de línea roja con reloj).
- **Puerto en Router 1**: `Serial 0/0/0` (proporcionado por la tarjeta `HWIC-2T` instalada en el router).
- **Puerto en Nube WAN (Cloud-PT)**: `Serial 0`.
- **Función**: Es el enlace de salida a la red WAN (`10.0.0.1/30`) hacia el circuito Frame-Relay con DLCI `102`.

#### 4. Conexión Nube WAN ➔ Router 2
- **Cable**: *Serial DTE* (Cable serial rojo).
- **Puerto en Nube WAN (Cloud-PT)**: `Serial 1`.
- **Puerto en Router 2**: `Serial 0/0/0` (tarjeta `HWIC-2T` en R2).
- **Función**: Es el enlace de llegada de la red WAN (`10.0.0.2/30`) desde el circuito Frame-Relay con DLCI `201`.

#### 5. Conexión Router 2 ➔ Switch 2
- **Cable**: *Copper Straight-Through* (Cable directo de cobre).
- **Puerto en Router 2**: `GigabitEthernet 0/0` (puerta de enlace de la LAN 2 con IP `192.168.20.1`).
- **Puerto en Switch 2**: `FastEthernet 0/24` (puerto de enlace de subida *uplink* en SW2).
- **Función**: Entrega los paquetes provenientes de la nube hacia el switch de la red local 2.

#### 6. Conexión Switch 2 ➔ PC 2 (o Server-PT)
- **Cable**: *Copper Straight-Through* (Cable directo de cobre).
- **Puerto en Switch 2**: `FastEthernet 0/1`.
- **Puerto en PC 2 / Server**: `FastEthernet 0` (tarjeta de red con IP `192.168.20.10`).
- **Función**: Entrega los paquetes cifrados recibidos al receptor o servidor web para su descifrado.

---

## 4. Paso a Paso: Cómo Configurar la Nube WAN en Packet Tracer

La nube emula una red WAN de conmutación de paquetes mediante el protocolo **Frame Relay**.

1. Haz clic sobre el dispositivo **`Cloud-PT`**.
2. Ve a la pestaña **`Config`**.
3. **Paso 3.1 - Configurar las Interfaces Seriales**:
   - En el menú izquierdo, bajo **`INTERFACES`**, haz clic en **`Serial0`**:
     - En el campo **`DLCI`**, escribe: `102`
     - En el campo **`Name`**, escribe: `R1-a-R2`
     - Haz clic en el botón **`Add`**.
   - En el menú izquierdo, haz clic en **`Serial1`**:
     - En el campo **`DLCI`**, escribe: `201`
     - En el campo **`Name`**, escribe: `R2-a-R1`
     - Haz clic en el botón **`Add`**.
4. **Paso 3.2 - Crear el Puente Frame Relay**:
   - En el menú izquierdo, bajo **`CONNECTIONS`**, haz clic en **`Frame Relay`**.
   - En el selector de la izquierda (Serial0), elige: `102 R1-a-R2`.
   - En el selector de la derecha (Serial1), elige: `201 R2-a-R1`.
   - Haz clic en el botón **`Add`**.
   - Verás en la tabla la ruta bidireccional: `Serial0: 102 <----> Serial1: 201`.
5. Cierra la ventana de la Nube. ¡La nube WAN está configurada!

---

## 5. Comandos para Routers y Switches

### Router 1 (R1 - Lado Emisor):
Abre `R1` -> pestaña **CLI** y pega:
```ios
enable
configure terminal
hostname R1
no ip domain-lookup

! Interfaz hacia Switch 1 (LAN 1)
interface GigabitEthernet0/0
 description Enlace a LAN 1
 ip address 192.168.10.1 255.255.255.0
 no shutdown
 exit

! Interfaz Serial hacia la Nube WAN
interface Serial0/0/0
 description Enlace WAN hacia Nube Frame-Relay
 ip address 10.0.0.1 255.255.255.252
 encapsulation frame-relay
 frame-relay map ip 10.0.0.2 102 broadcast
 no shutdown
 exit

! Ruta estática para alcanzar la LAN 2 (donde está PC 2)
ip route 192.168.20.0 255.255.255.0 10.0.0.2
end
write memory
```

---

### Router 2 (R2 - Lado Receptor):
Abre `R2` -> pestaña **CLI** y pega:
```ios
enable
configure terminal
hostname R2
no ip domain-lookup

! Interfaz hacia Switch 2 (LAN 2)
interface GigabitEthernet0/0
 description Enlace a LAN 2
 ip address 192.168.20.1 255.255.255.0
 no shutdown
 exit

! Interfaz Serial hacia la Nube WAN
interface Serial0/0/0
 description Enlace WAN hacia Nube Frame-Relay
 ip address 10.0.0.2 255.255.255.252
 encapsulation frame-relay
 frame-relay map ip 10.0.0.1 201 broadcast
 no shutdown
 exit

! Ruta estática para alcanzar la LAN 1 (donde está PC 1)
ip route 192.168.10.0 255.255.255.0 10.0.0.1
end
write memory
```

---

### Switches 1 y 2:
- En **SW1**:
  ```ios
  enable
  configure terminal
  hostname SW1
  interface vlan 1
   ip address 192.168.10.2 255.255.255.0
   no shutdown
   exit
  ip default-gateway 192.168.10.1
  end
  write memory
  ```
- En **SW2**:
  ```ios
  enable
  configure terminal
  hostname SW2
  interface vlan 1
   ip address 192.168.20.2 255.255.255.0
   no shutdown
   exit
  ip default-gateway 192.168.20.1
  end
  write memory
  ```

---

## 6. Verificación de la Red en Packet Tracer

1. En **PC 1**, abre `Desktop` -> `Command Prompt`:
   ```cmd
   ping 192.168.20.10
   ```
   *(Debe responder `Reply from 192.168.20.10: bytes=32...`)*.
2. Ejecuta una traza para verificar los saltos por la nube:
   ```cmd
   tracert 192.168.20.10
   ```
   **Saltos visibles**:
   - Salto 1: `192.168.10.1` (Router 1)
   - Salto 2: `10.0.0.2` (Router 2 al cruzar la Nube WAN)
   - Salto 3: `192.168.20.10` (PC 2 de destino)

---

## 7. Cómo Mostrar la Página Web DENTRO de Cisco Packet Tracer

En Packet Tracer puedes demostrar la página web funcionando en la red simulada usando el servicio HTTP integrado:

### Paso 7.1: En PC 2 (o reemplazando PC 2 por un `Server-PT`)
1. Si usas un **`Server-PT`** en lugar de PC 2 con IP `192.168.20.10`:
   - Haz clic en el servidor -> pestaña **`Services`** -> opción **`HTTP`**.
   - Asegúrate de que el servicio **HTTP** esté en **`On`**.
   - Busca el archivo `index.html`, haz clic en **`edit`**.
   - Borra el contenido existente y **pega todo el código de [`packet_tracer_web/index.html`](packet_tracer_web/index.html)**.
   - Haz clic en **`Save`** y confirma el reemplazo (**Yes**).

### Paso 7.2: Abrir la Web desde PC 1 en Packet Tracer
1. Haz clic en **`PC 1`**.
2. Ve a la pestaña **`Desktop`** y abre **`Web Browser`**.
3. En la barra de direcciones URL escribe:
   ```
   http://192.168.20.10
   ```
   y presiona el botón **`Go`**.
4. Se cargará la página web de cifrado **directamente en el navegador de Packet Tracer**:
   - Puedes escribir un mensaje en **PC 1**.
   - Elegir **César**, **Vigenère** o **Vernam**.
   - Ingresar la clave `K`.
   - Presionar **"Ejecutar Cifrado"**.
   - Ingresar la clave en la sección de PC 2, presionar **"Descifrar Mensaje"** y exportar el archivo `.txt` descifrado con la palomita &#10004;.

---

## 8. Cómo Montar el Proyecto con Equipos Físicos Reales (2 Laptops + Routers)

Cuando lleves el proyecto al laboratorio con **routers, switches y laptops reales**, sigue estos pasos (también tienes la guía extendida en [`network_configs/GUIA_EQUIPOS_REALES.md`](network_configs/GUIA_EQUIPOS_REALES.md)):

### 8.1 ¿Cómo se hace la "Nube" en la vida real?
En un laboratorio físico no hay una nube de internet flotante. La "Nube WAN" entre Router 1 y Router 2 se hace de una de estas dos formas según lo que tenga tu laboratorio:
- **Opción A (Cable Serial V.35 / Smart Serial DCE-DTE)**: Se conectan `R1` y `R2` con un cable serial. El extremo del cable marcado como **DCE** se conecta en R1 y se le configura `clock rate 64000` (este extremo simula el reloj del proveedor de la nube).
- **Opción B (Cable Ethernet Directo RJ-45)**: En routers modernos sin puertos seriales, se conecta un cable de red de `GigabitEthernet 0/1` de R1 a `GigabitEthernet 0/1` de R2, asignando la subred WAN `10.0.0.0/30`.

> Los scripts listos para copiar y pegar en consola están en:
> - [`network_configs/R1_Router1_FISICO.txt`](network_configs/R1_Router1_FISICO.txt)
> - [`network_configs/R2_Router2_FISICO.txt`](network_configs/R2_Router2_FISICO.txt)

---

### 8.2 Configuración de las 2 Laptops en Windows (Paso a Paso)

En cada laptop presiona `Win + R`, escribe `ncpa.cpl`, clic derecho en **Ethernet** ➔ **Propiedades** ➔ **TCP/IPv4**:

1. **Laptop 1 (Emisor - Conectada a Switch 1 puerto Fa0/1)**:
   - IP: `192.168.10.10`
   - Máscara: `255.255.255.0`
   - Puerta de enlace: `192.168.10.1`
2. **Laptop 2 (Receptor - Conectada a Switch 2 puerto Fa0/1)**:
   - IP: `192.168.20.10`
   - Máscara: `255.255.255.0`
   - Puerta de enlace: `192.168.20.1`

> [!CAUTION]
> **Paso Crítico en Laptop 2 (Firewall de Windows):**
> Por defecto Windows bloquea conexiones entrantes de otras subredes en el puerto 5000. En **Laptop 2**, abre `firewall.cpl` y desactiva temporalmente el Firewall de Windows Defender para redes privadas, o agrega una excepción para el puerto TCP `5000`.

---

### 8.3 Ejecución de la Aplicación Web entre las 2 Laptops

1. **En Laptop 2 (Receptor)**:
   - Inicia la app con `iniciar_app.bat` (o `python app.py`).
   - Abre el navegador en: `http://localhost:5000/receiver`.
   - Se queda escuchando paquetes en tiempo real en la bandeja de entrada.
2. **En Laptop 1 (Emisor)**:
   - Inicia la app con `iniciar_app.bat` y abre `http://localhost:5000/sender`.
   - En el campo **"Destino en la Red"** escribe:
     `http://192.168.20.10:5000/api/receive`
   - Escribe el mensaje o carga un archivo `.txt`, elige **César**, **Vigenère** o **Vernam**, ingresa la clave $K$, presiona **"Ejecutar Cifrado"** y luego **"Transmitir a PC 2 (Topología WAN)"**.
3. **En Laptop 2**:
   - ¡Aparecerá inmediatamente el mensaje cifrado que viajó por los cables y routers!
   - Presionas **Cargar**, introduces la clave $K$, le das a **"Descifrar Mensaje"** y finalmente **"Descargar Archivo .txt (Descifrado) ✔"**.

---

## 9. Algoritmos de Cifrado Explicados

1. **Cifrado César**:
   - Desplaza cada letra $k$ posiciones en el abecedario: $C_i = (P_i + k) \pmod{26}$.
   - Conserva mayúsculas, minúsculas y caracteres de puntuación.
2. **Cifrado Vigenère**:
   - Aplica sustitución polialfabética sumando periódicamente los caracteres de una palabra clave:
     $$C_i = (P_i + K_{i \pmod m}) \pmod{26}$$
3. **Cifrado Vernam (One-Time Pad)**:
   - Aplica la operación lógica XOR bit a bit entre el mensaje y una clave de igual longitud:
     $$C_i = P_i \oplus K_i$$
   - Se representa en formato **Hexadecimal** para garantizar que los bytes no imprimibles viajen íntegros por la red.
