#!/bin/bash

set -e

echo "Waiting for Postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "Postgres started"

uvicorn monster_spawner.main:app --reload --workers 1 --host 0.0.0.0 --port 8002
