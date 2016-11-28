import csvreader
import helper

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

def analyze(rows):
    if not rows:
        raise "Invalid data input"

    totalBuy = 0
    totalSale = 0
    totalTaxedProfit = 0
    for row in rows:
        symbol = row[SYMBOL_IDX]
        qty = float(row[QTY_IDX])
        buyRate = float(row[BUY_PRICE_IDX])
        buyDate = row[BUY_DATE_IDX]
        saleRate = float(row[SALE_PRICE_IDX])
        saleDate = row[SALE_DATE_IDX]

        buyTotal = buyRate * qty
        saleTotal = saleRate * qty
        profit = saleTotal - buyTotal
        taxedProfit = _getTaxedProfit(profit, buyDate, saleDate)
        totalBuy += buyTotal
        totalSale += saleTotal
        totalTaxedProfit += taxedProfit
        print symbol, qty, buyRate, saleRate, profit, taxedProfit
    print totalBuy, totalSale, (totalSale-totalBuy), totalTaxedProfit

def _getTaxRate(buyDate, saleDate):
    daysHeld = helper.getDays(buyDate, saleDate)
    if daysHeld > LONG_DAYS:
        return LONG_TAX_RATE
    #TODO: compute correctly based on income bracket
    return SHORT_TAX_RATE

def _getTaxedProfit(profit, buyDate, saleDate):
    taxRate = _getTaxRate(buyDate, saleDate)
    if profit <= 0:
        return profit
    return profit - (profit * taxRate)

if __name__ == "__main__":
    #TODO: move into test code
    data = csvreader.read("./tests/sample.csv")
    analyze(data)
