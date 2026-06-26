#!/bin/bash
set -e

DB=/data/quickmart.duckdb

# Initialize the database from the mounted CSVs on first run only.
if [ ! -f "$DB" ]; then
    echo "[duckdb] Initializing database from /datasets CSVs..."
    duckdb "$DB" < /app/init.sql
    echo "[duckdb] Done."
fi

# DuckDB's UI server binds to the loopback interface only (::1:4213), which a
# Docker port-forward can't reach. Start the UI in the background (kept alive by
# `sleep infinity` holding stdin open so the REPL never hits EOF), then bridge
# the published port to it with socat.
echo "[duckdb] Starting UI server on internal [::1]:4213 ..."
sleep infinity | duckdb "$DB" --ui &

# give the UI server a moment to bind
sleep 2

echo "[duckdb] Bridging 0.0.0.0:4213 -> [::1]:4213  (open http://localhost:4213)"
exec socat TCP-LISTEN:4213,bind=0.0.0.0,fork,reuseaddr TCP6:[::1]:4213
