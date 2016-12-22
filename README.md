# Simple Portfolio Analyzer

An application to analyze the performance of a stock portfolio. Supports CSV and Google spreadsheet data sources.

## Installation
```pip install tabulate```

```pip install --upgrade google-api-python-client```

## Usage
```python analyzer.py --sheets={google_sheet_id} --conf=../tests/sheet.properties```

```python analyzer.py --csvDir=../tests --conf=../tests/csv.properties```

## Configuration
The input data source must contain the following fields:

Symbol: The stock symbol
Qty: Quantity of shares purchased
Buy price: The purchase price per share
Buy date: The date shares were purchased
Sale price: The sale price
Sale date: The sale date (Optional - can be empty)

The input configuration file maps the column indices for the above fields in the input data source. Please refer to tests/csv.properties and tests/sheet.properties for examples.

## Results
The output contains several useful components.

### Individual stock summary including annualized returns

```
YEAR  SYMBOL       QTY    BUY_PRICE    SELL_PRICE    GROSS_PROFIT    NET_PROFIT    GROSS PROFIT %    ANNUAL %
------  --------  ------  -----------  ------------  --------------  ------------  ----------------  ----------
 2009  MGC        15.00        28.93         33.79           72.90         54.67             16.80       16.80
 2011  GOOG        5.00       337.51        593.15         1278.20       1086.47             75.74       20.68
 2015  C         100.00        35.25         53.55         1830.00       1555.50             51.91        6.16
 2012  AAPL        9.00       366.60        472.90          956.70        717.52             29.00       29.00
 2016  KO        100.00        38.00         46.43          843.00        716.55             22.18        6.91
 ```

### Total performance benchmarked against popular indices (configurable).

```
 TOTAL COST    TOTAL SALE    GROSS PROFIT    NET PROFIT  GROSS PROFIT %    NET PROFIT %      SPY %    RUSSELL 2000 %
------------  ------------  --------------  ------------  ----------------  --------------  -------  ----------------
 12237.16     14352.25        2115.09      1576.23  17.29%            12.89%            13.83             13.48
 ```
### Yearly Performance: Unsold stocks are hypothetically sold in the current year to compute performance.

```
 YEAR    GROSS PROFIT    NET PROFIT
------  --------------  ------------
 2009          701.15        525.86
 2011         1278.20       1086.47
 2012         3772.00       3064.52
 2016         3609.59       1138.73
```

### Yearly Transactions

```
YEAR  BUYS    SALES
------  ------  -------
2009  5       2
2010  -       1
2011  3       1
2014  5       -
2015  3       4
2016  5       10
```
