from os import system
from datetime import datetime

timestamp = datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
filename = 'results/myuniversity-courses-' + timestamp + '.csv'

system('scrapy crawl myuniversity -o ' + filename + ' -t csv')