# Python-Freerider
Parser som hämtar all tillgängliga bilar från Herz Freerider och sparar dem som en dictionary. 

Följande är resultatet från `get_rides()`
```json
[
    {
        "offer_date": "2023-01-16",
        "end_date": "2023-02-07",
        "car_model": "FORD FOCUS",
        "start": {
            "id": "378",
            "name": "Visby AP Motorcentralen",
            "street": "Visby Flygplats",
            "postalcode": "621 22",
            "postaladdress": "Visby",
            "cordinates": [
                "57.66999",
                "18.35388"
            ]
        },
        "end": {
            "id": "378",
            "name": "Visby AP Motorcentralen",
            "street": "Visby Flygplats",
            "postalcode": "621 22",
            "postaladdress": "Visby",
            "cordinates": [
                "57.66999",
                "18.35388"
            ]
        }
    },
    {
        "offer_date": "2023-01-25",
        "end_date": "2023-02-06",
        "car_model": "VOLVO V60",
        "start": {
            "id": "276",
            "name": "Sk\u00f6vde Brandt",
            "street": "Mellomkvarnsv\u00e4gen 2",
            "postalcode": "541 29",
            "postaladdress": "Sk\u00f6vde",
            "cordinates": [
                "58.41908",
                "13.87015"
            ]
        },
        "end": {
            "id": "276",
            "name": "Sk\u00f6vde Brandt",
            "street": "Mellomkvarnsv\u00e4gen 2",
            "postalcode": "541 29",
            "postaladdress": "Sk\u00f6vde",
            "cordinates": [
                "58.41908",
                "13.87015"
            ]
        }
    }
]
```

## Installation

Installera moduler
```shell
pip install -r requirements.txt
```

Importera funktionen
```python
from freerider_parser import get_rides
```

Sen kalla på funktionen
```python
rides = get_rides()
```
