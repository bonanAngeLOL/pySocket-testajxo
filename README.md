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

### To Do: 

- [x] Create socket
- [x] Establish connection user - server
- [x] Runnable by console command
- [x] Use bidirectional communication from client app
- [X] User to user communication
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
