import numpy as np
import numpy_financial as npf
from datetime import timedelta

def get_interval_in_months(from_date, to_date):
    periods = to_date.month+(to_date.year*12) - (from_date.month+(from_date.year*12))
    if from_date.day > to_date.day:
        periods = periods - 1
    return periods

def before(from_date, to_date):
    return to_date < from_date



class Portfolio:
    def __init__(self, platform):
        self.platform = platform
        self.investments = {}
        self.deposits = {}


    def add_investment(self, investment):
        if investment.id not in self.investments:
            self.investments[investment.id] = investment

    def add_deposit(self, deposit):
        if deposit.id not in self.deposits:
            self.deposits[deposit.id] = deposit

    def get_value_at(self, date):
        total = 0
        for i, (key, investment) in enumerate(self.investments.items()):
            total += investment.get_value_at(date)
        return total

    def get_deposits_at(self, date):
        total = 0

        for i, (key, deposit) in enumerate(self.deposits.items()):
            if deposit.date < date:
                total += deposit.value

        return total

class Investiment:
    def __init__(self, id, name, rate, periods, amount, date):
        self.id = id
        self.name = name
        self.rate = rate
        self.periods = periods
        self.amount = amount
        self.date = date
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
        payments = self.get_payments_at(date)
        return self.amount - payments


    def get_planned_payments_at(self, date):
        if before(self.date, date):
            return 0.0

        num_intervals = get_interval_in_months(self.date, date)
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

class Deposit:
    def __init__(self, id, date, value):
        self.id = id
        self.date = date
        self.value = value

