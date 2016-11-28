from datetime import date
from datetime import datetime

DATE_FORMAT="%m/%d/%Y"

def getDays(startDate, endDate):
    start = _getDate(startDate)
    end = _getDate(endDate)
    delta = end-start
    return delta.days

def _getDate(dateVal):
    if not dateVal:
        return datetime.today()
    return datetime.strptime(dateVal, DATE_FORMAT)
