from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from myuniversityscraper.items import Course

class MyuniversityscraperSpider(Spider):
	name = 'myuniversity'
	allowed_domains = ['myuniversity.gov.au']

	def start_requests(self):
		requests = []

		for i in range(1,76): # The second argument of the range function should be 1 more than the number of pages.
			requests.append(FormRequest('http://myuniversity.gov.au/UndergraduateCourses/GetSearchResults', formdata={
				'courseCutOff': '100',
				'courseCutOffQld': '1',
				'courseEntryCutOffOption': '0',
				'courseFee': '100000',
				'courseFeeOption': '0',
				'courseLevelOption': 'Undergraduate',
				'courseName': '',
				'degreeStudyOption': '0',
				'deliveryOption': '0',
				'excludedWords': '',
				'page':	str(i),
				'pageSize':	'Hundred',
				'providerType':	'0',
				'resetSelections': 'false',
				'sortDirection': 'Ascending',
				'sortOrder': ''
			}, callback=self.get_courses))

		for i in range(1,82): # The second argument of the range function should be 1 more than the number of pages.
			requests.append(FormRequest('http://myuniversity.gov.au/PostgraduateCourses/GetSearchResults', formdata={
				'courseCutOff': '100',
				'courseCutOffQld': '1',
				'courseEntryCutOffOption': '0',
				'courseFee': '100000',
				'courseFeeOption': '0',
				'courseLevelOption': 'Postgraduate',
				'courseName': '',
				'degreeStudyOption': '0',
				'deliveryOption': '0',
				'excludedWords': '',
				'page':	str(i),
				'pageSize':	'Hundred',
				'providerType':	'0',
				'resetSelections': 'false',
				'sortDirection': 'Ascending',
				'sortOrder': ''
			}, callback=self.get_courses))

		return requests

	def get_courses(self, response):
		is_undergraduate = 'Undergraduate' in response.url
		sel = Selector(response)
		course_elements = sel.xpath("//div[@class='myuni-small-cell-block']")
		courses = []
		for course_element in course_elements:
			course_attribute_elements = course_element.xpath('.//span')
			course = Course()
			course['course_name'] = course_attribute_elements[0].xpath('a/text()').extract()
			course['cutoff_atar'] = course_attribute_elements[2].xpath('text()').extract() if is_undergraduate else ''
			course['duration'] = course_attribute_elements[4].xpath('text()').extract() if is_undergraduate else course_attribute_elements[2].xpath('text()').extract()
			course['award_type'] = course_attribute_elements[5].xpath('text()').extract() if is_undergraduate else course_attribute_elements[3].xpath('text()').extract()
			course['field_of_education'] = course_attribute_elements[6].xpath('text()').extract() if is_undergraduate else course_attribute_elements[4].xpath('text()').extract()
			course['provider'] = course_attribute_elements[7].xpath('a/text()').extract() if is_undergraduate else course_attribute_elements[5].xpath('a/text()').extract()
			course['campus'] = course_attribute_elements[8].xpath('text()').extract() if is_undergraduate else course_attribute_elements[6].xpath('text()').extract()
			course['level'] = 'Undergraduate' if is_undergraduate else 'Postgraduate'
			courses.append(course)
		return courses