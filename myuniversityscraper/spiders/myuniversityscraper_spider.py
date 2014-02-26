from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from myuniversityscraper.items import Course

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
		return FormRequest('http://myuniversity.gov.au/' + course_level + 'Courses/GetSearchResults', formdata={
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
		}, callback=self.get_courses)

	def get_courses(self, response):
		is_undergraduate = 'Undergraduate' in response.url
		sel = Selector(response)

		try:
			course_elements = sel.xpath("//div[@class='myuni-small-cell-block']")
			if course_elements == []:
				raise Exception(
					"WebPageStructureChangedError",
					"The course_elements selector is an empty list.",
					"Please update the xpaths in the source code."
				)

			for course_element in course_elements:
				course_attribute_elements = course_element.xpath('.//span')
				course = Course()
				course['course_name'] = course_attribute_elements[0].xpath('a/text()').extract()
				if is_undergraduate:
					course['cutoff_atar'] = course_attribute_elements[2].xpath('text()').extract()
					course['duration'] = course_attribute_elements[4].xpath('text()').extract()
					course['award_type'] = course_attribute_elements[5].xpath('text()').extract()
					course['field_of_education'] = course_attribute_elements[6].xpath('text()').extract()
					course['provider'] = course_attribute_elements[7].xpath('a/text()').extract()
					course['campus'] = course_attribute_elements[8].xpath('text()').extract()
					course['level'] = 'Undergraduate'
				else:
					course['cutoff_atar'] = ''
					course['duration'] = course_attribute_elements[2].xpath('text()').extract()
					course['award_type'] = course_attribute_elements[3].xpath('text()').extract()
					course['field_of_education'] = course_attribute_elements[4].xpath('text()').extract()
					course['provider'] = course_attribute_elements[5].xpath('a/text()').extract()
					course['campus'] = course_attribute_elements[6].xpath('text()').extract()
					course['level'] = 'Postgraduate'
				yield course

			number_of_pages = int(sel.xpath("//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/label/span[last()]/text()").extract()[0].replace('of', ''))
			current_page = int(sel.xpath("//div[@class='myuni-alignright-whenbig'][../p[@id='navigationDescriptor']]/label/input/@value").extract()[0])
			if number_of_pages > current_page:
				course_level = 'Undergraduate' if is_undergraduate else 'Postgraduate'
				yield self.get_request(course_level, current_page)
			
		except Exception as e:
			print
			print e.args[0]+': ', e.args[1]
			print 'Fix:', e.args[2]
			print