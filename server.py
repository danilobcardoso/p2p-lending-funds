from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import numpy as np
import numpy_financial as npf
import datetime
import json
from dateutil.relativedelta import relativedelta

from data import Investiment, get_interval_in_months
from read import init_portfolio

app = Flask(__name__)
CORS(app)
api = Api(app)


class Portfolio(Resource):
    def get(self):
        today = datetime.datetime.now()
        from_date = today + relativedelta(months=-12)
        portfolio = init_portfolio('iouu')
        portifolio_debts = []
        portifolio_value = []
        portifolio_cash = []
        portifolio_allocated = []
        portifolio_deposits = []

        for i in range(52):
            curr_date = from_date + relativedelta(weeks=+i)

            portifolio_value.append( {
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_value_at(curr_date)
            } )
            portifolio_deposits.append( {
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.sum_deposits_until(curr_date)
            })
            portifolio_debts.append({
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_debt_at(curr_date)
            })
            portifolio_cash.append({
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_balance_at(curr_date)
            })
            portifolio_allocated.append({
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_allocated_at(curr_date)
            })

        return [
            { 'name': 'Valor do portifólio', 'series': portifolio_value },
            {'name': 'Depositos', 'series': portifolio_deposits},
            {'name': 'Débitos', 'series': portifolio_debts},
            {'name': 'Conta', 'series': portifolio_cash},
            {'name': 'Alocado', 'series': portifolio_allocated},
        ]


class Returns(Resource):
    def get(self):
        portfolio = init_portfolio('iouu')
        today = datetime.datetime.now()
        from_date = today + relativedelta(months=-12)
        data = portfolio.calc_quota_value(from_date, today)
        daily_returns = []
        for daily_data in data:
            daily_returns.append({
                'name': daily_data['date'].strftime("%d/%m/%Y"),
                'value': daily_data['quota_value']
            })

        return [
            {'name': 'Valor da cota', 'series': daily_returns}
        ]



api.add_resource(Portfolio, '/portfolio')
api.add_resource(Returns, '/returns')

if __name__ == '__main__':
     app.run(port=5002)







