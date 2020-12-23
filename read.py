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


def extract_date_part(datestr):
    date_part = datestr.split('T')[0]
    return date_part


def extract_date(datestr):
    date_part = extract_date_part(datestr)
    date = datetime.datetime.strptime(date_part, '%Y-%m-%d')
    return date


def update_iouu_payments(portfolio):

    with open('data/iouu/202012/wallet.json') as json_file:
        data = json.load(json_file)
        visited_transactions = set()
        balance = 0

        transactions = []

        for i in data:
            transactions = transactions + i['Operacoes']

        transactions.sort(key=(lambda tx: extract_date(tx['Data'])))
        daily_balance = {}

        for tx in transactions:
            is_payment = tx['Tipo'] == 'PAGAMENTO'
            is_deposit = (tx['Tipo'] == 'DEPOSITO' or tx['Tipo'] == 'TRANSFERENCIA')

            id = tx['id']
            if id not in visited_transactions:
                visited_transactions.add(id)
                balance += tx['Valor']
                date_key = extract_date_part(tx['Data'])
                daily_balance[date_key] = {
                    'date':  extract_date(tx['Data']),
                    'value': balance
                }

                print('\t{}'.format(tx['Valor']))
                print('{}'.format(balance))
                if is_payment:
                    date = extract_date(tx['Data'])
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
                    date = extract_date(tx['Data'])
                    value = tx['Valor']
                    deposit = Deposit(id, date, value)
                    portfolio.add_deposit(deposit)

        portfolio.set_daily_balance(daily_balance)