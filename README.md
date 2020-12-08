# Python y Linux 1 -Proyecto 2 

A Chat program using sockets and public key encryption for 
message communication.

### Install 

Before installing create a new VENV to place the code within.

```bash
mkdir -p proyecto && cd "$_" && python3 -m venv venv
```

Current install options are only to clone project to local 
and installing required libraries listed in `requirements.txt`

```bash
pip3 install -r requirements.txt
```

### Run

First of all open a terminal, and source to venv from bash

```bash
cd /path/to/proyecto && source venv/bin/activate
```

To run as server:

```bash
python main.py  init [ip] [port]
```

To run as client:

```bash
python main.py conn [server_ip] [server_port]
```

### Requerimientos del proyecto
- [x] Se debe asignar un hilo de ejecución a cada conversación, ya sea entrante o saliente.
- [x] Cada objeto debe tener un socket servidor para recibir peticiones de conversación.
- [x] Cuando un objeto desee iniciar una conversación comenzará una conexión a un socket de otro objeto utilizando un socket cliente.
- [ ] Cada objeto debe tener un archivo de BD que utilizará para almacenamiento de mensajes y de llaves, este archivo debe estar en la misma carpeta que el código.py que crea el objeto.
- [x] Las direcciones y puertos del servidor de otros objetos son introducidos de manera manual.
- [x] Cuando  los  sockets  establecen  comunicación,  el  socketcliente  envíasu  nombre  y  llave públicaal socketservidor, este responde con su nombre yllave pública.
- [x] Cuando se ha llevado a cabo el intercambio de llaves públicas, se comienza la comunicación segura de acuerdo al diagrama de comunicación

### ToDo:
- [ ] Add Thread blocking in database operations
- [ ] Functions to read messages from database
- [x] function to get connected users
- [x] Tidy the code up 
- [x] Add docs
- [ ] Cypher and Decrypt functions on messages
- [ ] Delete database when leaving
