from datetime import date
from datetime import datetime
import pprint

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

def printPercent(descr, num, denom, newLine=False):
    print descr,
    print "{percent:.2%}".format(percent=num/denom)
    _printNewLine(newLine)

def printFloat(descr, value, newLine=False):
    print "%s: %.2f" % (descr, value)
    _printNewLine(newLine)

def printDict(dikt, descr, newLine=True):
    print descr
    pprint.pprint(dikt)
    _printNewLine(newLine)

def _printNewLine(newLine):
    if newLine:
        print ""
