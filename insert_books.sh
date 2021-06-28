#!/usr/bin/env bash

# Carregar informações de conexão do banco de dados
source database.env

# Leia a consulta em uma variável
sql="$(<"query.sql")"

# Se o psql não estiver disponível, saia
if ! command -v psql > /dev/null; then
  echo "Este script requer que o psql esteja instalado e em seu PATH ..."
  exit 1
fi

# Conecte-se ao banco de dados, execute a operação e, em seguida, desconecte
PGPASSWORD="${POSTGRES_PASSWORD}" psql -t -A \
-h "${POSTGRES_HOST}" \
-p "${POSTGRES_PORT}" \
-d "${POSTGRES_DATABASE}" \
-U "${POSTGRES_USERNAME}" \
-c "${sql}"