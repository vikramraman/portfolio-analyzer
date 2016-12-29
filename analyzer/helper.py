from datetime import date
from datetime import datetime
import pprint
import math
import ConfigParser
from tabulate import tabulate

DATE_FORMAT = "%m/%d/%Y"
SECTION_NAME = "RowTemplate"
SYMBOL_IDX = "symbol.idx"
QTY_IDX = "qty.index"
BUY_PRICE_IDX = "buy.price.idx"
BUY_DATE_IDX = "buy.date.idx"
SALE_PRICE_IDX = "sale.price.idx"
SALE_DATE_IDX = "sale.date.idx"
PROP_KEYS = [SYMBOL_IDX, QTY_IDX, BUY_PRICE_IDX, BUY_DATE_IDX, SALE_PRICE_IDX, SALE_DATE_IDX]

def get_year(dateStr):
    return dateStr[-4:] if dateStr else get_current_year()

def get_current_year():
    return str(datetime.today().year)

def get_years(start_date, end_date):
    days = get_days(start_date, end_date)
    return 1 if days <= 365 else int(get_year(end_date)) - int(get_year(start_date)) + 1

def get_days(start_date, end_date):
    delta = _get_date(end_date) - _get_date(start_date)
    return delta.days

def _get_date(dateVal):
    return datetime.strptime(dateVal, DATE_FORMAT) if dateVal else datetime.today()

def print_float(descr, value):
    print '%s: %.2f \n' % (descr, value)

def print_table(l, header):
    print tabulate(l, header, floatfmt=".2f"), '\n'

def print_dict(d, header):
    l = sorted([(k,v) for k,v in d.items()])
    print_table(l, header)

def print_dicts(d1, d2, header):
    l = sorted([[k, v, d2.get(k)] for k,v in d1.items()])
    print_table(l, header)

def parse_properties(props_file):
    config = ConfigParser.RawConfigParser()
    config.read(props_file)
    return {k : int( config.get(SECTION_NAME, k) ) for k in PROP_KEYS}

def get_rows(rows, indices):
    values = []
    for row in rows:
        l = [_get_field(row, indices, k) for k in PROP_KEYS]
        if l[0] and l[1]:
            values.append(l)
    return values

def _get_field(row, indices, key):
    try:
        return _strip_currency_symbol(row[indices.get(key)])
    except IndexError:
        return None

def _strip_currency_symbol(data):
    return str(data[1:]) if data and data[0] == '$' else data

def get_annual_rate(buy_rate, sale_rate, years):
    """
    Gets the annual rate of return given the buy price, sell price and years held.
    """
    p = sale_rate/buy_rate
    return ( math.pow(p, 1.0/years)-1.0 ) * 100.0

def get_compound_rate(yearly_returns):
    """
    Computes the geometric average aka compound average rate of return.
    """
    if not yearly_returns:
        return 0.0
    count = float(len(yearly_returns))
    l = [1.0 + (x/100.0) for x in yearly_returns]
    p = reduce(lambda x,y : x * y, l)
    return ( math.pow(p, 1.0/count)-1.0 ) * 100.0
