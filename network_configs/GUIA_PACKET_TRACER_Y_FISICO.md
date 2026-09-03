# Guía Completa de Configuración de Red: Packet Tracer y Equipos Físicos

Esta guía describe paso a paso cómo montar la topología mostrada en el pizarrón:
`PC1` <---> `Switch 1` <---> `Router 1` <---> `[ Nube WAN ]` <---> `Router 2` <---> `Switch 2` <---> `PC2`

---

## 1. Tabla de Direccionamiento IP y Conexiones Físicas

| Dispositivo | Interfaz | Dirección IP | Máscara | Gateway | Cable / Conexión |
|:---|:---|:---|:---|:---|:---|
| **PC 1 (Laptop 1)** | `Ethernet` | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` | Directo (Cobre) a Switch 1 `Fa0/1` |
| **Switch 1** | `Vlan 1` | `192.168.10.2` | `255.255.255.0` | `192.168.10.1` | Directo a R1 `Gig0/0` desde `Fa0/24` |
| **Router 1 (R1)** | `Gig0/0` (LAN) | `192.168.10.1` | `255.255.255.0` | N/A | Directo a Switch 1 |
| **Router 1 (R1)** | `Serial0/0/0` (WAN) | `10.0.0.1` | `255.255.255.252` | N/A | Serial DTE a Nube `Serial0` |
| **Nube WAN (Cloud-PT)**| `Serial0` / `Serial1`| Frame-Relay | N/A | N/A | Serial DTE a R1 y R2 |
| **Router 2 (R2)** | `Serial0/0/0` (WAN) | `10.0.0.2` | `255.255.255.252` | N/A | Serial DTE a Nube `Serial1` |
| **Router 2 (R2)** | `Gig0/0` (LAN) | `192.168.20.1` | `255.255.255.0` | N/A | Directo a Switch 2 |
| **Switch 2** | `Vlan 1` | `192.168.20.2` | `255.255.255.0` | `192.168.20.1` | Directo a R2 `Gig0/0` desde `Fa0/24` |
| **PC 2 (Laptop 2)** | `Ethernet` | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` | Directo (Cobre) a Switch 2 `Fa0/1` |

---

## 2. Instrucciones para Cisco Packet Tracer

### Paso 2.1: Colocar los dispositivos
1. Agrega **2 PCs** (PC-PT).
2. Agrega **2 Switches** modelo `2960`.
3. Agrega **2 Routers** modelo `1941` o `2811`.
   - *Importante*: Antes de conectar cables seriales, haz clic en cada Router -> pestaña **Physical** -> apaga el interruptor de encendido -> arrastra el módulo `HWIC-2T` o `WIC-2T` a una ranura libre -> vuelve a encender el Router.
4. Agrega **1 Nube** (`Cloud-PT` en el apartado de emulaciones WAN).

### Paso 2.2: Conectar el cableado
- **Cables Directos de Cobre (Rayo negro continuo)**:
  - De `PC 1` (FastEthernet0) a `Switch 1` (FastEthernet0/1).
  - De `Switch 1` (FastEthernet0/24) a `Router 1` (GigabitEthernet0/0).
  - De `Router 2` (GigabitEthernet0/0) a `Switch 2` (FastEthernet0/24).
  - De `Switch 2` (FastEthernet0/1) a `PC 2` (FastEthernet0).
- **Cables Seriales (Rayo rojo con reloj)**:
  - De `Router 1` (Serial0/0/0) a `Cloud-PT` (Serial0).
  - De `Cloud-PT` (Serial1) a `Router 2` (Serial0/0/0).

### Paso 2.3: Configurar la Nube WAN (Cloud-PT)
1. Haz clic en la **Cloud-PT** y ve a la pestaña **Config**.
2. En el menú de la izquierda, bajo **INTERFACES**:
   - Clic en **Serial0**:
     - DLCI: `102`
     - Name: `R1-a-R2`
     - Clic en **Add**.
   - Clic en **Serial1**:
     - DLCI: `201`
     - Name: `R2-a-R1`
     - Clic en **Add**.
3. En el menú de la izquierda, bajo **CONNECTIONS**:
   - Clic en **Frame Relay**:
     - Serial0: Selecciona `102 R1-a-R2`.
     - Serial1: Selecciona `201 R2-a-R1`.
     - Clic en el botón **Add** (verás aparecer la ruta bidireccional `Serial0: 102 <-> Serial1: 201`).

### Paso 2.4: Aplicar comandos en R1 y R2
- Abre la pestaña **CLI** de `Router 1` y pega el contenido del archivo `network_configs/R1_Router1.txt`.
- Abre la pestaña **CLI** de `Router 2` y pega el contenido del archivo `network_configs/R2_Router2.txt`.

### Paso 2.5: Configurar IP en PC 1 y PC 2 en Packet Tracer
- **PC 1**: Clic en PC 1 -> Desktop -> IP Configuration:
  - IP Address: `192.168.10.10`
  - Subnet Mask: `255.255.255.0`
  - Default Gateway: `192.168.10.1`
- **PC 2**: Clic en PC 2 -> Desktop -> IP Configuration:
  - IP Address: `192.168.20.10`
  - Subnet Mask: `255.255.255.0`
  - Default Gateway: `192.168.20.1`

### Paso 2.6: Comprobación de Conectividad
En PC 1 abre `Command Prompt` y ejecuta:
```cmd
ping 192.168.20.10
```
*(El primer o segundo paquete puede perderse por ARP; si repites el comando debe dar 4/4 recibidos).*
Luego ejecuta:
```cmd
tracert 192.168.20.10
```
Verás los saltos:
1. `192.168.10.1` (Gateway R1)
2. `10.0.0.2` (R2 cruzando la Nube)
3. `192.168.20.10` (PC 2 de destino)

---

## 3. Instrucciones para Equipos Físicos (2 Laptops + Routers Reales)

Cuando vayas a implementar la práctica con equipos reales en tu laboratorio:

### 3.1 Configuración de las Laptops en Windows
En cada Laptop:
1. Presiona `Win + R`, escribe `ncpa.cpl` y presiona Enter.
2. Clic derecho en el adaptador Ethernet -> **Propiedades**.
3. Selecciona **Protocolo de Internet versión 4 (TCP/IPv4)** -> **Propiedades**.
4. Selecciona *"Usar la siguiente dirección IP"*:
   - **En Laptop 1**:
     - IP: `192.168.10.10`
     - Máscara: `255.255.255.0`
     - Puerta de enlace: `192.168.10.1`
   - **En Laptop 2**:
     - IP: `192.168.20.10`
     - Máscara: `255.255.255.0`
     - Puerta de enlace: `192.168.20.1`
5. **Importante (Firewall de Windows)**:
   - En Windows Defender Firewall, permite el puerto `5000` (TCP) o desactiva temporalmente el firewall de la red privada para que el servidor Flask reciba las peticiones HTTP entre ambas laptops.

### 3.2 Conexión WAN entre Routers Físicos
- En laboratorios físicos, los routers suelen conectarse directamente con un cable serial V.35 (DCE/DTE) o con un cable Ethernet Gigabit directo entre R1 y R2 si no hay conmutador Frame-Relay físico.
- Si se conectan directamente por cable Serial, en el router que tenga el extremo DCE se debe configurar `clock rate 64000`.
- Si se conectan con cable Ethernet directo entre `Gig0/1` de R1 y `Gig0/1` de R2, la subred `10.0.0.0/30` se configura en esas interfaces Ethernet en lugar del Serial.
