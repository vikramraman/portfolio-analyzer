import csvreader
import helper
import argparse
import os
import sys
import sheetsapi

SYMBOL_IDX=0
QTY_IDX=1
BUY_PRICE_IDX=2
BUY_DATE_IDX=3
SALE_PRICE_IDX=4
SALE_DATE_IDX=5

LONG_TAX_RATE=.15
SHORT_TAX_RATE=.25
CURRENT_SHORT_TAX_RATE=.28
LONG_DAYS=365

STOCK_HEADER = ['YEAR', 'SYMBOL', 'QTY', 'BUY_PRICE', 'SELL_PRICE', 'GROSS_PROFIT', 'NET_PROFIT']
RESULTS_HEADER = ['TOTAL COST', 'TOTAL SALE', 'GROSS PROFIT', 'NET PROFIT', 'GROSS PROFIT %', 'NET PROFIT %']
PROFIT_HEADER = ['YEAR', 'GROSS PROFIT', 'NET PROFIT']

yearly_profits = {}
yearly_taxed_profits = {}
yearly_transactions = {}
total_buy = 0
total_sale = 0
total_net_profit = 0
current_invested = 0

def _analyze(rows):
    global total_buy
    global total_sale
    global total_net_profit
    global current_invested

    if not rows:
        raise StandardError('Invalid data input')

    l = []
    for row in rows:
        symbol = row[SYMBOL_IDX]
        qty = float(row[QTY_IDX])
        buy_rate = float(row[BUY_PRICE_IDX])
        buy_date = row[BUY_DATE_IDX]
        sale_rate = float(row[SALE_PRICE_IDX])
        sale_date = row[SALE_DATE_IDX]

        buy_total = buy_rate * qty
        sale_total = sale_rate * qty
        year = helper.get_year(sale_date)

        profit = sale_total - buy_total
        net_profit = _get_net_profit(profit, buy_date, sale_date)
        total_buy += buy_total
        total_sale += sale_total
        total_net_profit += net_profit

        if not sale_date:
            current_invested += buy_total

        _update_profits(year, yearly_profits, profit)
        _update_profits(year, yearly_taxed_profits, net_profit)
        _update_transactions(buy_date, sale_date, yearly_transactions)
        l.append([year, symbol, qty, buy_rate, sale_rate, profit, net_profit])
    helper.print_table(l, STOCK_HEADER)

def _update_profits(year, yearly_profits, profit):
    sum = yearly_profits.get(year, 0)
    yearly_profits[year] = sum + round(profit, 2)

def _update_transactions(buy_date, sale_date, trans_dict):
    buy_year = helper.get_year(buy_date)
    sale_year = helper.get_year(sale_date)
    _increment_transaction(buy_year, 'bought', trans_dict)
    _increment_transaction(sale_year, 'sold', trans_dict)

def _increment_transaction(year, key, trans_dict):
    dic = trans_dict.get(year, {})
    count = dic.get(key, 0)
    dic[key] = count + 1
    trans_dict[year] = dic

def _get_tax_rate(buy_date, sale_date):
    days_held = helper.get_days(buy_date, sale_date)
    if days_held > LONG_DAYS:
        return LONG_TAX_RATE
    #TODO: compute correctly based on income bracket
    return SHORT_TAX_RATE

def _get_net_profit(profit, buy_date, sale_date):
    tax_rate = _get_tax_rate(buy_date, sale_date)
    if profit <= 0:
        return profit
    return profit - (profit * tax_rate)

def doAnalyze(args):
    csv_dir = args.csvDir
    ids = args.sheets

    if csv_dir:
        if not os.path.isdir(csv_dir):
            print "Invalid input: Please enter a valid directory: %s" % csv_dir
            sys.exit(1)
        _parse_csv(csv_dir)
    if ids:
        _parse_sheets(ids)
    _pprint_data()

def _parse_sheets(ids):
    if len(ids) == 1:
        ids = ids[0].split(',')
    for sheetID in ids:
        data = sheetsapi.parse_spreadsheet(sheetID)
        if not data:
            continue
        _analyze(data)

def _parse_csv(csv_dir):
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            data = csvreader.read(csv_dir + "/" + file)
            _analyze(data)

def _get_percent(num, denom):
    if denom == 0:
        return '0%'
    return "{percent:.2%}".format(percent=num/denom)

def _print_transactions(d, header):
    l = sorted([[k, v.get('bought', '-'), v.get('sold', '-')] for k,v in d.items()])
    helper.print_table(l, header)

def _pprint_data():
    total_profit = total_sale - total_buy
    gross_percent = _get_percent(total_profit, total_buy)
    net_percent = _get_percent(total_net_profit, total_buy)
    table = [[total_buy, total_sale, total_profit, total_net_profit, gross_percent, net_percent]]
    helper.print_table(table, RESULTS_HEADER)
    helper.print_dicts(yearly_profits, yearly_taxed_profits, PROFIT_HEADER)
    _print_transactions(yearly_transactions, ['YEAR', 'BUYS', 'SALES'])
    helper.print_float("CURRENT INVESTMENTS", current_invested)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--csvDir', type=str, nargs='?', help='CSV directory')
    parser.add_argument('--sheets', metavar='ID', type=str, nargs='+', help='Google spreadsheet IDs')
    args = parser.parse_args()

    if not (args.csvDir or args.sheets):
        parser.error('csvDir or sheets must be provided.')
    doAnalyze(args)
