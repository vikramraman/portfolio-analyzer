import csvreader
import helper
import argparse
import os
import sys

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

yearlyProfits = {}
yearlyTaxedProfits = {}
yearlyTransactions = {}
totalBuy = 0
totalSale = 0
totalNetProfit = 0
currentInvested = 0

def _analyze(rows):
    global totalBuy
    global totalSale
    global totalNetProfit
    global currentInvested

    if not rows:
        raise "Invalid data input"

    for row in rows:
        symbol = row[SYMBOL_IDX]
        qty = float(row[QTY_IDX])
        buyRate = float(row[BUY_PRICE_IDX])
        buyDate = row[BUY_DATE_IDX]
        saleRate = float(row[SALE_PRICE_IDX])
        saleDate = row[SALE_DATE_IDX]

        buyTotal = buyRate * qty
        saleTotal = saleRate * qty
        year = helper.getYear(saleDate)

        profit = saleTotal - buyTotal
        netProfit = _getNetProfit(profit, buyDate, saleDate)
        totalBuy += buyTotal
        totalSale += saleTotal
        totalNetProfit += netProfit

        if not saleDate:
            currentInvested += buyTotal

        _updateProfits(year, yearlyProfits, profit)
        _updateProfits(year, yearlyTaxedProfits, netProfit)
        _updateTransactions(buyDate, saleDate, yearlyTransactions)
        print year, symbol, qty, buyRate, saleRate, profit, netProfit

def _updateProfits(year, yearlyProfits, profit):
    sum = yearlyProfits.get(year, 0)
    yearlyProfits[year] = sum + round(profit, 2)

def _updateTransactions(buyDate, saleDate, transDict):
    buyYear = helper.getYear(buyDate)
    saleYear = helper.getYear(saleDate)
    _incrementTransaction(buyYear, 'bought', transDict)
    _incrementTransaction(saleYear, 'sold', transDict)

def _incrementTransaction(year, key, transDict):
    dic = transDict.get(year, {})
    count = dic.get(key, 0)
    dic[key] = count + 1
    transDict[year] = dic

def _getTaxRate(buyDate, saleDate):
    daysHeld = helper.getDays(buyDate, saleDate)
    if daysHeld > LONG_DAYS:
        return LONG_TAX_RATE
    #TODO: compute correctly based on income bracket
    return SHORT_TAX_RATE

def _getNetProfit(profit, buyDate, saleDate):
    taxRate = _getTaxRate(buyDate, saleDate)
    if profit <= 0:
        return profit
    return profit - (profit * taxRate)

def doAnalyze(args):
    csvDir = args.csvDir
    if not os.path.isdir(csvDir):
        print "Invalid input: Please enter a valid directory"
        sys.exit(1)

    for file in os.listdir(csvDir):
        if file.endswith(".csv"):
            data = csvreader.read(csvDir + "/" + file)
            _analyze(data)
    _pprintData()

def _pprintData():
    print "\nResults:\n"
    totalProfit = totalSale - totalBuy
    helper.printFloat("Total Cost", totalBuy)
    helper.printFloat("Total Sale", totalSale)
    helper.printFloat("Gross Profit", totalProfit)
    helper.printFloat("Net Profit", totalNetProfit)
    helper.printPercent("Gross profit %:", totalProfit, totalBuy)
    helper.printPercent("Net profit %:", totalNetProfit, totalBuy, True)
    helper.printFloat("Outstanding investments", currentInvested, True)
    helper.printDict(yearlyProfits, "Gross profits:")
    helper.printDict(yearlyTaxedProfits, "Net profits:")
    helper.printDict(yearlyTransactions, "Transactions:")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csvDir', metavar='csvDir', type=str, help='CSV directory')
    args = parser.parse_args()
    doAnalyze(args)
