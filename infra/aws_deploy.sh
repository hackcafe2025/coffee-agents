#!/bin/bash
# Copia e roda em EC2 (ajuste key e user)
EC2_USER="ec2-user"
EC2_IP="yy.yy.yy.yy"
KEY_PATH="~/.ssh/yourkey.pem"
REMOTE_DIR="/home/${EC2_USER}/coffee-agents"

scp -i ${KEY_PATH} -r . ${EC2_USER}@${EC2_IP}:${REMOTE_DIR}
ssh -i ${KEY_PATH} ${EC2_USER}@${EC2_IP} "cd ${REMOTE_DIR} && docker-compose build && docker-compose up -d"
echo "Deploy triggered to ${EC2_IP}"
