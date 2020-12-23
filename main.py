import numpy as np
import numpy_financial as npf
import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce

from read import init_portfolio


today = datetime.datetime.now()
from_date = today + relativedelta(months=-13)

portfolio = init_portfolio('iouu')

print(portfolio)

for i in range(58):
    curr_date = from_date + relativedelta(weeks=+i)
    print(curr_date)
    print('\t {:.2f}'.format( portfolio.get_balance_at(curr_date)) )



