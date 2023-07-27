#!/bin/bash

VM_NAME=$1
PROJECT_ID=$2
ZONE=$3

echo "Criação da Instância"

gcloud compute instances create $VM_NAME \
--project=$PROJECT_ID \
--zone=$ZONE \
--machine-type=e2-micro --image-family=debian-12 --image-project=debian-cloud \
--scopes=https://www.googleapis.com/auth/devstorage.read_write

echo "Criação da Instância finalizada"

sleep 30

# Instalação de dependências
## Copia o arquivo com o script
gcloud compute scp dependencies.sh $VM_NAME:~/ --zone=$ZONE 

## Executa a instalação
gcloud compute ssh $VM_NAME --zone=$ZONE --command="bash ~/dependencies.sh"

# Execução do arquivo principal
## Copia o arquivo com o script e o arquivo de configuração
gcloud compute scp config.json $VM_NAME:~/ --zone=$ZONE 
gcloud compute scp etl_github.py $VM_NAME:~/ --zone=$ZONE 

## Executa o processo
gcloud compute ssh $VM_NAME --zone=$ZONE --command="my_env/bin/python3 ~/etl_github.py"

# Para a instância da VM (Compute Engine)
gcloud compute instances stop $VM_NAME --zone=$ZONE