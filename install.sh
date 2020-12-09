#!/bin/bash
ErrorM="An error happened, check the install instructions at echo https://github.com/bonanAngeLOL/pySocket-testajxo"
echo -e "\n\nInstalling ... proyect from GitHub repository\n"
git clone https://github.com/bonanAngeLOL/pySocket-testajxo.git
if [ $? -eq 0 ]; then
    echo "Repository cloned"
else
    echo $ErrorM
    echo "Could not clone repository"
    exit 1
fi
cd pySocket-testajxo
python3 -m venv venv
if [ $? -eq 0 ]; then
    echo "Python VENV created"
else
    echo $ErrorM
    echo "Could not create VENV, check your python installation"
    exit 1
fi
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo "Executing now from VENV"
else
    echo $ErrorM
    echo "VENV python installation not found"
    exit 1
fi
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "All the requirements successfully installed"
else
    echo $ErrorM
    echo "PIP error installing requirements"
    exit 1
fi
