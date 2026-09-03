# Guía Definitiva: Montaje con Equipos Físicos Reales (2 Laptops, 2 Routers, 2 Switches)

Esta guía explica detalladamente cómo implementar la práctica con **equipos físicos en el laboratorio**, cómo resolver el tema de **la nube en la vida real**, la configuración de las **2 laptops en Windows** y la ejecución de la **aplicación web**.

---

## 1. ¿Cómo se hace la "Nube" en Equipos Físicos Reales?

En un simulador como Packet Tracer existe un objeto virtual llamado `Cloud-PT`. Sin embargo, en un laboratorio físico de redes **no existe una nube flotante de internet**. En las universidades, la "nube WAN" entre dos routers se representa físicamente de una de estas dos formas (pregunta a tu profesor cuál de las dos tienen disponible en su laboratorio):

### Opción 1: Mediante Cable Serial V.35 / Smart Serial (DCE a DTE) [La más clásica]
Si los routers físicos tienen tarjetas seriales (`WIC-2T` o `HWIC-2T`):
- Se conectan ambos routers directamente con un **cable serial físico**.
- El cable físico tiene dos extremos: un conector macho y uno hembra (o están etiquetados como **DCE** y **DTE**).
- El extremo **DCE** simula ser la "empresa proveedora de la nube" (ISP) y es el que proporciona la señal de reloj (*clock rate*).
- En el router donde conectes el extremo DCE (por ejemplo R1), se debe agregar el comando:
  ```ios
  clock rate 64000
  ```
- La encapsulación puede ser `encapsulation hdlc` o `encapsulation ppp`.

### Opción 2: Mediante Cable Ethernet Directo Gigabit (R1 Gig0/1 ➔ R2 Gig0/1) [La más moderna]
Muchos routers modernos de laboratorio (Cisco 1941, 2901, 2911, 4321) ya no usan puertos seriales porque son tecnologías antiguas.
- En su lugar, se usa un **cable de red Ethernet (RJ-45 normal)** conectado directamente de `GigabitEthernet 0/1` de Router 1 a `GigabitEthernet 0/1` de Router 2.
- A ese enlace entre routers se le asigna la subred WAN `10.0.0.0/30`:
  - R1 `Gig0/1`: `10.0.0.1 255.255.255.252`
  - R2 `Gig0/1`: `10.0.0.2 255.255.255.252`
- ¡Esta conexión directa entre routers representa exactamente el enlace de transporte WAN / Nube!

---

## 2. Mapa Físico de Conexión de Cables

```
[ Laptop 1 ] ──(Cable RJ-45)──► [ Switch 1 ] ──(Cable RJ-45)──► [ Router 1 ]
(192.168.10.10)                 (Puerto Fa0/1)  (Puerto Fa0/24)  (Gig0/0 LAN: 192.168.10.1)
                                                                        │
                                                                   [ ENLACE WAN / NUBE ]
                                                                   (Serial o Gig0/1 directo)
                                                                   (Red: 10.0.0.0/30)
                                                                        │
[ Laptop 2 ] ◄──(Cable RJ-45)── [ Switch 2 ] ◄──(Cable RJ-45)── [ Router 2 ]
(192.168.20.10:5000)            (Puerto Fa0/1)  (Puerto Fa0/24)  (Gig0/0 LAN: 192.168.20.1)
```

### Tabla de Conexiones Físicas:
1. **Laptop 1** (puerto Ethernet) con cable RJ-45 a **Switch 1** (puerto `Fa0/1`).
2. **Switch 1** (puerto `Fa0/24`) con cable RJ-45 a **Router 1** (puerto `Gig0/0`).
3. **Router 1** hacia **Router 2** (La Nube WAN):
   - *Si usan Serial*: Cable serial desde `Serial0/0/0` de R1 hacia `Serial0/0/0` de R2.
   - *Si usan Ethernet*: Cable RJ-45 desde `Gig0/1` de R1 hacia `Gig0/1` de R2.
4. **Router 2** (puerto `Gig0/0`) con cable RJ-45 a **Switch 2** (puerto `Fa0/24`).
5. **Switch 2** (puerto `Fa0/1`) con cable RJ-45 a **Laptop 2** (puerto Ethernet).

---

## 3. Comandos CLI para los Routers Físicos

### Configuración de Router 1 (R1):
Conecta tu cable de consola (azul claro) a R1, abre PuTTY / TeraTerm a 9600 baudios y pega:

```ios
enable
configure terminal
hostname R1
no ip domain-lookup

! 1. Interfaz hacia Switch 1 (LAN 1)
interface GigabitEthernet0/0
 description Hacia Switch 1 - LAN 1
 ip address 192.168.10.1 255.255.255.0
 no shutdown
 exit

! 2. Interfaz WAN hacia R2 (NUBE)
! ---> SI USAN CABLE SERIAL:
interface Serial0/0/0
 description Enlace WAN hacia R2
 ip address 10.0.0.1 255.255.255.252
 clock rate 64000
 no shutdown
 exit

! ---> O SI USAN CABLE ETHERNET DIRECTO (Gig0/1):
! interface GigabitEthernet0/1
!  description Enlace WAN hacia R2
!  ip address 10.0.0.1 255.255.255.252
!  no shutdown
!  exit

! 3. Ruta Estática hacia la red de Laptop 2 (LAN 2)
ip route 192.168.20.0 255.255.255.0 10.0.0.2

end
write memory
```

