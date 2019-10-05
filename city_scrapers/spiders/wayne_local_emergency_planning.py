from city_scrapers_core.constants import NOT_CLASSIFIED, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


from datetime import datetime


class WayneLocalEmergencyPlanningSpider(CityScrapersSpider):
    name = "wayne_local_emergency_planning"
    agency = "Wayne County Local Emergency Planning Committee"
    timezone = "America/Detroit"
    allowed_domains = ["www.waynecounty.com"]
    start_urls = ["https://www.waynecounty.com/departments/hsem/wayne-county-lepc.aspx"]
	
	
	
	
	
    def parse_meetings(response):
        #meeting_xpath = """
        #        //td[preceding::h3[1]/text()[
        #            contains(., "Meeting Schedule")
        #            ]]"""
					
        meeting_xpath = '''//p/p'''
		
        return response.xpath(meeting_xpath)		

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
		
        #print("type=" + str(type(response)))
        #print("response=" + str(response))	
        #print("response.css=" + str(response.css))			
		
        #from scrapy.selector import Selector
        #selector = Selector(response)
        html = response.xpath('//body//text()')
        #print("html=" + str(html))	
		
        '''current_year_non_empty_rows = response.xpath(
            '//section[contains(.,"%s")]//tbody/tr[child::td/text()]' % current_year
        '''
		
        #exit()
		
        #test_list = ["test item", "next test item"]
        #test_list = self.parse_meetings(response)
        #test_list = response.xpath('//p/p')
        meeting_dates = response.xpath('''//p[contains(text(),'day, ')]''')
        #test_list = response.xpath("//div//p[text() = 'Meeting Schedule']/following-sibling:://div//p")		
        #test_list = response.xpath("//div//p[text() = '<strong>Meeting Schedule</strong>']//p")		

		
		
        #print('length of test_list = ' + str(len(test_list)))
        #exit()
		
        #for item in response.css(".meetings"):
        for item in meeting_dates:
            #print('------------')
            #print(item)
            
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )
            
			
			

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting
        #exit()
		
    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return "test title"

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return "test description"

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return COMMITTEE #done
		
    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        test_dt = datetime.now()
        return test_dt

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        test_dt = datetime.now()
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return "test notes"

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "1234",
            "name": "teststreet",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "google.com", "title": "google"}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
