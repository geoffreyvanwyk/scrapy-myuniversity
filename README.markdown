# MyUniversity Scraper (Scrapy)

Uses the Scrapy framework to scrape undergraduate and postgraduate course information from the website www.myuniversity.gov.au. The data is collected in a CSV (comma-separated values) file with the following headings:

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

	python myuniversityscraper.py

The script's terminal output will be similar to this:

> Start Time:  18:15:29 Apr 13, 2014
> Initializing ...
> Retrieving Course: 15582 of 15582
> Stop Time:  18:18:00 Apr 13, 2014
> Done.

The script will produce a CSV (comma-separated values) file with a file name of the form `myuniversity-courses-&lt;date-and-time&gt;.csv in the results directory. The file name contains the date on and time at which the scrape was performed. It is necessary to have a unique file name each time to prevent the results being appended to previous results.

## Standalone Application

To create a standalone application which does not need the installation of Python, Scrapy or any other dependencies, use [PyInstaller](http://pythonhosted.org/PyInstaller/#installing-using-pip). Issue the following command from the root of the project's directory tree:

	pyinstaller myuniversityscraper.py

PyInstaller will create a **myuniversityscraper.spec** file, and two directories, **build** and **dist**. The **dist** directory contains a **myuniversityscraper** directory. This latter directory can be distributed. It contains an executable (myuniversityscraper) and other files which the executable needs. On a GNU/Linux system, the executable can be run from the command line as follows (from the same directory that contains the executable):

	./myuniversityscraper

It has the same output as the Python script.

## Performance

The performance was measured on a computer with the following specification:

* __Processor (x2):__ Intel Celeron CPU E3400 @ 2.60GHz
* __Memory:__ 8 GB
* __Internet Download Speed__: 4 Mbps

The results (as of 22 February 2014):

* __Number of Requests:__ 156
* __Number of Courses:__ 15,584
* __Duration:__ 2 minutes 49 seconds