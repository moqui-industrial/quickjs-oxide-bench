#!/bin/bash
# remove the delay and the databases, stop moqui-pg18 (never touch other containers)
docker exec moqui-pg18 tc qdisc del dev eth0 root 2>/dev/null
docker exec moqui-pg18 dropdb -U moqui --if-exists p_run
docker exec moqui-pg18 dropdb -U moqui --if-exists p_tpl
docker stop moqui-pg18 >/dev/null; echo stopped
