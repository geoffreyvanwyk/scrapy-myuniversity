from os import mkdir, path, system
from datetime import datetime

if not path.isdir('results'):
	mkdir('results', 0755)

timestamp = datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
filename = 'results/myuniversity-courses-' + timestamp + '.csv'

system('scrapy crawl myuniversity -o ' + filename + ' -t csv')