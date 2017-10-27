#!/usr/bin/env python
# encoding: utf-8


"""
CLI to provide exchange rates for bitcoin.
Uses Coindesk API to get the rates.
NEW: Possibility to get historical prices for bitcoin (limit up to 16 days)
NEW:
  Possibility to get exchange rates for other crypto currencies.
  Uses CoinMarketCap API to get the rates.
  WARNING: the rates, via this API, are limited to a number of currencies
"""

import click
import datetime
import requests


BPI_API = 'https://api.coindesk.com/v1/bpi'
CMC_API = 'https://api.coinmarketcap.com/v1/ticker'


def get_bpi(currency):
    """Get BTC exchange rate with another currency"""

    url = '{api}/currentprice/{currency}.json'
    url = url.format(api=BPI_API, currency=currency)
    bpi_response = requests.get(url)
    bpi_response.raise_for_status()
    bpi_json = bpi_response.json()
    return bpi_json['bpi'][currency]['rate_float']


def get_historical_bpi(date, currency):
    """Get historical prices for BTC with another currency"""

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    past = datetime.datetime.now() - datetime.timedelta(days=date)
    last_date = past.strftime('%Y-%m-%d')
    url = '{}/historical/close.json'.format(BPI_API)
    bpi_hist_response = requests.get(
        url,
        params={
            'start': last_date,
            'end': today,
            'currency': currency
            }
        )
    bpi_hist_response.raise_for_status()
    bpi_hist_json = bpi_hist_response.json()
    return bpi_hist_json['bpi']


def get_cmc(crypto_currency, currency):
    """Get crypto_currency exchange rate with currency via CMC_API"""

    response = requests.get(CMC_API)
    response.raise_for_status()
    for info in response.json():
        # since CMC_API looks for crypto currencies by id (e.g. 'bitcoin')
        # instead of symbol (e.g. 'BTC'), we search for the id at the index
        # of the API
        if info['symbol'] == crypto_currency:
            crypto_currency_id = info['id']
            # we then ask for the exchange rate in the specified currency
            response = requests.get(
                '{api}/{id}'.format(api=CMC_API, id=crypto_currency_id),
                params={'convert': currency}
                )
            response.raise_for_status()  # breaks the loop and exits
            info = response.json().pop()
            param = 'price_{}'.format(currency.lower())
            return info['name'], info[param]  # exits altogether


def print_hist_bpi(hist_bpi):
    hist_bpi_sort = sorted(hist_bpi.items())
    for i in hist_bpi_sort:
        print(i[0], "  ::  ", i[1])


@click.command()
@click.option('--currency', default='USD', help='Enter the required currency')
@click.option(
    '--show_country',
    is_flag=True,
    help='List the supported countries')
@click.option(
    '--date',
    default='-1',
    help=('Enter the number of days '
          'to look back from today (not more than 16 days)'
          ))
@click.option(
    '--crypto_currency',
    default='BTC',
    help='Get exchange rate for another crypto currency')
def cli(currency, show_country, date, crypto_currency):
    date = int(date)
    if date is not -1:
        if crypto_currency != 'BTC':
            msg = ('We are sorry, we cannot provide '
                   'infos for this crypto currency\n')
            click.echo(msg)
        else:
            currency = currency.upper()
            click.echo("Welcome to BPI\n\n")
            hist_bpi = get_historical_bpi(date, currency)
            print_hist_bpi(hist_bpi)
    else:
        currency = currency.upper()
        crypto_currency = crypto_currency.upper()
        if crypto_currency == 'BTC':  # use BPI_API
            click.echo("Welcome to BPI\n")
            bpi = get_bpi(currency)
            click.echo("1 Bitcoin for {} {}".format(bpi, currency))
        else:  # use CoinMarketCap
            click.echo('Welcome to CoinMarketCap\n')
            name, cmc = get_cmc(crypto_currency, currency)
            click.echo(
                '1 {name} for {value} {currency}'.format(
                    name=name,
                    value=cmc,
                    currency=currency
                    )
                )

    if show_country:
        country_response = requests.get(
            'https://api.coindesk.com/v1/bpi/supported-currencies.json'
            )
        country_response.raise_for_status()
        country_json = country_response.json()
        for c in country_json:
            print(str(c['currency'])+"  ::  "+str(c['country'])+"\n")

if __name__ == '__main__':
    cli()  # entry point at runtime
