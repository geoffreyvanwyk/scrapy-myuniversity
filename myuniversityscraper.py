from os import mkdir, path, system
from datetime import datetime

if not path.isdir('results'):
	mkdir('results', 0755)

if not path.isdir('logs'):
	mkdir('logs', 0755)

timestamp = datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
results_file_name = 'results/myuniversity-courses-' + timestamp + '.csv'
log_file_name = 'logs/' + timestamp + '.log'

system(
	'scrapy crawl myuniversity ' +
	'--output=' + results_file_name +
	' -t csv ' +
	'--logfile=' +	log_file_name
)