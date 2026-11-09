#!/usr/bin/env python3
"""Round 53: full screen renders over HTTP, single-threaded, as john.doe.

Logs in once and keeps the session on one keep-alive connection. For each case it makes one untimed request, then
`--rounds` rounds of `--n` sequential requests. A request's time runs from sending it to reading its last byte.
With `--perf-pid`, it then runs `perf stat -e instructions:u` on the server over `--perf-n` more requests, so the
instructions per request are measured with no other load.

    python3 -I screen_bench.py --label base --out ../../work/r53/base [--port 8080] [--cases B-html,A-qvt]
        [--rounds 3] [--n 100] [--perf-pid PID] [--perf-n 20] [--no-timing]

It writes `<out>/results.csv` (every request), `<out>/summary.txt` and `<out>/body-<case>.out`: one body per case,
with session tokens masked, for comparing output between builds (`diff -r`).
"""
import argparse, csv, hashlib, http.client, os, re, signal, statistics, subprocess, sys, time, urllib.parse

SCREENS = {
    "A": ("/apps/system/Cache/CacheList", "pageNoLimit=true"),
    "B": ("/apps/tools/Schema/Entities", "pageSize=3000"),
    "C": ("/apps/system/Cache/CacheElements", "cacheName=l10n.message&pageNoLimit=true"),
    "D": ("/apps/tools/ArtifactStats", "levels=3&pageNoLimit=true"),
    "E": ("/apps/system/dashboard", ""),
}


def case_url(screen, mode):
    path, query = SCREENS[screen]
    if mode == "qvt":
        path += ".qvt"
    elif mode == "tui":
        query = (query + "&" if query else "") + "renderMode=tui"
    elif mode == "menu":
        path = "/menuData" + path
    return path + ("?" + query if query else "")


ALL_CASES = [f"{s}-{m}" for s in SCREENS for m in ("html", "qvt", "tui")] + ["A-menu"]

ap = argparse.ArgumentParser()
ap.add_argument("--label", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--port", type=int, default=8080)
ap.add_argument("--cases", default=",".join(ALL_CASES))
ap.add_argument("--rounds", type=int, default=3)
ap.add_argument("--n", type=int, default=100)
ap.add_argument("--perf-pid", type=int)
ap.add_argument("--perf-n", type=int, default=20)
ap.add_argument("--no-timing", action="store_true", help="only the first request and the perf loop")
args = ap.parse_args()
os.makedirs(args.out, exist_ok=True)

cookies = {}
conn = http.client.HTTPConnection("localhost", args.port, timeout=120)


def req(method, path, body=None, extra=None):
    global conn
    h = {"Accept": "text/html", "Accept-Encoding": "identity", "Connection": "keep-alive"}
    if cookies:
        h["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    if extra:
        h.update(extra)
    t0 = time.perf_counter()
    conn.request(method, path, body=body, headers=h)
    r = conn.getresponse()
    t1 = time.perf_counter()
    data = r.read()
    t2 = time.perf_counter()
    for k, v in r.getheaders():
        if k.lower() == "set-cookie":
            n, _, val = v.split(";", 1)[0].partition("=")
            cookies[n.strip()] = val.strip()
    if r.getheader("Connection", "").lower() == "close":
        conn.close()
        conn = http.client.HTTPConnection("localhost", args.port, timeout=120)
    return r.status, r.getheader("Location"), data, (t1 - t0) * 1000, (t2 - t0) * 1000


def follow(method, path, body=None, extra=None):
    st, loc, data, _, _ = req(method, path, body, extra)
    for _ in range(5):
        if st not in (301, 302, 303, 307) or not loc:
            break
        p = urllib.parse.urlparse(loc)
        st, loc, data, _, _ = req("GET", (p.path or "/") + ("?" + p.query if p.query else ""))
    return st, data


MASK = re.compile(rb'(moquiSessionToken|sessionToken|csrf[A-Za-z]*)(["\'=:\s]+)([A-Za-z0-9_\-+/=]{8,})')


def mask(data):
    data = MASK.sub(rb"\1\2<token>", data)
    # times of day and the uptime / memory numbers on the dashboard move between requests
    data = re.sub(rb"\d{4}-\d\d-\d\d \d\d:\d\d(:\d\d)?", b"<time>", data)
    # the build's resource stamps and hashes
    data = re.sub(rb"\?v=[0-9a-f]+", b"?v=<stamp>", data)
    data = re.sub(rb'"[0-9a-f]{40}"', b'"<hash>"', data)
    return data


follow("GET", "/Login")
st, _ = follow("POST", "/Login/login", urllib.parse.urlencode({"username": "john.doe", "password": "moqui"}),
               {"Content-Type": "application/x-www-form-urlencoded"})
if "moqui.session" not in cookies and "JSESSIONID" not in cookies:
    sys.exit(f"login failed: {st} {cookies}")

cases = [c for c in args.cases.split(",") if c]
rows, summary, perf_rows = [], [], {}


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))]


