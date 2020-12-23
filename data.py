import numpy as np
import numpy_financial as npf
from datetime import timedelta
from functools import reduce
from dateutil.relativedelta import relativedelta

def get_interval_in_months(from_date, to_date):
    periods = to_date.month+(to_date.year*12) - (from_date.month+(from_date.year*12))
    if from_date.day > to_date.day:
        periods = periods - 1
    return periods

def before(from_date, to_date):
    return to_date < from_date

def apply_rate(days, amount, rate):
    return amount * np.power(1+rate, days/30.41)



class Portfolio:
    def __init__(self, platform):
        self.platform = platform
        self.investments = {}
        self.deposits = {}
        self.daily_balance = {}


    def add_investment(self, investment):
        if investment.id not in self.investments:
            self.investments[investment.id] = investment

    def add_deposit(self, deposit):
        if deposit.id not in self.deposits:
            self.deposits[deposit.id] = deposit

    def set_daily_balance(self, daily_balance):
        self.daily_balance = daily_balance

    def get_value_at(self, date):
        total = self.get_allocated_at(date)
        total += self.get_balance_at(date)
        return total

    def get_allocated_at(self, date):
        total = 0
        for i, (key, investment) in enumerate(self.investments.items()):
            total += investment.get_value_at(date)
        return total

    def get_debt_at(self, date):
        total = 0
        for i, (key, investment) in enumerate(self.investments.items()):
            a, b = investment.get_debt_at(date)
            total += a
        return total

    def get_balance_at(self, date):
        daily_balance =  list(self.daily_balance.values())
        daily_balance.sort(key=lambda b: b['date'])
        last_balance = 0
        for balance in daily_balance:
            if balance['date'] > date:
                break
            last_balance = balance['value']
        return last_balance

    def get_deposits_at(self, date):
        total = 0

        for i, (key, deposit) in enumerate(self.deposits.items()):
            if deposit.date < date:
                total += deposit.value

        return total

    def __str__(self):
        return reduce((lambda x, y: x + '\n' + y), map((lambda x: x.id + ' - ' + x.name), self.investments.values()))

    def __repr__(self):
        return self.__str__()

class Investiment:
    def __init__(self, id, name, rate, periods, amount, date):
        self.id = id
        self.name = name
        self.rate = rate
        self.periods = periods
        self.amount = amount
        self.date = date
        self.delay = 10
        self.payments = {}

    def get_payment(self):
        return npf.pmt(self.rate, self.periods, self.amount)

    def get_payments_at(self, date):
        if before(self.date, date):
            return 0.0

        total_paid = 0

        for i, (key, payment) in enumerate(self.payments.items()):
            if payment.date < date:
                total_paid += payment.principal

        return total_paid

    def get_value_at(self, date):
        if before(self.date, date):
            return 0.0

        currente_debt, _ = self.get_debt_at(date)
        risk = 1 - self.get_risk_at(date)
        return currente_debt * risk

    def get_risk_at(self, date):
        paid = self.get_payments_at(date)
        planned = -self.get_planned_payments_at(date)
        risk = (planned - paid)/ self.amount
        risk = min(1.0, risk)
        risk = max(0, risk)
        return risk


    def get_planned_payments_at(self, date):
        if before(self.date, date):
            return 0.0
        initial_date = self.date + relativedelta(days= 10 )
        num_intervals = get_interval_in_months(initial_date, date)
        total_paid = 0
        for p in range(num_intervals):
            total_paid += npf.ppmt(self.rate, p+1, self.periods, self.amount)
        return total_paid

    def get_interest_portion_at(self, date):
        if before(self.date, date):
            return 0.0

        num_intervals = get_interval_in_months(self.date, date)
        total_interest = 0
        for p in range(num_intervals):
            total_interest += npf.ipmt(self.rate, p+1, self.periods, self.amount)
        return total_interest

    def add_payment(self, payment):
        if payment.id not in self.payments:
            self.payments[payment.id] = payment


    def get_debt_at(self, date):
        if before(self.date, date):
            return 0.0, {}

        payment_list = list(self.payments.values())
        payment_list.sort(key=(lambda p: p.date))

        initial_date = self.date + relativedelta(days= 10 )
        final_date = date

        dates = [initial_date]
        values = []
        for payment in payment_list:
            if payment.date < final_date:
                dates.append(payment.date)
                values.append(payment.gross_value)
        dates.append(final_date)
        values.append(0.0)
        periods = []
        curr_value = self.amount
        for i in range(len(dates)-1):
            begin = dates[i]
            end = dates[i+1]
            num_days = (end - begin).days
            remaining_value = apply_rate(num_days, curr_value, self.rate) - values[i]

            periods.append({
                'begin': begin,
                'end': end,
                'value_begin': curr_value,
                'value_end': remaining_value,
                'value_paid': values[i],
                'num_days': num_days
            })
            curr_value = remaining_value
        return curr_value, periods




    def __str__(self):
        return "{} - ({} @ {}) - payments: {}".format(self.name, self.periods, self.rate, len(self.payments))

    def __repr__(self):
        return self.__str__()


class Payment:
    def __init__(self, id, op_id, date, sequence, gross_value, interest, taxes):
        self.id = id
        self.op_id = op_id
        self.date = date
        self.sequence = sequence
        self.gross_value = gross_value
        self.interest = interest
        self.taxes = taxes
        self.principal = self.gross_value-self.interest


    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.op_id, self.date, self.sequence, self.gross_value, self.interest, self.principal, self.taxes)



    def __repr__(self):
        return self.__str__()


class Deposit:
    def __init__(self, id, date, value):
        self.id = id
        self.date = date
        self.value = value

