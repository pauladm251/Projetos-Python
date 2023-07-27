#!/bin/bash

# Criação/Ativação de um ambiente virtual
sudo apt install -y python3-venv
python3 -m venv my_env
source my_env/bin/activate

#Instalação das dependências
pip install requests pandas gcsfs