for case in cases:
    screen, mode = case.split("-")
    url = case_url(screen, mode)
    st, _, data, _, first = req("GET", url)
    if st != 200 or b'name="password"' in data[:200000] and mode == "html":
        sys.exit(f"{case} {url}: status {st}, {len(data)} bytes")
    body = mask(data)
    with open(os.path.join(args.out, f"body-{case}.out"), "wb") as f:
        f.write(body)
    line = f"{case:8} first {first:8.1f} ms  {len(data):8} bytes  sha {hashlib.sha1(body).hexdigest()[:10]}"
    print(line, flush=True)
    summary.append(line)
    if not args.no_timing:
        for rnd in range(1, args.rounds + 1):
            ts, tf, sizes, errs = [], [], [], 0
            for i in range(args.n):
                st, _, data, ttfb, tot = req("GET", url)
                errs += st != 200
                ts.append(tot)
                tf.append(ttfb)
                sizes.append(len(data))
                rows.append((args.label, case, rnd, i, st, len(data), round(ttfb, 3), round(tot, 3)))
            line = (f"{case:8} r{rnd} min {min(ts):7.2f} med {statistics.median(ts):7.2f} mean {statistics.mean(ts):7.2f} "
                    f"p90 {pct(ts, 90):7.2f} max {max(ts):7.2f} sd {statistics.stdev(ts):6.2f} ttfb {statistics.median(tf):7.2f} "
                    f"errs {errs} bytes {min(sizes)}-{max(sizes)}")
            print(line, flush=True)
            summary.append(line)
    if args.perf_pid:
        perf = subprocess.Popen(["perf", "stat", "-x,", "-e", "instructions:u,task-clock", "-p", str(args.perf_pid)],
                                stderr=subprocess.PIPE, text=True)
        time.sleep(0.3)
        for _ in range(args.perf_n):
            req("GET", url)
        perf.send_signal(signal.SIGINT)
        err = perf.communicate()[1]
        vals = {}
        for l in err.splitlines():
            parts = l.split(",")
            if len(parts) > 3 and parts[0].replace(".", "").isdigit():
                vals[parts[2].split(":")[0]] = float(parts[0])
        ins = vals.get("instructions", 0) / args.perf_n
        clk = vals.get("task-clock", 0) / args.perf_n
        line = f"{case:8} perf {ins / 1e6:9.2f} M instructions:u/request  task-clock {clk:7.2f} ms/request (incl. idle poll)"
        print(line, flush=True)
        summary.append(line)

with open(os.path.join(args.out, "results.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["label", "case", "round", "i", "status", "bytes", "ttfb_ms", "total_ms"])
    w.writerows(rows)
with open(os.path.join(args.out, "summary.txt"), "w") as f:
    f.write("\n".join(summary) + "\n")
