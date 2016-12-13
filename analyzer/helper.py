from datetime import date
from datetime import datetime
import pprint
from tabulate import tabulate

DATE_FORMAT="%m/%d/%Y"

def get_year(dateStr):
    if dateStr:
        return dateStr[-4:]
    return _get_current_year()

def _get_current_year():
    #TODO: implement
    return '2016'

def get_days(startDate, endDate):
    start = _get_date(startDate)
    end = _get_date(endDate)
    delta = end-start
    return delta.days

def _get_date(dateVal):
    if not dateVal:
        return datetime.today()
    return datetime.strptime(dateVal, DATE_FORMAT)

def print_float(descr, value):
    print "%s: %.2f" % (descr, value)
    print

def print_table(l, header):
    print tabulate(l, header, floatfmt=".2f")
    print

def print_dict(d, header):
    l = sorted([(k,v) for k,v in d.items()])
    print_table(l, header)

def print_dicts(d1, d2, header):
    l = sorted([[k, v, d2.get(k)] for k,v in d1.items()])
    print_table(l, header)
