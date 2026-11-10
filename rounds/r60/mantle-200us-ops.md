| Operation | Calls | ms | CPU ms | RT | name reads | name writes | field reads | services | entity ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `place#Order` | 31 | 17.78 | 4.95 | 46 | 368 | 164 | 81 | 25 | 73 |
| `approve#Order` | 26 | 13.26 | 3.58 | 38 | 213.5 | 109 | 56 | 18 | 54 |
| `add#OrderProductQuantity` | 42 | 13.57 | 4.08 | 36 | 210 | 102 | 63 | 21 | 65 |
| `change#InvoiceState` | 2 | 18.46 | 4.37 | 57.5 | 158 | 85.5 | 163 | 29 | 92 |
| `create#Payment` | 11 | 18.27 | 5.28 | 50 | 299 | 128 | 219 | 41 | 96 |
| `apply#Settlement` | 9 | 53.11 | 14.88 | 126 | 708 | 382 | 599 | 80 | 386 |
| `pack#Shipment` | 8 | 44.21 | 13.92 | 105.5 | 1016 | 518 | 511 | 87.5 | 241.5 |
| `get#PaymentFinanceDetail` | 24 | 13.59 | 3.86 | 27.5 | 71 | 73 | 174.5 | 6 | 113 |
| `approve#Payable` | 6 | 25.41 | 7.46 | 66.5 | 420 | 207 | 286.5 | 48.5 | 180.5 |

| Operation | frame RT | read | lock | count | sequence | write | stream | begin | commit | savepoint | other | repeats | other params | read after read |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `place#Order` | 46 | 32 | 8 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 46 | 10 | 20 |
| `approve#Order` | 38 | 28 | 4 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 35 | 7 | 16 |
| `add#OrderProductQuantity` | 37 | 27 | 5.5 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 38 | 10 | 16 |
| `change#InvoiceState` | 57.5 | 42.5 | 10.5 | 1 | 0.5 | 0 | 0 | 0 | 1 | 0.5 | 0 | 67.5 | 29 | 30 |
| `create#Payment` | 50 | 37 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 70 | 30 | 19 |
| `apply#Settlement` | 100.5 | 72.5 | 19 | 4.5 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 69 | 29 | 75 |
| `pack#Shipment` | 84.5 | 69 | 9.5 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 85.5 | 30 | 43 |
| `get#PaymentFinanceDetail` | 27.5 | 23.5 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 2 | 25.5 |
| `approve#Payable` | 66.5 | 50.5 | 9 | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 49.5 | 20 | 43 |

Shapes most waited for, over the nine operations' frames (all runs):
| waited | kind | statement |
|---:|---|---|
| 2042 | read | `SELECT order_header` |
| 1562 | read | `SELECT order_part` |
| 1442 | read | `SELECT entity_audit_log` |
| 1098 | read | `SELECT order_item` |
| 568 | lock | `SELECT order_header` |
| 562 | read | `SELECT party_role` |
| 376 | read | `SELECT payment` |
| 336 | commit | `COMMIT` |
| 318 | read | `SELECT payment_application` |
| 294 | lock | `SELECT order_part` |
| 282 | lock | `SELECT gl_account_org_time_period` |
| 252 | read | `SELECT SELECT` |
| 246 | read | `SELECT localized_message` |
| 224 | read | `SELECT invoice_item` |
| 222 | read | `SELECT party` |
| 220 | savepoint | `SAVEPOINT moqui_feed` |
| 206 | read | `SELECT invoice` |
| 198 | read | `SELECT localized_entity_field` |
| 194 | read | `SELECT time_period` |
| 174 | lock | `SELECT time_period` |
| 162 | read | `SELECT acctg_trans` |
| 152 | read | `SELECT asset` |
| 148 | read | `SELECT asset_issuance` |
| 146 | read | `SELECT asset_reservation` |
| 146 | lock | `SELECT gl_account_organization` |
| 140 | read | `SELECT payment_content` |
| 134 | lock | `SELECT acctg_trans` |
| 128 | lock | `SELECT invoice` |
| 118 | read | `SELECT acctg_trans_entry` |
| 118 | read | `SELECT order_item_billing` |
