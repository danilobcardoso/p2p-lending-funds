import numpy as np
import numpy_financial as npf
import datetime
from dateutil.relativedelta import relativedelta

from read import init_portfolio

today = datetime.datetime.now()
from_date = today + relativedelta(years=-1)

portfolio = init_portfolio('iouu')

for i in range(53):
    curr_date = from_date + relativedelta(weeks=+i)
    print(curr_date)
    print('\t {:.2f}'.format( portfolio.get_value_at(curr_date)) )
    print('\t {:.2f}'.format( portfolio.get_deposits_at(curr_date)) )

