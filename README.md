# Major's random stock scripts

This is a collection of random scripts that I use for managing stock and
option investments.

## put_finder.py

The `put_finder.py` script searches for put options to sell that meet your
annual return requirements. The returns are calculated like this:

```
return = bid_price / (strike_price - bid_price)
annualized_return = return * DTE * 365
```

The script uses TD Ameritrade's API to get information about option data.
Authentication is a little unusual, so [follow the guide provided here]. When
you're finished, you should have a `refresh_token` in a credentials file.

Create a small YAML file called `creds.yaml` that looks like:

```yaml
client_id: <from your TDA developer account>
refresh_token: <from the authentication steps linked above>
```

[follow the guide provided here]: https://github.com/areed1192/td-ameritrade-python-api#api-key-and-credentials

The script takes a few arguments:

```
➜ ./put_finder.py --help
usage: put_finder.py [-h] [--credentials-path CREDENTIALS_PATH] [--pop-min POP_MIN] [--pop-max POP_MAX] [--min-return MIN_RETURN] [--dte-max DTE_MAX] ticker

Find options that meet an annual rate of return requirement

positional arguments:
  ticker                Stock ticker symbol

optional arguments:
  -h, --help            show this help message and exit
  --credentials-path CREDENTIALS_PATH
                        TD Ameritrade Credentials Path (default: ./creds.yaml)
  --pop-min POP_MIN     Minimum percent chance of profit (default: 70)
  --pop-max POP_MAX     Maximum percent chance of profit (default: 90)
  --min-return MIN_RETURN
                        Minimum annual return percentage (default: 20)
  --dte-max DTE_MAX     Maximum days until expiration (default: 60)

```

Let's say you're interested in TSLA options that:

* Expire in 21 days or less
* Have a chance of profit somewhere in the 75-85% range
* Have an annualized return over 20%

Run the script like this:

```
| 💸                |   Strike | Exp Date   |   DTE |   Bid |   PoP % |   Ret. % |   Annual % |
|:------------------|---------:|:-----------|------:|------:|--------:|---------:|-----------:|
| TSLA_010821P695   |    695   | 2021-01-08 |     4 |  7.6  |    76.1 |      1.1 |      100.9 |
| TSLA_010821P692.5 |    692.5 | 2021-01-08 |     4 |  7.1  |    77.4 |      1   |       94.5 |
| TSLA_010821P690   |    690   | 2021-01-08 |     4 |  6.65 |    78.7 |      1   |       88.8 |
| TSLA_010821P687.5 |    687.5 | 2021-01-08 |     4 |  6.25 |    79.8 |      0.9 |       83.7 |
| TSLA_010821P685   |    685   | 2021-01-08 |     4 |  5.85 |    81   |      0.9 |       78.6 |
| TSLA_010821P682.5 |    682.5 | 2021-01-08 |     4 |  5.45 |    82.1 |      0.8 |       73.5 |
| TSLA_010821P680   |    680   | 2021-01-08 |     4 |  5.2  |    83   |      0.8 |       70.3 |
| TSLA_010821P677.5 |    677.5 | 2021-01-08 |     4 |  4.8  |    84   |      0.7 |       65.1 |
| TSLA_011521P675   |    675   | 2021-01-15 |    11 | 12.25 |    76.6 |      1.8 |       61.3 |
| TSLA_010821P675   |    675   | 2021-01-08 |     4 |  4.5  |    85   |      0.7 |       61.2 |
| TSLA_011521P670   |    670   | 2021-01-15 |    11 | 11.2  |    78.3 |      1.7 |       56.4 |
| TSLA_012221P667.5 |    667.5 | 2021-01-22 |    18 | 16.9  |    75.2 |      2.6 |       52.7 |
| TSLA_011521P665   |    665   | 2021-01-15 |    11 | 10.3  |    79.8 |      1.6 |       52.2 |
| TSLA_012221P665   |    665   | 2021-01-22 |    18 | 16.25 |    75.9 |      2.5 |       50.8 |
| TSLA_012221P662.5 |    662.5 | 2021-01-22 |    18 | 15.65 |    76.6 |      2.4 |       49.1 |
| TSLA_011521P660   |    660   | 2021-01-15 |    11 |  9.4  |    81.3 |      1.4 |       47.9 |
| TSLA_012221P660   |    660   | 2021-01-22 |    18 | 15.1  |    77.3 |      2.3 |       47.5 |
| TSLA_012221P657.5 |    657.5 | 2021-01-22 |    18 | 14.55 |    78   |      2.3 |       45.9 |
| TSLA_011521P655   |    655   | 2021-01-15 |    11 |  8.65 |    82.7 |      1.3 |       44.4 |
| TSLA_012221P655   |    655   | 2021-01-22 |    18 | 14    |    78.7 |      2.2 |       44.3 |
| TSLA_012221P652.5 |    652.5 | 2021-01-22 |    18 | 13.5  |    79.4 |      2.1 |       42.8 |
| TSLA_011521P650   |    650   | 2021-01-15 |    11 |  8.05 |    83.9 |      1.3 |       41.6 |
| TSLA_012221P650   |    650   | 2021-01-22 |    18 | 12.95 |    80   |      2   |       41.2 |
| TSLA_012221P647.5 |    647.5 | 2021-01-22 |    18 | 12.55 |    80.7 |      2   |       40.1 |
| TSLA_012221P645   |    645   | 2021-01-22 |    18 | 12.05 |    81.3 |      1.9 |       38.6 |
| TSLA_012221P642.5 |    642.5 | 2021-01-22 |    18 | 11.65 |    81.9 |      1.8 |       37.4 |
| TSLA_012221P640   |    640   | 2021-01-22 |    18 | 11.2  |    82.4 |      1.8 |       36.1 |
| TSLA_012221P637.5 |    637.5 | 2021-01-22 |    18 | 10.75 |    83   |      1.7 |       34.8 |
| TSLA_012221P635   |    635   | 2021-01-22 |    18 | 10.5  |    83.5 |      1.7 |       34.1 |
| TSLA_012221P632.5 |    632.5 | 2021-01-22 |    18 | 10.05 |    84.1 |      1.6 |       32.7 |
| TSLA_012221P630   |    630   | 2021-01-22 |    18 |  9.65 |    84.6 |      1.6 |       31.5 |
```

All of the available puts to sell that meet your requirements are displayed.

[robin-stocks login documentation]: https://robin-stocks.readthedocs.io/en/latest/quickstart.html#importing-and-logging-in
