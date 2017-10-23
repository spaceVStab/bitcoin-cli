import os


from setuptools import setup

setup(
	name = "bitcoin-cli",
	version = 0.1,
	py_modules=['bitcoin-cli'],
	install_requires = ['Click'],
	entry_points = '''
		[console_scripts]
		bitcoin-cli = bitcoin_coindesk:cli
		''',
)