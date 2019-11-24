from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.chi_northern_il_university import ChiNorthernIlUniversitySpider

test_response = file_response(
    join(dirname(__file__), "files", "chi_northern_il_university_calendar.html"),
    url="https://www.neiu.edu/about/board-of-trustees/calendar-of-meetings",
)

docs_response = file_response(
    join(dirname(__file__), "files", "chi_northern_il_university_docs.html"),
    url="https://www.neiu.edu/about/board-of-trustees/board-meeting-materials",
)

spider = ChiNorthernIlUniversitySpider()

freezer = freeze_time("2019-11-15")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

# def test_tests():
#    print("Please write some tests for this spider or at least disable this one.")
#    assert False
"""
Uncomment below
"""


def test_title():
    assert parsed_items[0][
        "title"] == "(was previously scheduled for January 17)  Academic/Student Affairs \
          and Enrollment Management Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 1, 16, 13, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 1, 16, 15, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == "See agenda for meeting time"


def test_id():
    assert parsed_items[
        0]["id"
           ] == "chi_northern_il_university/201901161300/x/_was_previously_scheduled_for_january_17\
    _academic_student_affairs_and_enrollment_management_committee"


def test_status():
    assert parsed_items[0]["status"] == "cancelled"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "5500 North St. Louis Avenue, Chicago, Ill., 60625",
        "address": "Northeastern Illinois University"
    }


def test_source():
    assert parsed_items[0]["source"] == test_response.url


def test_links():
    assert parsed_items[0]["links"] == [{
        "href":
            "https://www.neiu.edu/sites/neiu.edu/files/documents/ktvoigt/\
19.01.16.ASAEM%20Committee%20Meeting%20Agenda.pdf",
        "title": "Committee Meeting Agenda"
    }, {
        "href":
            "https://www.neiu.edu/sites/neiu.edu/files/documents/ktvoigt/\
19.01.16.ASAEM%20Committee%20Meeting%20Minutes_approved.pdf",
        "title": "Committee Meeting Minutes"
    }]


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
