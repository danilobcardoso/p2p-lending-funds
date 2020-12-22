import numpy as np
import numpy_financial as npf
import datetime
from dateutil.relativedelta import relativedelta

from data import Investiment, get_interval_in_months
from read import load_portfolio_from_iouu, load_payments_from_iouu


from_date = datetime.datetime(2019, 10, 22)

portfolio = load_portfolio_from_iouu()

for i in range(70):
    curr_date = from_date + relativedelta(weeks=+i)
    print(curr_date)
    print('\t {}'.format( portfolio.get_value_at(curr_date)) )

