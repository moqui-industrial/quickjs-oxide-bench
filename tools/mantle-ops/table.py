"""usage: table.py OUT_DIR TAG[,TAG...] -- the nine Mantle operations from run.sh's files (plans/Profiling3.md M1-M3).

For each operation: the medians over its calls of the outermost call's wall and CPU time, round trips, bare-name reads
and writes, entity field reads and service calls (ops-TAG.jsonl), then from its census frames (census-TAG.jsonl) the
round trips by statement kind (waited), the repeats of a shape, those with other parameters, and reads right after a
read. Then the statement shapes most waited for over all nine."""
import json, statistics as st, sys
from collections import Counter, defaultdict

OUT, TAGS = sys.argv[1], sys.argv[2].split(",")
SV = ["order.OrderServices.place#Order", "order.OrderServices.approve#Order", "order.OrderServices.add#OrderProductQuantity",
      "account.InvoiceServices.change#InvoiceState", "account.PaymentServices.create#Payment", "account.PaymentServices.apply#Settlement",
      "shipment.ShipmentServices.pack#Shipment", "account.PaymentServices.get#PaymentFinanceDetail", "account.InvoiceServices.approve#Payable"]


def lines(path):
    try:
        for line in open(path):
            try:
                yield json.loads(line)
            except ValueError:
                continue
    except FileNotFoundError:
        return


def short(service):
    return service.split(".")[-1]


ops, frames = defaultdict(list), defaultdict(list)
for tag in TAGS:
    for j in lines(f"{OUT}/ops-{tag}.jsonl"):
        for k in SV:
            if j.get("path", "").endswith(k):
                ops[k].append(j)
    for j in lines(f"{OUT}/census-{tag}.jsonl"):
        if j.get("kind") != "frame":
            continue
        for k in SV:
            if j.get("service", "").endswith(k):
                frames[k].append(j)


def med(values):
    values = [v for v in values if v is not None]
    return st.median(values) if values else 0


print("| Operation | Calls | ms | CPU ms | RT | name reads | name writes | field reads | services | entity ops |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for k in SV:
    o = ops[k]
    if not o:
        print(f"| `{short(k)}` | 0 | | | | | | | | |")
        continue
    c = lambda name: med([x["counts"].get(name, 0) for x in o])
    services = med([x["phases"].get("phase:service.nested", {}).get("n", 0) + 1 for x in o])
    entity = med([sum(n for a, n in x["artifacts"].items() if a.startswith("AT_ENTITY")) for x in o])
    print(f"| `{short(k)}` | {len(o) // len(TAGS)} | {med([x['total_us'] for x in o]) / 1000:.2f} | "
          f"{med([x['cpu_us'] for x in o]) / 1000:.2f} | {med([x['round_trips'] for x in o]):g} | {c('name.read'):g} | "
          f"{c('name.write'):g} | {c('field.read'):g} | {services:g} | {entity:g} |")

print()
kinds = ["read", "lock", "count", "sequence", "write", "stream", "begin", "commit", "savepoint", "other"]
print("| Operation | frame RT | " + " | ".join(kinds) + " | repeats | other params | read after read |")
print("|---|---:|" + "---:|" * (len(kinds) + 3))
shapes = Counter()
heads = {}
for k in SV:
    f = frames[k]
    if not f:
        continue
    waited = {kind: med([x.get("kinds", {}).get(kind, {}).get("waited", 0) for x in f]) for kind in kinds}
    print(f"| `{short(k)}` | {med([x['round_trips'] for x in f]):g} | " + " | ".join(f"{waited[kind]:g}" for kind in kinds)
          + f" | {med([x.get('repeats', 0) for x in f]):g} | {med([x.get('repeats_other_params', 0) for x in f]):g} | "
          f"{med([x.get('read_after_read', 0) for x in f]):g} |")
    for x in f:
        for shape in x.get("shapes", []):
            shapes[(shape["kind"], shape["head"])] += shape["waited"]

print("\nShapes most waited for, over the nine operations' frames (all runs):")
print("| waited | kind | statement |")
print("|---:|---|---|")
for (kind, head), n in shapes.most_common(30):
    print(f"| {n} | {kind} | `{head}` |")
