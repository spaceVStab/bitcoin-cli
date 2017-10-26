# bitcoin-cli
* The command line interface for getting the exchange rates for Bitcoin
* The line interface uses the simple API provided by coindesk.com for Bitcoin Price Index for various countries
* [Updated] Has now feature of historical price of Bitcoin for any currencies; but the limit is only 16 days


# How to use
You need a python3 virtual environment: `virtualenv`
* Installing `virtualenv` : ` sudo pip install virtualenv`
* `virtualenv venv --python=python3`
* `. venv/bin/activate`
* Clone the repository via `git clone https://github.com/spaceVStab/bitcoin-cli.git`.
* `cd bitcoin-cli`
* `pip3 install .`

* Simply run `bitoin-cli` to display the USD exchange rates
* You have to add `--currency inr` for to display INR exchange rates and similarly other countries rates
* You can run `bitcoin-cli --show_country` for displaying the supported country list
* Run `bitcoin-cli --date 10` for displaying past 10 days Bitcoin Price in default USD

* Can be used with virtual environment only till now. Further contribution can be done.
* Further history for bitcoin can be added, different exchange points can also be used, other crypto-currency can be done.
