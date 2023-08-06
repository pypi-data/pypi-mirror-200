#!/bin/env bash

BASE_PATH="${HOME}"
PROJECT_PATH=Documentos/Proyectos2022
SERVICE_TPL=backup_collector.service.tpl
ENVIRON_TPL=backup_collector.env.tpl

SERVICE=$(echo $SERVICE_TPL | awk -F'.'  '{print $1"."$2}')
ENVIRON=$(echo $ENVIRON_TPL | awk -F'.'  '{print $1"."$2}')

rm -f $SERVICE
rm -f $ENVIRON

sed -e "s|\[BASE_PATH\]|"${BASE_PATH}"|g;s|\[PROJECT_PATH\]|"${PROJECT_PATH}"|g;s/\[USER\]/${USER}/g" $SERVICE_TPL>$SERVICE
sed -e "s|\[BASE_URL\]|${BASE_URL}|g" $ENVIRON_TPL>$ENVIRON


LOCAL=$(pwd)
SYSTEMD_PATH="$HOME/.config/systemd/user"

rm ${SYSTEMD_PATH}/$SERVICE
ln -s ${LOCAL}/$SERVICE ${SYSTEMD_PATH}/$SERVICE

echo "$(ls ${SYSTEMD_PATH}|grep $SERVICE) is located as service"

systemctl enable --user $SERVICE
systemctl start --user $SERVICE
systemctl status --user $SERVICE


