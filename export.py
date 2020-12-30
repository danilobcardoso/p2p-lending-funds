import numpy as np
import numpy_financial as npf
import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce
import csv

from read import init_portfolio

portfolio = init_portfolio('iouu')

with open('data/deposits_iouu.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i, (key, deposit) in enumerate(portfolio.deposits.items()):
        writer.writerow([deposit.id, deposit.date, deposit.value])


with open('data/investments_iouu.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i, (key, investment) in enumerate(portfolio.investments.items()):
        writer.writerow([investment.id, investment.name, investment.rate, investment.periods, investment.date])

with open('data/payments_iouu.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i, (key, investment) in enumerate(portfolio.investments.items()):
        for i, (key, payment) in enumerate(investment.payments.items()):
            writer.writerow([investment.id, investment.name, payment.id, payment.date, payment.sequence, payment.gross_value, payment.interest, payment.taxes])
