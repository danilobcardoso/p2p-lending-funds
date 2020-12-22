from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import numpy as np
import numpy_financial as npf
import datetime
import json
from dateutil.relativedelta import relativedelta

from data import Investiment, get_interval_in_months
from read import load_portfolio_from_iouu, load_payments_from_iouu

app = Flask(__name__)
CORS(app)
api = Api(app)


class Portfolio(Resource):
    def get(self):
        from_date = datetime.datetime(2019, 10, 22)
        portfolio = load_portfolio_from_iouu()
        portifolio_value = []
        portifolio_deposits = []

        for i in range(53):
            curr_date = from_date + relativedelta(weeks=+i)
            portifolio_value.append( {
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_value_at(curr_date)
            } )
            portifolio_deposits.append( {
                'name': curr_date.strftime("%d/%m/%Y"),
                'value': portfolio.get_deposits_at(curr_date)
            })

        return [{ 'name': 'Valor do portifólio', 'series': portifolio_value }, {'name': 'Depositos', 'series': portifolio_deposits} ]

api.add_resource(Portfolio, '/portfolio')

if __name__ == '__main__':
     app.run(port=5002)







