#!/bin/bash
# usage: run.sh MR_MOQUI_DIR TAG OUT_DIR [pg18]
# The nine Mantle operations in process (plans/Profiling3.md M3, the spec-driven form of mantle_speed): the eight
# mr-mantle specs that run them, with the operation profile (MOQUI_OP_PROFILE, M1: CPU, round trips, counts per
# outermost call) and the census with statement shapes (MOQUI_TX_CACHE_CENSUS_FILE, M2) on. With no fourth argument
# on the specs' embedded Postgres (a local socket); with `pg18`, on a fresh copy of p_tpl in moqui-pg18 as
# ../mantle-pg/run.sh does (setup.sh there first). A release build of MR_MOQUI_DIR first: ./moq build --release.
set -u
W=$1; TAG=$2; OUT=$(realpath -m "$3"); DB=${4:-embedded}
mkdir -p "$OUT"
export MOQUI_TX_CACHE_CENSUS_FILE=$OUT/census-$TAG.jsonl MOQUI_OP_PROFILE=$OUT/ops-$TAG.jsonl
rm -f "$MOQUI_TX_CACHE_CENSUS_FILE" "$MOQUI_OP_PROFILE"
EXTRA=()
if [ "$DB" = pg18 ]; then
  IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' moqui-pg18)
  export entity_ds_db_conf=postgres entity_ds_host=$IP entity_ds_port=5432 entity_ds_user=moqui entity_ds_password=moqui entity_ds_sslmode=disable
  docker exec moqui-pg18 dropdb -U moqui --if-exists p_run
  docker exec moqui-pg18 createdb -U moqui -T p_tpl p_run || exit 1
  export entity_ds_database=p_run
  EXTRA=(--db existing)
fi
cd "$W"
./moq test mr-mantle --release --nobuild "${EXTRA[@]}" \
  --spec OrderToCashBasicFlow,OrderProcureToPayBasicFlow,AccountingSettlement,AccountingPaymentLifecycle,AssetReservationMisc,WarehouseShipping,AccountingPayables,InvoiceOrderApply > "$OUT/test-$TAG.log" 2>&1
echo "exit $? $TAG $DB"; grep "features:" "$OUT/test-$TAG.log"
