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
        portifolio_account = []
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
                'value': portfolio.get_deposits_at(curr_date)
            })
            portifolio_debts.append({
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_debt_at(curr_date)
            })
            portifolio_account.append({
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
            {'name': 'Conta', 'series': portifolio_account},
            {'name': 'Alocado', 'series': portifolio_allocated},
        ]

api.add_resource(Portfolio, '/portfolio')

if __name__ == '__main__':
     app.run(port=5002)







