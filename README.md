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

The script uses Robinhood's unofficial APIs to get information about option
data. Start by creating a `~/.robinhood.json` file that contains the
following:

```json
{
  "login": "",
  "password": "",
  "totp": ""
}
```

Your login/password are what you normally use to login at robinhood.com. The
TOTP is your alphanumberic 2FA token. This is displayed when you first
configure 2FA at Robinhood. Refer to the [robin-stocks login documentation] if
you need help logging in.

The script takes a few arguments:

```
./put_finder.py --help
usage: put_finder.py [-h] [--pop-min POP_MIN] [--pop-max POP_MAX] [--min-return MIN_RETURN] [--dte-max DTE_MAX] ticker

Find options that meet an annual rate of return requirement

positional arguments:
  ticker                Stock ticker symbol

optional arguments:
  -h, --help            show this help message and exit
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
$ ./put_finder.py --pop-min 75 --pop-max 85 --min-return 20 --dte-max 21 TSLA

|      |   Strike | Exp Date   |   DTE |   PoP % |   Delta |   Ret. % |   Annual %  |
|------|----------|------------|-------|---------|---------|----------|-------------|
| TSLA |    672.5 | 2021-01-08 |     6 |    75.6 |    0.28 |      1.7 |       100.7 |
| TSLA |    670   | 2021-01-08 |     6 |    76.4 |    0.26 |      1.6 |        95.9 |
| TSLA |    667.5 | 2021-01-08 |     6 |    77.3 |    0.25 |      1.5 |        89.7 |
| TSLA |    665   | 2021-01-08 |     6 |    78.1 |    0.24 |      1.4 |        84.4 |
| TSLA |    662.5 | 2021-01-08 |     6 |    79   |    0.23 |      1.3 |        79.5 |
| TSLA |    660   | 2021-01-08 |     6 |    79.7 |    0.22 |      1.3 |        76.1 |
| TSLA |    657.5 | 2021-01-08 |     6 |    80.6 |    0.21 |      1.2 |        70.7 |
| TSLA |    655   | 2021-01-08 |     6 |    81.4 |    0.19 |      1.1 |        66.7 |
| TSLA |    660   | 2021-01-15 |    13 |    75.3 |    0.27 |      2.3 |        64   |
| TSLA |    652.5 | 2021-01-08 |     6 |    82.1 |    0.18 |      1   |        62.6 |
| TSLA |    650   | 2021-01-08 |     6 |    82.9 |    0.17 |      1   |        59.5 |
| TSLA |    655   | 2021-01-15 |    13 |    76.6 |    0.25 |      2.1 |        58.6 |
| TSLA |    647.5 | 2021-01-08 |     6 |    83.6 |    0.17 |      0.9 |        55.9 |
| TSLA |    650   | 2021-01-15 |    13 |    77.8 |    0.23 |      1.9 |        54.2 |
| TSLA |    645   | 2021-01-08 |     6 |    84.3 |    0.16 |      0.9 |        52.8 |
| TSLA |    647.5 | 2021-01-22 |    20 |    75.1 |    0.26 |      2.8 |        51.7 |
| TSLA |    645   | 2021-01-22 |    20 |    75.6 |    0.25 |      2.7 |        50   |

Options found below annual return threshold of 50%: 24
```

All of the available puts to sell that meet your requirements are displayed.

[robin-stocks login documentation]: https://robin-stocks.readthedocs.io/en/latest/quickstart.html#importing-and-logging-in
