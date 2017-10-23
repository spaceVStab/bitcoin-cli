import requests
import click

def get_bpi(currency):
	url = 'https://api.coindesk.com/v1/bpi/currentprice/{}.json'.format(currency)
	#print(url)
	bpi_response = requests.get(url)
	bpi_response.raise_for_status()
	bpi_json = bpi_response.json()
	return bpi_json['bpi'][currency]['rate_float']

@click.command()
@click.option('--currency', default='USD', help='Enter the required currency')
@click.option('--show_country', is_flag = True, help = 'List the supported countries')
def cli(currency, show_country):
	currency = currency.upper()
	click.echo("Welcome to BPI\n\n")
	bpi = get_bpi(currency)
	click.echo("1 Bitcoin for {} {}".format(bpi,currency))

	if show_country:
		country_response = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')
		country_response.raise_for_status()	
		country_json = country_response.json()
		for c in country_json:
			print(str(c['currency'])+"  ::  "+str(c['country'])+"\n")