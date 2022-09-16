import os

from dotenv import load_dotenv
from pyqiwip2p import AioQiwiP2P, QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime

load_dotenv()

QIWI_PRIV_KEY = os.getenv('QIWI_PRIV_KEY')


p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)



# Выставим счет на сумму 228 рублей который будет работать 45 минут
new_bill = p2p.bill(amount=228, lifetime=5)

print(new_bill.bill_id, new_bill.pay_url)

# Проверим статус выставленного счета через его bill_id
print(p2p.check(bill_id=new_bill.bill_id).status)

# Или просто передавая сам объект Bill
print(p2p.check(new_bill).status)

# Потеряли ссылку на оплату счета? Не проблема!
# print(p2p.check(bill_id=245532).pay_url)

# Клиент отменил заказ? Тогда и счет надо закрыть
# p2p.reject(bill_id=new_bill.bill_id)

