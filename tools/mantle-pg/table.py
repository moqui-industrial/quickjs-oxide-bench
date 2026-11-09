"""usage: table.py OUT_DIR A_TAGS B_TAGS, e.g. table.py out rq1,rq2 ox1,ox2 -- median ms a call of the nine services,
from the census frame lines (micros, round_trips) that run.sh writes as OUT_DIR/census-TAG.jsonl."""
import json, statistics as st, os, sys
OUT, A, B = sys.argv[1], sys.argv[2].split(","), sys.argv[3].split(",")
SV = ["order.OrderServices.place#Order", "order.OrderServices.approve#Order", "order.OrderServices.add#OrderProductQuantity",
      "account.InvoiceServices.change#InvoiceState", "account.PaymentServices.create#Payment", "account.PaymentServices.apply#Settlement",
      "shipment.ShipmentServices.pack#Shipment", "account.PaymentServices.get#PaymentFinanceDetail", "account.InvoiceServices.approve#Payable"]

def load(fs):
    d = {}
    for f in fs:
        for l in open(f):
            try:
                j = json.loads(l)
            except Exception:
                continue
            if j.get("kind") != "frame":
                continue
            s = j["service"]
            for k in SV:
                if s.endswith(k):
                    d.setdefault(k, []).append(j)
    return d

runs = {"rq": [f"{OUT}/census-{t}.jsonl" for t in A], "ox": [f"{OUT}/census-{t}.jsonl" for t in B]}
D = {e: [load([f]) for f in fs] for e, fs in runs.items()}
P = {e: load(fs) for e, fs in runs.items()}
tm = {"rq": 0, "ox": 0}
ts = {"rq": [0] * len(A), "ox": [0] * len(B)}
print("| Service | Calls | rquickjs ms | oxide ms | ratio | RT rq | RT ox | sum ms rq1/rq2 | ox1/ox2 | max ms rq | ox |")
for k in SV:
    m = {e: st.median([x["micros"] for x in P[e][k]]) / 1000 for e in P}
    n = len(P["rq"][k]) // len(A)
    rt = {e: st.median([x["round_trips"] for x in P[e][k]]) for e in P}
    for e in D:
        for i, d in enumerate(D[e]):
            ts[e][i] += sum(x['micros'] for x in d[k]) / 1000
    sums = {e: "/".join(f"{sum(x['micros'] for x in d[k]) / 1000:.0f}" for d in D[e]) for e in D}
    mx = {e: max(x["micros"] for x in P[e][k]) / 1000 for e in P}
    for e in tm:
        tm[e] += m[e] * n
    print(f"| `{k}` | {n} | {m['rq']:.1f} | {m['ox']:.1f} | {m['ox'] / m['rq']:.3f} | {rt['rq']:g} | {rt['ox']:g} | {sums['rq']} | {sums['ox']} | {mx['rq']:.0f} | {mx['ox']:.0f} |")
print("median x calls total:", {e: round(v) for e, v in tm.items()})
print("summed micros per run:", {e: [round(v) for v in vs] for e, vs in ts.items()})
for k in SV:
    a = sorted(x["round_trips"] for x in P["rq"][k])
    b = sorted(x["round_trips"] for x in P["ox"][k])
    if a != b:
        print("RT differ", k, sum(a) / len(a), sum(b) / len(b))
