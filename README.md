# pyBabilu

A Chat program using sockets and public key encryption for 
message communication with Qt interfaces

### Install 

Before installing create a new VENV to place the code within.

```bash
mkdir -p babilu && cd "$_" && python3 -m venv venv
```

Current install options are only to clone project to local 
and installing required libraries listed in `requirements.txt`

```bash
pip3 install -r requirements.txt
```

### Run

First of all open a terminal, and source to venv from bash

```bash
cd /path/to/babilu
source venv/bin/activate
```

To run as server:

```bash
python main.py start [ip] [port] [max_users]
```

To run as client:

```bash
python main.py connect [server_ip] [port] [user] [password]
```

### Requerimientos del proyecto
- [x] Se debe asignar un hilo de ejecución a cada conversación, ya sea entrante o saliente.
- [x] Cada objeto debe tener un socket servidor para recibir peticiones de conversación.
- [x] Cuando un objeto desee iniciar una conversación comenzará una conexión a un socket de otro objeto utilizando un socket cliente.
- [ ] Cada objeto debe tener un archivo de BD que utilizará para almacenamiento de mensajes y de llaves, este archivo debe estar en la misma carpeta que el código.py que crea el objeto.
- [x] Las direcciones y puertos del servidor de otros objetos son introducidos de manera manual.
- [ ] Cuando  los  sockets  establecen  comunicación,  el  socketcliente  envíasu  nombre  y  llave públicaal socketservidor, este responde con su nombre yllave pública.
- [ ] Cuando se ha llevado a cabo el intercambio de llaves públicas, se comienza la comunicación segura de acuerdo al diagrama de comunicación

### To Do: 

- [x] Create socket
- [x] Establish connection user - server
- [x] Runnable by console command
- [x] Use bidirectional communication from client app
- [ ] User to user communication
- [ ] Set server timeout
- [ ] Add public key encryption
- [ ] Set user db 
- [ ] Add auth 
- [ ] Detect user disconnection
- [ ] Change print to logger
- [ ] Use SQlite on client
- [ ] Add actions on received info from server (in client)
- [ ] Qt Interfaces

#### If it happens to have more time to work

- [ ] Make code run as a Unix daemon
- [ ] Achieve any async socket listening
- [ ] Use security signal protocol 
