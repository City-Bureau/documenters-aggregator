import pytest

from tests.utils import file_response
from city_scrapers.spiders.chi_mayors_bicycle_advisory_council import ChiMayorsBicycleAdvisoryCouncilSpider


def test_tests():
    print('Please write some tests for this spider or at least disable this one.')
    assert False


"""
Uncomment below
"""

# test_response = file_response('files/chi_mayors_bicycle_advisory_council.html')
# spider = ChiMayorsBicycleAdvisoryCouncilSpider()
# parsed_items = [item for item in spider.parse(test_response) if isinstance(item, dict)]


# def test_name():
    # assert parsed_items[0]['name'] == 'EXPECTED NAME'


# def test_description():
    # assert parsed_items[0]['event_description'] == 'EXPECTED DESCRIPTION'


# def test_start():
    # assert parsed_items[0]['start'] == {'date': None, 'time': None, 'note': 'EXPECTED DATE AND TIME'}


# def test_end():
    # assert parsed_items[0]['end'] == {'date': None, 'time': None, 'note': 'EXPECTED DATE AND TIME'}


# def test_id():
    # assert parsed_items[0]['id'] == 'EXPECTED ID'


# def test_status():
    # assert parsed_items[0]['status'] == 'EXPECTED STATUS'


# def test_location():
    # assert parsed_items[0]['location'] == {
        # 'neighborhood': 'EXPECTED URL',
        # 'name': 'EXPECTED NAME',
        # 'address': 'EXPECTED ADDRESS'
    # }


# def test_sources():
    # assert parsed_items[0]['sources'] == [{
        # 'url': 'EXPECTED URL',
        # 'note': 'EXPECTED NOTE'
    # }]


# def test_documents():
    # assert parsed_items[0]['documents'] == [{
      # 'url': 'EXPECTED URL',
      # 'note': 'EXPECTED NOTE'
    # }]


# @pytest.mark.parametrize('item', parsed_items)
# def test_all_day(item):
    # assert item['all_day'] is False


# @pytest.mark.parametrize('item', parsed_items)
# def test_classification(item):
    # assert item['classification'] is None


# @pytest.mark.parametrize('item', parsed_items)
# def test__type(item):
    # assert parsed_items[0]['_type'] == 'event'
