#!/bin/bash

echo "<<<<<<<<< ${AUTH_POSTGRES_HOST} >>>>>>>>>"


# Verifica que las variables necesarias estén configuradas
if [[ -z "$AUTH_POSTGRES_HOST" || -z "$AUTH_POSTGRES_PORT" || -z "$AUTH_POSTGRES_DB" ]]; then
    echo "Error: Las variables POSTGRES_HOST, POSTGRES_PORT o POSTGRES_DB no están configuradas."
    exit 1
fi


# Espera a que PostgreSQL esté disponible
dockerize -wait tcp://$AUTH_POSTGRES_HOST:$AUTH_POSTGRES_PORT -timeout 30s
if [ $? -ne 0 ]; then
    echo "Error: No se pudo conectar a PostgreSQL en $AUTH_POSTGRES_HOST:$AUTH_POSTGRES_PORT"
    exit 1
fi

python app.py
