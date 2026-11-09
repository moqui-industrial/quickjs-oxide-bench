#!/bin/bash
# The Mantle operations against a Postgres 200 µs away (plans/Profiling.md Rounds 26, 27, 32).
# usage: setup.sh MR_MOQUI_DIR   -- start moqui-pg18, load every component's data into the template p_tpl, add the delay
set -eu
W=$1
docker start moqui-pg18 >/dev/null
IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' moqui-pg18)
echo "moqui-pg18 at $IP"
for i in $(seq 60); do docker exec moqui-pg18 pg_isready -U moqui -q && break; sleep 1; done
docker exec moqui-pg18 dropdb -U moqui --if-exists p_tpl
docker exec moqui-pg18 createdb -U moqui p_tpl
cd "$W"
entity_ds_db_conf=postgres entity_ds_host=$IP entity_ds_port=5432 entity_ds_user=moqui entity_ds_password=moqui \
  entity_ds_sslmode=disable entity_ds_database=p_tpl ./moq load --release --nobuild
docker exec moqui-pg18 tc qdisc replace dev eth0 root netem delay 200us
echo "delay on; run run.sh for each engine, then teardown.sh"
