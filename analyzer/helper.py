from datetime import date
from datetime import datetime
import pprint
from tabulate import tabulate

DATE_FORMAT="%m/%d/%Y"

def getYear(dateStr):
    if dateStr:
        return dateStr[-4:]
    return _getCurrentYear()

def _getCurrentYear():
    #TODO: implement
    return '2016'

def getDays(startDate, endDate):
    start = _getDate(startDate)
    end = _getDate(endDate)
    delta = end-start
    return delta.days

def _getDate(dateVal):
    if not dateVal:
        return datetime.today()
    return datetime.strptime(dateVal, DATE_FORMAT)

def printFloat(descr, value):
    print "%s: %.2f" % (descr, value)
    print

def printTable(l, header):
    print tabulate(l, header, floatfmt=".2f")
    print

def printDict(d, header):
    l = sorted([(k,v) for k,v in d.items()])
    printTable(l, header)

def printDicts(d1, d2, header):
    l = sorted([[k, v, d2.get(k)] for k,v in d1.items()])
    printTable(l, header)