---

### Configuración de Router 2 (R2):
Conecta tu cable de consola a R2 y pega:

```ios
enable
configure terminal
hostname R2
no ip domain-lookup

! 1. Interfaz hacia Switch 2 (LAN 2)
interface GigabitEthernet0/0
 description Hacia Switch 2 - LAN 2
 ip address 192.168.20.1 255.255.255.0
 no shutdown
 exit

! 2. Interfaz WAN hacia R1 (NUBE)
! ---> SI USAN CABLE SERIAL:
interface Serial0/0/0
 description Enlace WAN hacia R1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit

! ---> O SI USAN CABLE ETHERNET DIRECTO (Gig0/1):
! interface GigabitEthernet0/1
!  description Enlace WAN hacia R1
!  ip address 10.0.0.2 255.255.255.252
!  no shutdown
!  exit

! 3. Ruta Estática hacia la red de Laptop 1 (LAN 1)
ip route 192.168.10.0 255.255.255.0 10.0.0.1

end
write memory
```

---

## 4. Configuración de las Laptops en Windows (Paso a Paso)

En cada una de las laptops debes fijar su dirección IP manualmente:

### En Laptop 1 (Emisor - PC 1):
1. Presiona `Tecla Windows + R`, escribe: `ncpa.cpl` y presiona Enter.
2. Clic derecho sobre el adaptador **Ethernet** (red cableada) ➔ **Propiedades**.
3. Haz doble clic en **Protocolo de Internet versión 4 (TCP/IPv4)**.
4. Selecciona *"Usar la siguiente dirección IP"*:
   - **Dirección IP**: `192.168.10.10`
   - **Máscara de subred**: `255.255.255.0`
   - **Puerta de enlace predeterminada**: `192.168.10.1`
5. Clic en **Aceptar** y **Aceptar**.

### En Laptop 2 (Receptor - PC 2):
1. Presiona `Tecla Windows + R`, escribe: `ncpa.cpl` y presiona Enter.
2. Clic derecho sobre el adaptador **Ethernet** ➔ **Propiedades**.
3. Haz doble clic en **Protocolo de Internet versión 4 (TCP/IPv4)**.
4. Selecciona *"Usar la siguiente dirección IP"*:
   - **Dirección IP**: `192.168.20.10`
   - **Máscara de subred**: `255.255.255.0`
   - **Puerta de enlace predeterminada**: `192.168.20.1`
5. Clic en **Aceptar** y **Aceptar**.

---

## 5. ¡ATENCIÓN! Configuración del Firewall de Windows en Laptop 2

> [!CAUTION]
> Windows Defender Firewall por defecto **bloquea las conexiones entrantes en el puerto 5000** que provengan de otra subred. Si no haces esto, Laptop 1 no podrá comunicarse con Laptop 2.

En **Laptop 2**:
1. Presiona `Tecla Windows + R`, escribe `firewall.cpl` y presiona Enter.
2. A la izquierda, haz clic en **"Activar o desactivar el Firewall de Windows Defender"**.
3. Para la red privada o pública, selecciona temporalmente **"Desactivar el Firewall de Windows Defender"** durante la práctica (o agrega una regla de entrada para el puerto TCP `5000`).
4. Haz clic en **Aceptar**.

---

## 6. Verificación de Conectividad Física

Antes de abrir la aplicación web, abre la terminal (`cmd`) en **Laptop 1** y prueba:
```cmd
ping 192.168.10.1       <-- Prueba comunicación con su Gateway (Router 1)
ping 10.0.0.2           <-- Prueba cruce por el enlace WAN hacia Router 2
ping 192.168.20.10      <-- Prueba comunicación total de extremo a extremo con Laptop 2
```
Si el último ping da `4 recibidos, 0 perdidos`, ¡tu red física está funcionando a la perfección!

---

## 7. Ejecución de la Aplicación Web en las 2 Laptops

### En Laptop 2 (Receptor):
1. Copia la carpeta del proyecto a Laptop 2 (por USB o red).
2. Haz doble clic en el archivo **`iniciar_app.bat`** (se iniciará el servidor web escuchando en `0.0.0.0:5000`).
3. Abre Google Chrome o Edge y entra a:
   $$\mathbf{http://localhost:5000/receiver}$$
   *(Verás el panel de monitoreo de red esperando paquetes).*

### En Laptop 1 (Emisor):
1. Haz doble clic en el archivo **`iniciar_app.bat`**.
2. Abre Google Chrome o Edge y entra a:
   $$\mathbf{http://localhost:5000/sender}$$
3. En la casilla **"Destino en la Red"**, escribe:
   $$\mathbf{http://192.168.20.10:5000/api/receive}$$
4. Escribe el mensaje (o carga un `.txt`), elige **César**, **Vigenère** o **Vernam**, escribe la clave $K$, presiona **"Ejecutar Cifrado"** y luego **"Transmitir a PC 2 (Topología WAN)"**.

### Resultado en Laptop 2:
- En la pantalla de Laptop 2 aparecerá inmediatamente el mensaje cifrado recibido a través de los routers.
- Ingresas la clave $K$, presionas **"Descifrar Mensaje"** y luego **"Descargar Archivo .txt (Descifrado) ✔"**.
