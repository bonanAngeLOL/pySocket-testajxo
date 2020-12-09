#!/bin/bash
ErrorM="\n\nAn error happened, check the install instructions at echo https://github.com/bonanAngeLOL/pySocket-testajxo\n\n"
echo -e "\n\nInstalling ... proyect from GitHub repository\n\n"
git clone https://github.com/bonanAngeLOL/pySocket-testajxo.git
if [ $? -eq 0 ]; then
    echo -e "\n\n!!!!!!Repository cloned\n\n"
else
    echo -e $ErrorM
    echo -e "\n\n!!!!Could not clone repository\n\n"
    exit 1
fi
cd pySocket-testajxo
python3 -m venv venv
if [ $? -eq 0 ]; then
    echo -e "\n\n!!!!! Python VENV created\n\n"
else
    echo -e $ErrorM
    echo -e "\n\n!!!!! Could not create VENV, check your python installation\n\n"
    exit 1
fi
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "\n\n!!!!!! Executing now from VENV \n\n "
else
    echo -e $ErrorM
    echo -e "\n\n!!!!!VENV python installation not found\n\n"
    exit 1
fi
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "\n\n!!!!!All the requirements successfully installed\n\n"
else
    echo -e $ErrorM
    echo -e "\n\n !!!!! PIP error installing requirements\n\n"
    exit 1
fi
echo -e "\n\n!!!Project installed successfully!!!\n\n"
