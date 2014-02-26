from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

from myuniversityscraper.items import Course
from myuniversityscraper.exceptions import WebPageChangedError

class MyuniversityscraperSpider(Spider):
	name = 'myuniversity'
	allowed_domains = ['myuniversity.gov.au']

	def start_requests(self):
		course_levels = ['Undergraduate', 'Postgraduate']
		requests = []
		for course_level in course_levels:
			requests.append(self.get_request(course_level, 0))
		return requests

	def get_request(self, course_level, page_number):
		return FormRequest(
			'http://myuniversity.gov.au/' +
			course_level +
			'Courses/GetSearchResults',
			formdata={
				'courseCutOff': '100',
				'courseCutOffQld': '1',
				'courseEntryCutOffOption': '0',
				'courseFee': '100000',
				'courseFeeOption': '0',
				'courseLevelOption': course_level,
				'courseName': '',
				'degreeStudyOption': '0',
				'deliveryOption': '0',
				'excludedWords': '',
				'page':	str(page_number + 1),
				'pageSize':	'Hundred',
				'providerType':	'0',
				'resetSelections': 'false',
				'sortDirection': 'Ascending',
				'sortOrder': ''
		}, callback=self.parse_page)

	def parse_page(self, response):
		is_undergraduate = 'Undergraduate' in response.url
		sel = Selector(response)

		try:
			courses = sel.xpath("//div[@class='myuni-small-cell-block']")
			if courses == []:
				raise WebPageChangedError('courses')

			for course in courses:
				fields = course.xpath('.//span')
				if fields == []:
					raise WebPageChangedError('fields')

				crs = Course()
				crs['course_name'] = fields[0].xpath('a/text()').extract()

				if is_undergraduate:
					crs['cutoff_atar'] = fields[2].xpath('text()').extract()
					crs['duration'] = fields[4].xpath('text()').extract()
					crs['award_type'] = fields[5].xpath('text()').extract()
					crs['field_of_education'] = (
						fields[6].xpath('text()').extract()
					)
					crs['provider'] = fields[7].xpath('a/text()').extract()
					crs['campus'] = fields[8].xpath('text()').extract()
					crs['level'] = 'Undergraduate'
				else:
					crs['cutoff_atar'] = ''
					crs['duration'] = fields[2].xpath('text()').extract()
					crs['award_type'] = fields[3].xpath('text()').extract()
					crs['field_of_education'] = (
						fields[4].xpath('text()').extract()
					)
					crs['provider'] = fields[5].xpath('a/text()').extract()
					crs['campus'] = fields[6].xpath('text()').extract()
					crs['level'] = 'Postgraduate'

				yield crs

			yield self.get_next_page(sel, is_undergraduate)

		except WebPageChangedError as e:
			print
			print e.description
			print e.message
			print e.fix
			print

	def get_next_page(self, sel, is_undergraduate):
		try:
			paginator = sel.xpath(
				"//div[@class='myuni-alignright-whenbig']" +
				"[../p[@id='navigationDescriptor']]/label"
			)
			if paginator == []:
				raise WebPageChangedError('paginator')

			number_of_pages = (
				int(
					paginator
						.xpath("span[last()]/text()")
						.extract()[0]
						.replace('of', '')
				)
			)

			current_page = int(paginator.xpath("input/@value").extract()[0])

			if number_of_pages > current_page:
				if is_undergraduate:
					course_level = 'Undergraduate'
				else:
					course_level = 'Postgraduate'

				return self.get_request(course_level, current_page)

		except IndexError:
			raise WebPageChangedError('number_of_pages or current_page')