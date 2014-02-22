# MyUniversity Scraper (Scrapy)

Uses the Scrapy framework to scrape undergraduate and postgraduate course information from the website www.myuniversity.gov.au. The data is collected in a CSV file with the following headings:

* Course Name
* Cut-off ATAR
* Duration
* Award Type
* Field of Education
* Provider
* Campus
* Level

## Requirements

* [Python 2.7](http://python.org/downloads/)
* [Scrapy 0.22](http://doc.scrapy.org/en/latest/intro/install.html)

## Usage

From the root directory of the project, issue the following command:

	python myuniversityscraper_run.py

The beginning of the script's terminal output will be similar to this:

![Screenshot of beginning of terminal output](beginning-of-terminal-output.png)

The end of the script's terminal output will be similar to this:

![Screenshot of end of terminal output](end-of-terminal-output.png)

The script will produce a CSV (comma-separated values) file with a file name of the form `myuniversity-courses-<date-and-time>.csv. The file name contains the date on and time at which the scrape was performed. It is necessary to have a unique file name each time to prevent the results being appended to previous results.

## Standalone Application

To create a standalone application which does not need the installation of Python, Scrapy or any other dependencies, use PyInstaller. Issue the following command from the root of the project's directory tree:

	pyinstaller myuniversityscraper_run.py

PyInstaller will create a **myuniversityscraper_run.spec** file, and two directories, **build** and **dist**. The **dist** directory contains a **myuniversityscraper_run** folder. This latter folder can be distributed. It contains an executable (myuniversityscraper_run), and other files which the executable needs. On a GNU/Linux system, the executable can be run from the command line as follows (from the same directory that contains the executable):

	./myuniversityscraper_run

It has the same output as the Python script.

## Performance

The performance was measured on a computer with the following specification:

* __Processor (x2):__ Intel(R) Celeron(R) CPU E3400 @ 2.60GHz
* __Memory:__ 8 GB
* __Internet Download Speed__: 4 Mbps

The results (as 22 February 2014):

* __Number of Requests:__ 156
* __Number of Courses per Request:__ 100
* __Duration:__ 2 minutes 49 seconds