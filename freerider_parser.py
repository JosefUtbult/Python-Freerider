import requests
from bs4 import BeautifulSoup
import json
import re

RIDES_URL = "http://hertzfreerider.se/unauth/list_transport_offer.aspx"
STATION_URL = "https://hertzfreerider.se/unauth/stationInfo.aspx?stationId={}"

STATIONID_REG = r"stationId=([0-9]*)"
STATION_CORDINATE_REG = r"google\.maps\.LatLng\(([0-9|\.]*),([0-9|\.]*)\)\;"


def _get_request(url):
    while True:
        try:
            return requests.get(url)
        except requests.exceptions.ConnectionError:
            print(f"Unable to load {url}. Retry")


def _station_from_id(id):
    site = _get_request(STATION_URL.format(id))
    soup = BeautifulSoup(site.text, 'html.parser')

    name = soup.find(id='ctl00_ContentPlaceHolder1_stationName').text
    street = soup.find(id='ctl00_ContentPlaceHolder1_street').text
    postalcode = soup.find(id='ctl00_ContentPlaceHolder1_postalcode').text
    postaladdress = soup.find(id='ctl00_ContentPlaceHolder1_postaladdress').text

    if not name or not street or not postalcode or not postaladdress:
        return False, "", "", "", "", ("", "")

    matches = re.search(STATION_CORDINATE_REG, site.text)
    if not matches or len(matches.groups()) < 2:
        return False, "", "", "", "", ("", "")

    cordinates = (matches.groups()[0], matches.groups()[1])

    return True, name, street, postalcode, postaladdress, cordinates


def _location_from_href(element):
    matches = re.search(STATIONID_REG, element.get('href'))
    if not matches:
        return (False, {})
    
    stationId = matches.groups()[0]
    status_station, name, street, postalcode, postaladdress, cordinates = _station_from_id(stationId)
    if not status_station:
        return (False, {})

    return (True, {
        'id': stationId,
        'name': name,
        'street': street,
        'postalcode': postalcode,
        'postaladdress': postaladdress,
        'cordinates': cordinates
    })


def _info_from_element(element):
    spans = element.find_all('span')
    if len(spans) < 3:
        return False, "", "", ""

    offer_date = spans[0].text
    end_date = spans[1].text
    car_model = spans[2].text
    
    return True, offer_date, end_date, car_model


def get_rides():
    site = _get_request(RIDES_URL)
    soup = BeautifulSoup(site.text, 'html.parser')

    routes = []
    table = soup.find(id="ctl00_ContentPlaceHolder1_Display_transport_offer_advanced1_DataList1")
    for child in table.find_all(class_='highlight'):
        links = child.find_all('a')
        if len(links) < 2:
            continue
        
        status_start, start = _location_from_href(links[0])
        status_end, end = _location_from_href(links[0])
        status_info, offer_date, end_date, car_model = _info_from_element(child.find_next_sibling('tr'))

        if not status_start or not status_end or not status_info:
            continue

        routes.append({
            'offer_date': offer_date,
            'end_date': end_date,
            'car_model': car_model,
            'start': start, 
            'end': end
        })
    return routes
    

if __name__=='__main__':
    routes = get_rides()
    with open('test.json', 'w') as file:
        file.write(json.dumps(routes, indent=4))

get_rides()