#!/bin/bash
# usage: run.sh MR_MOQUI_DIR ENGINE TAG OUT_DIR  -- one run of the eight mr-mantle specs on a fresh copy of p_tpl
# (a release build of MR_MOQUI_DIR first: ./moq build --release). Alternate engines: rquickjs A, oxide A, rquickjs B, ...
set -u
W=$1; ENGINE=$2; TAG=$3; OUT=$4
mkdir -p "$OUT"
IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' moqui-pg18)
export entity_ds_db_conf=postgres entity_ds_host=$IP entity_ds_port=5432 entity_ds_user=moqui entity_ds_password=moqui entity_ds_sslmode=disable
docker exec moqui-pg18 dropdb -U moqui --if-exists p_run
docker exec moqui-pg18 createdb -U moqui -T p_tpl p_run || exit 1
export entity_ds_database=p_run script_engine=$ENGINE MOQUI_TX_CACHE_CENSUS_FILE=$OUT/census-$TAG.jsonl
rm -f "$MOQUI_TX_CACHE_CENSUS_FILE"
cd "$W"
./moq test mr-mantle --release --nobuild --db existing \
  --spec OrderToCashBasicFlow,OrderProcureToPayBasicFlow,AccountingSettlement,AccountingPaymentLifecycle,AssetReservationMisc,WarehouseShipping,AccountingPayables,InvoiceOrderApply > "$OUT/test-$TAG.log" 2>&1
echo "exit $? $TAG $ENGINE"; grep "features:" "$OUT/test-$TAG.log"
