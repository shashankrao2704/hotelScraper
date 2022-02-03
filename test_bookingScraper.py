import json

import bookingScraper as bs

url = "Input_dir/extraction.booking.html"
filename = "./extracted_data/booking_scraped_data.json"


def test_get_html_file(tmpdir):
    tmp_html = tmpdir.join('temp.html')
    tmp_html.write_text('<h1>Test</h1>', encoding='utf-8')
    parsed_html = bs.get_html_file(tmp_html.strpath)
    assert parsed_html.text == 'Test'


def test_get_hotel_name():
    hotel_name = 'Kempinski Hotel Bristol Berlin'
    test_hotel_name = bs.get_hotel_name(bs.get_html_file(url))
    assert test_hotel_name == hotel_name


def test_get_hotel_address():
    hotel_address = 'Kurfürstendamm 27, Charlottenburg-Wilmersdorf, 10719 Berlin, Germany'
    test_hotel_address = bs.get_hotel_address(bs.get_html_file(url))
    assert test_hotel_address == hotel_address


def test_get_hotel_stars():
    hotel_stars = 5
    test_hotel_address = bs.get_hotel_stars(bs.get_html_file(url))
    assert test_hotel_address == hotel_stars


def test_get_score_card():
    score_card_attr = 'featured_review_score'
    test_card_attr = bs.get_score_card(bs.get_html_file(url))
    assert test_card_attr.get('class')[1] == score_card_attr


def test_get_review_points():
    review_points = 8.3
    test_review_points = bs.get_review_points(bs.get_score_card(bs.get_html_file(url)))
    assert test_review_points == review_points


def test_get_no_of_reviews():
    no_of_reviews = 1401
    test_no_of_reviews = bs.get_no_of_reviews(bs.get_score_card(bs.get_html_file(url)))
    assert test_no_of_reviews == no_of_reviews


def test_get_hotel_description():
    test_description = bs.get_hotel_description(bs.get_html_file(url))
    assert test_description.startswith('This') and test_description.endswith('away. ')


def test_get_room_categories():
    test_room_categories = bs.get_room_categories(bs.get_html_file(url))
    assert len(test_room_categories) == 7


def test_get_alternate_hotels():
    test_alternate_hotels = bs.get_alternate_hotels(bs.get_html_file(url))
    assert len(test_alternate_hotels) == 4


def test_json_save(tmpdir):
    tmp_data = {'test': True}
    tmp_file = tmpdir.join('temp.json')
    bs.json_save(tmp_data, tmp_file)
    with open(tmp_file) as tmp:
        test_data = json.load(tmp)
        assert test_data['test'] is True


def test_scrape_hotel_info():
    test_keys = ['hotel_name', 'hotel_address', 'hotel_stars', 'review_points', 'number_of_reviews', 'description',
                 'room_categories', 'alternate_hotels']
    with open(filename) as file:
        test_data = json.load(file)
        assert list(test_data.keys()) == test_keys
