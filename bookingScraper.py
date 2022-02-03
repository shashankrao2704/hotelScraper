import json
import os

from bs4 import BeautifulSoup


class InvalidFile(Exception):
    pass


def get_html_file(url):
    try:
        with open(url, "rb") as f:
            bs_doc = BeautifulSoup(f, "html.parser")
        return bs_doc
    except IOError as e:
        raise InvalidFile(e)


def get_hotel_name(bs_doc):
    hotel_name = bs_doc.find('span', attrs={'id': 'hp_hotel_name'})
    return hotel_name.text.replace('\n', '')


def get_hotel_address(bs_doc):
    hotel_address = bs_doc.find('span', attrs={'id': 'hp_address_subtitle'})
    return hotel_address.text.replace('\n', '')


def get_hotel_stars(bs_doc):
    star_check = bs_doc.find('span', attrs={'class': '_bebcf8d60 _00b78c844'})
    if star_check is not None:
        star_count = 0
        for star in star_check:
            star_count += 1
        return star_count
    else:
        stars_class = bs_doc.find('span', attrs={'class': 'hp__hotel_ratings__stars'})
        stars = stars_class.find('i').attrs['class']
        for star in stars:
            if star.startswith('ratings_stars_'):
                return int(star[-1])
        return 0


def get_score_card(bs_doc):
    card = bs_doc.find('div', attrs={'class': 'hotel_large_photp_score'})
    return card


def get_review_points(card):
    review_points = card.findChild('span', attrs={'class': 'average'})
    return float(review_points.text)


def get_no_of_reviews(card):
    no_of_reviews = card.findChild('strong')
    return int(no_of_reviews.text)


def get_hotel_description(bs_doc):
    description_card = bs_doc.find('div', attrs={'class': 'hotel_description_wrapper_exp'}).findChild('div', attrs={
        'id': 'summary'}).findChildren('p')
    description_string = ""
    for description in description_card:
        description_string += description.text.replace('\n', '')
    return description_string


def get_room_categories(bs_doc):
    room_type_list = []
    room_types = bs_doc.find('table', attrs={'class': 'roomstable'}).findChildren('td', attrs={'class': 'ftd'})
    for room_type in room_types:
        room_type_list.append(room_type.text.replace('\n', ''))
    return room_type_list


def get_alternate_hotels(bs_doc):
    alternate_hotels_list = []
    alternate_hotels = bs_doc.find('tr', attrs={'id': 'althotelsRow'}).findChildren('a',
                                                                                    attrs={'class': 'althotel_link'})
    for alternate_hotel in alternate_hotels:
        alternate_hotels_list.append(alternate_hotel.text.replace('\n', ''))
    return alternate_hotels_list


def json_save(hotel_info, fname):
    try:
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(hotel_info, f, ensure_ascii=False, indent=4)
            f.close()
            print(json.dumps(hotel_info, indent=4))
    except IOError as e:
        raise InvalidFile(e)


def scrape_hotel_info():
    url = "Input_dir/extraction.booking.html"
    filename = "./extracted_data/booking_scraped_data.json"

    bsoup = get_html_file(url)
    hotel_info_dict = {'hotel_name': get_hotel_name(bsoup), 'hotel_address': get_hotel_address(bsoup),
                       'hotel_stars': get_hotel_stars(bsoup), 'review_points': get_review_points(get_score_card(bsoup)),
                       'number_of_reviews': get_no_of_reviews(get_score_card(bsoup)),
                       'description': get_hotel_description(bsoup), 'room_categories': get_room_categories(bsoup),
                       'alternate_hotels': get_alternate_hotels(bsoup)}
    json_save(hotel_info_dict, filename)


if __name__ == '__main__':
    scrape_hotel_info()

