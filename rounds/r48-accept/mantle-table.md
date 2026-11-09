| Service | Calls | rquickjs ms | oxide ms | ratio | RT rq | RT ox | sum ms rq1/rq2 | ox1/ox2 | max ms rq | ox |
| `order.OrderServices.place#Order` | 26 | 21.1 | 21.1 | 0.997 | 66 | 66 | 659/635 | 658/628 | 99 | 110 |
| `order.OrderServices.approve#Order` | 26 | 16.3 | 16.3 | 1.002 | 54 | 54 | 460/458 | 470/469 | 38 | 51 |
| `order.OrderServices.add#OrderProductQuantity` | 32 | 16.7 | 16.7 | 0.998 | 52 | 52 | 631/622 | 630/628 | 45 | 46 |
| `account.InvoiceServices.change#InvoiceState` | 2 | 23.0 | 22.6 | 0.982 | 80 | 80 | 46/46 | 49/45 | 41 | 44 |
| `account.PaymentServices.create#Payment` | 11 | 23.4 | 23.7 | 1.015 | 77 | 77 | 233/235 | 235/228 | 27 | 27 |
| `account.PaymentServices.apply#Settlement` | 8 | 48.0 | 49.0 | 1.021 | 120 | 120 | 437/436 | 440/453 | 150 | 154 |
| `shipment.ShipmentServices.pack#Shipment` | 16 | 44.2 | 43.0 | 0.975 | 117 | 117 | 822/815 | 821/837 | 136 | 137 |
| `account.PaymentServices.get#PaymentFinanceDetail` | 24 | 12.7 | 13.9 | 1.095 | 27.5 | 27.5 | 359/364 | 378/395 | 60 | 62 |
| `account.InvoiceServices.approve#Payable` | 6 | 29.0 | 29.0 | 0.999 | 84 | 84 | 133/136 | 132/142 | 39 | 38 |
median x calls total: {'rq': 3380, 'ox': 3400}
summed micros per run: {'rq': [3782, 3749], 'ox': [3813, 3825]}
RT differ account.PaymentServices.apply#Settlement 153.375 153.625
