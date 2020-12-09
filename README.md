# Python y Linux 1 -Proyecto 2 

A Chat program using sockets and public key encryption for 
message communication.

## Install 

### Automatically

You can try executing the next command in bash, it will clone the repository,
create a VENV and install requirements to VENV.

```bash
git clone https://github.com/bonanAngeLOL/pySocket-testajxo.git && cd pySocket-testajxo && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

There's also a bash executable file in the release files (`install.sh`), which
you can use do install and basically has the same command written above.

```bash
chmod +x install.sh
./install.sh
```

If this command did not work, check the following steps to install.

### Steps

The only option available to install is to clone to a local repository.

 ```bash
git clone https://github.com/bonanAngeLOL/pySocket-testajxo.git
```

Create a new VENV  within the project folder.

```bash
cd pySocket-testajxo && python3 -m venv venv 
```

Finally install required libraries listed in `requirements.txt`, 
remember sourcing to `venv/bin/activate` to install packages to 
VENV, not globally.

```bash
source venv/bin/activate && pip install -r requirements.txt
```

## Run

First of all open a terminal, and source to venv from bash.

```bash
cd /path/to/proyecto && source venv/bin/activate
```

But basically, the process is:

- _Start_ a socket server (`init`)
- _Connect_ to another server (`conn`)
- _Send_ a message (`send`)
- _Read_ messages (`inbox`)

You can read help docs with the `help` command.

To exit from the given cmd type exit or CTRL+d

### Help

You can type this command to get help, e.g.

General help:

    ~> help

    Documented commands (type help <topic>):
    ========================================
    EOF  conn  exit  help  inbox  init  send

Read help document of command. Help will display the information
you can find in this document.

    ~> help conn

    conn - Connect to a Server from CMD:

        Use:
            ~> conn [host] [port]
        Example
            ~> conn 192.168.0.1 8085
    ...


### Server

To run as server:

```bash
python3 main.py init [host] [port] [username]
```

But you can also execute main.py and start the server directly in
the given CMD.

```bash
python main.py
~> init [host] [port] [username]
```

When you try to start a server, you'll be notified if port
was successfully binded. e.g.:
                                                               
    Now listening on 192.168.0.21:8095
                                                               
If port, address or anything else prevents this program to bind
a port you'll get an error.
                                                               
    Either you don't have permission or
    port is already in use.
    Try a different port!

#### Examples

In bash console:

```bash
python3 main.py init 192.168.0.100 8090 Oscar
```
Directly in the given cmd

```bash
init 192.168.0.100 8090 Oscar
```

### Connect

Once server socket is started, you can connect to another server.
Note: You won't be able to connect anyone if server hasn't been started 
in the current execution.

```bash
~> conn [host] [port]
```

When you try to connect a message will be displayed
to make you know that it is attempting to connect to server
e.g.:

    connecting to 192.168.0.21:8091

If a connection was successful, you (and server), will be
notified, e.g.:

    Now connected to [server's username]

### Send

Send a message to server

```bash
~> send [server username]
```

After send command is executed you'll be asked to type a
message to be sent, to send that message just press Enter key. e.g.

    ~> send julia
    Write a message
    [Input a message] + Enter

To list all available servers type "send " + <Tab>
Using tabulator will display a list of current servers. e.g.:

    ~> send <TAB>
    angel   juan    julia   pancho

Trying to message a non connected server will lead to error

    ~> send ana
    You're not connected to ana

### Inbox

Function to list messages sent by sender. 

```bash
~> inbox [sender's name]
```

You can also hit <tab> to get a list of users and autocomplete

    ~> inbox <tab>
    angel  julia  

When you type a name and press Enter, a list of messages will be
displayed:

    ~> inbox julia
        julia 2020-12-09 04:39:43 Hola Angel
        julia 2020-12-09 04:39:50 Como estas?
        julia 2020-12-09 04:40:02 responde por favor


## Requerimientos del proyecto
- [x] Se debe asignar un hilo de ejecución a cada conversación, ya sea entrante o saliente.
- [x] Cada objeto debe tener un socket servidor para recibir peticiones de conversación.
- [x] Cuando un objeto desee iniciar una conversación comenzará una conexión a un socket de 
otro objeto utilizando un socket cliente.
- [x] Cada objeto debe tener un archivo de BD que utilizará para almacenamiento de mensajes 
y de llaves, este archivo debe estar en la misma carpeta que el código.py que crea el objeto.
- [x] Las direcciones y puertos del servidor de otros objetos son introducidos de manera manual.
- [x] Cuando  los  sockets  establecen  comunicación,  el  socketcliente  envíasu  nombre  y  llave 
pública al socket servidor, este responde con su nombre yllave pública.
- [x] Cuando se ha llevado a cabo el intercambio de llaves públicas, se comienza la comunicación 
segura de acuerdo al diagrama de comunicación

## ToDo:
- [x] Add Thread blocking in database operations
- [x] Functions to read messages from database
- [x] function to get connected users
- [x] Tidy the code up 
- [x] Add docs
- [x] Cypher and Decrypt functions on messages
- [x] Delete database when leaving
