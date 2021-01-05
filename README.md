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

The `get_tda_token.py` script will generate the `creds.yaml` that contains
your `client_id` and `refresh_token` that are required for the script to work.
See the comments in the script for the steps required for creating a TD
Ameritrade developer account.

The main script takes a few arguments:

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
* Have an annualized return over 50%

Run the script like this:

```
➜ ./put_finder.py --pop-min 75 --pop-max 85 --min-return 50 --dte-max 21 TSLA
| 💸                |   Strike | Exp Date   |   DTE |   Bid |   PoP % |   Ret. % |   Annual % |
|:------------------|---------:|:-----------|------:|------:|--------:|---------:|-----------:|
| TSLA_010821P710   |    710   | 2021-01-08 |     3 |  5.7  |    75.9 |      0.8 |       98.5 |
| TSLA_010821P707.5 |    707.5 | 2021-01-08 |     3 |  5.15 |    77.7 |      0.7 |       89.2 |
| TSLA_010821P705   |    705   | 2021-01-08 |     3 |  4.7  |    79.3 |      0.7 |       81.7 |
| TSLA_010821P702.5 |    702.5 | 2021-01-08 |     3 |  4.3  |    80.9 |      0.6 |       74.9 |
| TSLA_010821P700   |    700   | 2021-01-08 |     3 |  3.95 |    82.3 |      0.6 |       69   |
| TSLA_010821P697.5 |    697.5 | 2021-01-08 |     3 |  3.55 |    83.8 |      0.5 |       62.2 |
| TSLA_011521P690   |    690   | 2021-01-15 |    10 | 11.05 |    75.6 |      1.6 |       59.4 |
| TSLA_010821P695   |    695   | 2021-01-08 |     3 |  3.3  |    85   |      0.5 |       58   |
| TSLA_011521P685   |    685   | 2021-01-15 |    10 | 10    |    77.6 |      1.5 |       54.1 |
```

All of the available puts to sell that meet your requirements are displayed.

[robin-stocks login documentation]: https://robin-stocks.readthedocs.io/en/latest/quickstart.html#importing-and-logging-in
