#!/bin/bash
# Script simples: copia arquivos para VM e roda docker-compose
# Ajuste VARS conforme sua infra
VM_USER="youruser"
VM_IP="xx.xx.xx.xx"
REMOTE_DIR="/home/$VM_USER/coffee-agents"

scp -r . ${VM_USER}@${VM_IP}:${REMOTE_DIR}
ssh ${VM_USER}@${VM_IP} "cd ${REMOTE_DIR} && docker-compose pull || true && docker-compose build && docker-compose up -d"
echo "Deploy triggered to ${VM_IP}"
