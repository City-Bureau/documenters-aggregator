from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD, CANCELLED, FORUM, NOT_CLASSIFIED, PASSED, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.il_pollution_control import IlPollutionControlSpider

test_minutes_response = file_response(
    join(dirname(__file__), "files", "il_pollution_control.html"),
    url="https://pcb.illinois.gov/ClerksOffice/MeetingMinutes",
)

test_response = file_response(
    join(dirname(__file__), "files", "il_pollution_control.json"),
    url="https://pcb.illinois.gov/ClerksOffice/GetCalendarEvents",
)
spider = IlPollutionControlSpider()

freezer = freeze_time("2019-10-03")
freezer.start()

parsed_items = [item for item in spider._parse_json(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 87


def test_title():
    # Define expected number of occurrences of each title:
    expected_title_counts = {
        "Board Meeting": 30,
        "Brown Bag Seminar": 4,
        "Hearing PCB 2012-035": 1,
        "Hearing PCB 2014-003": 4,
        "Hearing PCB 2018-083": 1,
        "Hearing R2018-020": 9,
        "Hearing R2018-024": 4,
        "Hearing R2018-029": 2,
        "Hearing R2018-030": 4,
        "Hearing R2018-032": 12,
        "Hearing R2019-001": 10,
        "Hearing R2019-006": 2,
        "Hearing R2019-018": 4
    }

    # Calculate actual counts from scraped items:
    all_titles = [item["title"] for item in parsed_items]
    unique_titles = set(all_titles)
    title_counts = {ut: len([t for t in all_titles if t == ut]) for ut in unique_titles}
    for title in title_counts:
        assert (title_counts[title] == expected_title_counts[title])


def test_start():
    expected_starts = {
        0: datetime(2018, 10, 4, 12, 0),
        1: datetime(2019, 5, 23, 11, 0),
        38: datetime(2018, 11, 28, 13, 0)
    }

    for n in expected_starts:
        assert parsed_items[n]["start"] == expected_starts[n]


@pytest.mark.parametrize("item", parsed_items)
def test_end(item):
    assert item["end"] is None


def test_id():
    assert parsed_items[0]["id"] == 'il_pollution_control/201810041200/x/brown_bag_seminar'


def test_status():
    expected_counts = {CANCELLED: 11, PASSED: 66, TENTATIVE: 10}
    actual_counts = {}
    for key in expected_counts:
        actual_counts[key] = len([item for item in parsed_items if item['status'] == key])
        assert actual_counts[key] == expected_counts[key]


def test_location():
    expected_counts = {
        "Chicago IPCB Office": 55,
        "Springfield IPCB Office": 14,
        "Illinois EPA": 3,
        "": 15
    }
    actual_counts = {}
    for key in expected_counts:
        actual_counts[key] = len([item for item in parsed_items if item['location']['name'] == key])
        assert actual_counts[key] == expected_counts[key]


def test_source():
    expected_counts = {
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15564": 2,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15596": 10,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15588": 12,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15480": 9,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15559": 4,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15565": 4,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15607": 2,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=16703": 4,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=15594": 1,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=14216": 1,
        "https://pcb.illinois.gov/Cases/GetCaseDetailsById?caseId=14657": 4,
        "https://pcb.illinois.gov/ClerksOffice/GetCalendarEvents": 34
    }
    actual_counts = {}
    for key in expected_counts:
        actual_counts[key] = len([item for item in parsed_items if item['source'] == key])
        assert actual_counts[key] == expected_counts[key]


def test_links():
    # Must use `list()` so generator is fully consumed and spider.link_map is populated.
    list(spider._parse_minutes(test_minutes_response))
    expected_links = {
        datetime(2019, 1, 17).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-99687/1-17-2019 draft2.pdf",  # noqa
        datetime(2019, 2, 28).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-99956/2-28-2019 draft2.pdf",  # noqa
        datetime(2019, 3, 14).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-99970/3-14-2019 draft2.pdf",  # noqa
        datetime(2019, 3, 28).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100053/3-28-2019 draft2.pdf",  # noqa
        datetime(2019, 2, 14).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-99955/2-14-2019 draft2.pdf",  # noqa
        datetime(2019, 4, 11).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100602/04-11-2019 draft1.pdf",  # noqa
        datetime(2019, 4, 25).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100603/04-25-2019 draft1.pdf",  # noqa
        datetime(2019, 5, 30).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100725/05-30-2019 draft1.pdf",  # noqa
        datetime(2019, 6, 20).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100854/06-20-2019 draft1.pdf",  # noqa
        datetime(2019, 7, 25).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-100956/07-25-2019 draft1.pdf",  # noqa
        datetime(2019, 8, 22).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-101165/08-22-2019 draft1.pdf",  # noqa
        datetime(2019, 9, 19).date():
            "https://pcb.illinois.gov/documents/dsweb/Get/Document-101211/09-19-2019 draft1.pdf",  # noqa
    }

    for dt in expected_links:
        assert expected_links[dt] == spider.link_map[dt]


def test_classification():
    expected_counts = {BOARD: 30, FORUM: 4, NOT_CLASSIFIED: 53}
    actual_counts = {}
    for key in expected_counts:
        actual_counts[key] = len([item for item in parsed_items if item['classification'] == key])
        assert actual_counts[key] == expected_counts[key]


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False