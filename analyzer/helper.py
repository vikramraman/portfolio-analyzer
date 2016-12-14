from datetime import date
from datetime import datetime
import pprint
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
    return dateStr[-4:] if dateStr else _get_current_year()

def _get_current_year():
    #TODO: implement
    return '2016'

def get_days(startDate, endDate):
    delta = _get_date(endDate) - _get_date(startDate)
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
