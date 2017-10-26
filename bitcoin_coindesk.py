import requests
import click
import datetime

def get_bpi(currency):
	url = 'https://api.coindesk.com/v1/bpi/currentprice/{}.json'.format(currency)
	#print(url)
	bpi_response = requests.get(url)
	bpi_response.raise_for_status()
	bpi_json = bpi_response.json()
	return bpi_json['bpi'][currency]['rate_float']

def get_historical_bpi(date,currency):
	today = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
	past = datetime.datetime.now() - datetime.timedelta(days = date)
	last_date = str(past.year)+"-"+str(past.month)+"-"+str(past.day)
	url = 'https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}&currency={}'.format(last_date,today,currency)
	bpi_hist_response = requests.get(url)
	bpi_hist_response.raise_for_status()
	bpi_hist_json = bpi_hist_response.json()
	return bpi_hist_json['bpi']

def print_hist_bpi(hist_bpi):
	hist_bpi_sort = sorted(hist_bpi.items())
	for i in hist_bpi_sort:
		print(i[0],"  ::  ",i[1])

@click.command()
@click.option('--currency', default='USD', help='Enter the required currency')
@click.option('--show_country', is_flag = True, help = 'List the supported countries')
@click.option('--date', default='-1', help = 'Enter the number of days to look back from today (not more than 16 days')
def cli(currency, show_country, date):
	date = int(date)
	if date  is not -1:
		currency = currency.upper()
		click.echo("Welcome to BPI\n\n")	
		hist_bpi = get_historical_bpi(date, currency)
		print_hist_bpi(hist_bpi)
	else:
		#click.echo(date)
		currency = currency.upper()
		click.echo("Welcome to BPI\n")
		bpi = get_bpi(currency)
		click.echo("1 Bitcoin for {} {}".format(bpi,currency))

	if show_country:
		country_response = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')
		country_response.raise_for_status()	
		country_json = country_response.json()
		for c in country_json:
			print(str(c['currency'])+"  ::  "+str(c['country'])+"\n")
