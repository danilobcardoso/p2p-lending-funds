import json
import dateutil.parser
import datetime
import os.path
import numpy as np
import numpy_financial as npf
import datetime
import pickle
from dateutil.relativedelta import relativedelta


from data import Portfolio, Investiment, Payment, Deposit


def init_portfolio(platform):
    if os.path.isfile('{}.data'.format(platform)):
        print('File exists. Loading...')
        with open('{}.data'.format(platform), 'rb') as data_file:
            portfolio = pickle.load(data_file)
            return portfolio
    else:
        print('File does not exist. Initializing...')
        return Portfolio(platform)

def update_iouu():
    platform = 'iouu'
    portfolio = init_portfolio(platform)
    with open('data/iouu/202012/investments.json') as json_file:
        data = json.load(json_file)
        for i in data:
            prop = i['SolicitacaoId']
            id = prop["_id"]
            rate = prop['RetornoBrutoMensal']/100
            periods = prop['Prazo']
            name = prop['Empresa']['NomeFantasia']
            amount = i['Valor']
            created = datetime.datetime.strptime(i['Created'], '%Y-%m-%dT%H:%M:%S.%fZ')
            valid = i['AssinouCCB']

            if valid:
                portfolio.add_investment(Investiment(id, name, rate, periods, amount, created))

        update_iouu_payments(portfolio)

    with open('{}.data'.format(platform), 'wb') as data_file:
        pickle.dump(portfolio, data_file)


def update_iouu_payments(portfolio):

    with open('data/iouu/202012/wallet.json') as json_file:
        data = json.load(json_file)

        for i in data:
            for tx in i['Operacoes']:
                is_payment = tx['Tipo'] == 'PAGAMENTO'
                is_deposit = (tx['Tipo'] == 'DEPOSITO' or tx['Tipo'] == 'TRANSFERENCIA')

                id = tx['id']
                if is_payment:
                    date = datetime.datetime.strptime(tx['Data'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    inv_id = tx['Detalhes']['Pagamento']['SolicitacaoId']
                    gross_value = tx['Detalhes']['Pagamento']['ValorBruto']
                    period = tx['Detalhes']['Pagamento']['IndiceParcela']
                    interest = 0
                    if 'Ipmt' in tx['Detalhes']['Pagamento']:
                        interest = tx['Detalhes']['Pagamento']['Ipmt']
                    taxes = 0
                    if 'Ir' in tx['Detalhes']['Pagamento']:
                        taxes = tx['Detalhes']['Pagamento']['Ir']

                    pmt = Payment(id, inv_id, date, period, gross_value, interest, taxes)

                    portfolio.investments[inv_id].add_payment(pmt)
                elif is_deposit:
                    date_part = tx['Data'].split('T')[0]
                    date = datetime.datetime.strptime(date_part, '%Y-%m-%d')
                    value = tx['Valor']
                    deposit = Deposit(id, date, value)
                    portfolio.add_deposit(deposit)
        return data