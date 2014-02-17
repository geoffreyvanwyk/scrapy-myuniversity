from scrapy.item import Item, Field

class Course(Item):
    course_name = Field()
    cutoff_atar = Field()
    duration = Field()
    award_type = Field()
    field_of_education = Field()
    provider = Field()
    campus = Field()
    level = Field()
