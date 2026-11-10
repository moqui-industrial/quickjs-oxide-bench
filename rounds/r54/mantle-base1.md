| Operation | Calls | ms | CPU ms | RT | name reads | name writes | field reads | services | entity ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `place#Order` | 31 | 8.45 | 5.18 | 66 | 413 | 169 | 81 | 25 | 73 |
| `approve#Order` | 26 | 5.96 | 3.85 | 54 | 235.5 | 109 | 56 | 18 | 54 |
| `add#OrderProductQuantity` | 42 | 7.81 | 5.29 | 51 | 227 | 102 | 63 | 21 | 65 |
| `change#InvoiceState` | 2 | 7.02 | 4.39 | 80 | 187.5 | 86.5 | 163 | 29 | 92 |
| `create#Payment` | 11 | 8.07 | 5.56 | 77 | 338 | 129 | 219 | 41 | 96 |
| `apply#Settlement` | 9 | 30.64 | 18.30 | 135 | 860 | 388 | 599 | 80 | 386 |
| `pack#Shipment` | 8 | 27.69 | 15.91 | 137.5 | 1472.5 | 602.5 | 511 | 87.5 | 246 |
| `get#PaymentFinanceDetail` | 24 | 8.80 | 4.68 | 27.5 | 77 | 73 | 174.5 | 6 | 113 |
| `approve#Payable` | 6 | 12.53 | 7.57 | 84 | 472 | 209 | 286.5 | 48.5 | 180.5 |

| Operation | frame RT | read | lock | count | sequence | write | stream | begin | commit | savepoint | other | repeats | other params | read after read |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `place#Order` | 66 | 32 | 8 | 1 | 0 | 0 | 0 | 0 | 1 | 20.5 | 0 | 46 | 10 | 20 |
| `approve#Order` | 54 | 28 | 4 | 2 | 0 | 0 | 0 | 0 | 1 | 17 | 0 | 35 | 7 | 16 |
| `add#OrderProductQuantity` | 52 | 27 | 5.5 | 0 | 0 | 0 | 0 | 0 | 1 | 16 | 0 | 38 | 10 | 16 |
| `change#InvoiceState` | 80 | 42.5 | 10.5 | 1 | 0.5 | 0 | 0 | 0 | 1 | 23 | 0 | 67.5 | 29 | 30 |
| `create#Payment` | 77 | 37 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 27 | 0 | 70 | 30 | 19 |
| `apply#Settlement` | 120 | 72.5 | 19 | 4.5 | 0 | 0 | 0 | 0 | 1 | 20.5 | 0 | 69 | 28.5 | 75 |
| `pack#Shipment` | 117 | 69 | 9.5 | 0 | 0 | 0 | 0 | 0 | 1 | 36 | 0 | 85.5 | 30 | 43 |
| `get#PaymentFinanceDetail` | 27.5 | 23.5 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 5 | 2 | 25.5 |
| `approve#Payable` | 84 | 50.5 | 9 | 3 | 0 | 0 | 0 | 0 | 1 | 17 | 0 | 49.5 | 20 | 43 |

Shapes most waited for, over the nine operations' frames (all runs):
| waited | kind | statement |
|---:|---|---|
| 2781 | savepoint | `SAVEPOINT moqui_feed` |
| 1021 | read | `SELECT order_header` |
| 781 | read | `SELECT order_part` |
| 721 | read | `SELECT entity_audit_log` |
| 549 | read | `SELECT order_item` |
| 532 | read | `SELECT db_resource` |
| 284 | lock | `SELECT order_header` |
| 281 | read | `SELECT party_role` |
| 188 | read | `SELECT payment` |
| 175 | commit | `COMMIT` |
| 159 | read | `SELECT localized_message` |
| 159 | read | `SELECT payment_application` |
| 147 | lock | `SELECT order_part` |
| 141 | lock | `SELECT gl_account_org_time_period` |
| 126 | read | `SELECT SELECT` |
| 112 | read | `SELECT invoice_item` |
| 111 | read | `SELECT party` |
| 103 | read | `SELECT invoice` |
| 99 | read | `SELECT localized_entity_field` |
| 97 | read | `SELECT time_period` |
| 87 | lock | `SELECT time_period` |
| 81 | read | `SELECT acctg_trans` |
| 76 | read | `SELECT asset` |
| 74 | read | `SELECT asset_issuance` |
| 73 | read | `SELECT asset_reservation` |
| 73 | lock | `SELECT gl_account_organization` |
| 70 | read | `SELECT payment_content` |
| 67 | lock | `SELECT acctg_trans` |
| 64 | lock | `SELECT invoice` |
| 59 | read | `SELECT acctg_trans_entry` |
