The nine Mantle operations against moqui-pg18 200 us away (tools/mantle-ops/run.sh ... pg18), census frame medians over two runs,
against R48's run ox1 (Profiling3 section 2).

| Operation | R48 ms | R60 ms | ratio | R48 round trips | R60 round trips |
|---|---:|---:|---:|---:|---:|
| `place#Order` | 21.4 | 16.9 | 0.79 | 66 | 46 |
| `approve#Order` | 16.1 | 13.0 | 0.81 | 54 | 38 |
| `add#OrderProductQuantity` | 16.4 | 13.4 | 0.82 | 52 | 37 |
| `change#InvoiceState` | 24.4 | 18.2 | 0.75 | 80 | 57.5 |
| `create#Payment` | 24.0 | 18.0 | 0.75 | 77 | 50 |
| `apply#Settlement` | 48.6 | 43.2 | 0.89 | 120 | 100.5 |
| `pack#Shipment` | 43.4 | 35.8 | 0.82 | 117 | 84.5 |
| `get#PaymentFinanceDetail` | 12.9 | 13.4 | 1.04 | 27.5 | 27.5 |
| `approve#Payable` | 28.7 | 25.1 | 0.87 | 84 | 66.5 |
