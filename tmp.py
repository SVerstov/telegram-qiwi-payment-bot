from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime, PaymentMethods

QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InZvcDh4ZS0wMCIsInVzZXJfaWQiOiI3OTkyMTY5MjUzOSIsInNlY3JldCI6IjQxZDhlODA0ZTY1OTJkODA1YWRiZjQxZmEzZTc0YmE5M2MzN2E0YTgxOWViMDI5Y2Y2NDNlOGUwMDkwNzVmOGIifX0="

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

# Выставим счет на сумму 228 рублей который будет работать 45 минут
new_bill = p2p.bill(amount=150, lifetime=30)

print(new_bill.bill_id, new_bill.pay_url)

# Проверим статус выставленного счета
print(p2p.check(bill_id=new_bill.bill_id).status)