import requests
import re
import json

BASE_URL = "http://127.0.0.1:5000/"
HOME_PAGE = BASE_URL

LOGIN_URL = BASE_URL + 'api/auth/login'
REGISTER_USR = BASE_URL + 'api/auth/register_user'
ADD_HOTEL_URL = BASE_URL + 'api/admin/create_hotel'
ADD_ACCOMMODATION_URL = BASE_URL + 'api/admin/create_accommodation'
ADD_INVENTORY_URL = BASE_URL + 'api/admin/create_room_inventory'
GET_ROOM_INVENTORY_URL = BASE_URL + 'api/admin/get_inventory_list'
GET_RESERVATION_URL = BASE_URL + 'api/admin/get_reservation_list'
CONFIRM_RESERVATION_URL = BASE_URL + 'api/admin/confirm_reservation'

SEARCH_ROOM_URL = BASE_URL + 'api/guest/search_available_room'
BOOKING_RESERVATION_URL = BASE_URL + 'api/guest/create_reservation'

test_account = "quill@gmail.com"
test_password = "16041992"


def get_auth_request():
    ses = requests.session()
    ses.get(HOME_PAGE)

    payload = {
        'email': test_account,
        'password': test_password,
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = ses.post(LOGIN_URL, json=payload, headers=headers)
    # First I send a get request to get the cookies
    return ses


def test_user_register():
    payload = {
        'first_name': "Peter",
        'last_name': "Quill",
        'email': "quill@gmail.com",
        "superuser": True,
        "role_type": 1,
        "password": "16041992"
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.post(REGISTER_USR, json=payload, headers=headers)

    assert response.status_code == 201

    return response


def test_logout():
    pass


def test_create_hotel():
    payload = {
        'name': "Red Sun Hotel",
        'description': "This is one of a few places in the area that has this feature.",
        'timezone': "G+17",
        "address": "Thành phố Vũng Tàu",
        "website": "https://www.airbnb.com/rooms/32486428",
        "logo_url": "https://www.airbnb.com/rooms/32486428",
        "cover_url": "https://www.airbnb.com/rooms/32486428",
        "loyalty_club": "loyalty_club",
        "loyalty_url": "https://www.airbnb.com/rooms/32486428",
        "currency": "USD"
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = session.post(ADD_HOTEL_URL, json=payload, headers=headers)

    json = response.json()
    assert response.status_code == 200
    assert "hotel_id" in json

    payload = {
        'name': "Annata Hotel",
        'description': "This is one of a few places in the area that has this feature.",
        'timezone': "G+17",
        "address": "",
        "website": "https://www.airbnb.com/rooms/34607048",
        "logo_url": "https://www.airbnb.com/rooms/34607048",
        "cover_url": "https://www.airbnb.com/rooms/34607048",
        "loyalty_club": "loyalty_club",
        "loyalty_url": "https://www.airbnb.com/rooms/34607048",
        "currency": "USD"
    }

    response = session.post(ADD_HOTEL_URL, json=payload)
    json = response.json()
    assert response.status_code == 200
    assert "hotel_id" in json


def test_create_accommodation():
    payload_1 = {
        'name': "Room 1",
        "hotel_id": "981d8df721044059a7a632220d88b865",
        'description': "Room 1 des",
        'max_guests': 10,
        "image_url": "https://www.airbnb.com/rooms/34607048"
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = session.post(ADD_ACCOMMODATION_URL, json=payload_1, headers=headers)
    json = response.json()
    assert response.status_code == 200
    assert "accommodation_id" in json

    payload_2 = {
        'name': "Room 2",
        "hotel_id": "981d8df721044059a7a632220d88b865",
        'description': "Room 2 des",
        'max_guests': 10,
        "image_url": "https://www.airbnb.com/rooms/34607048"
    }

    response = session.post(ADD_ACCOMMODATION_URL, json=payload_2, headers=headers)

    payload_3 = {
        'name': "Room 3",
        "hotel_id": "981d8df721044059a7a632220d88b865",
        'description': "Room 3 des",
        'max_guests': 10,
        "image_url": "https://www.airbnb.com/rooms/34607048"
    }

    response = session.post(ADD_ACCOMMODATION_URL, json=payload_3, headers=headers)


def test_add_room_inventory():
    payload_1 = {
        'accommodation_id': "2e35ce5f3e314f079498075e69c26a9c",
        "name": "inventory 1",
        'description': "inventory 1 des",
        'sell_start_date': '2019-07-10',
        "sell_end_date": '2019-10-10',
        "daily_rates": [
            {
                "date": "2019-08-10",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-08-15",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-08-16",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-08-20",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            }
        ]
    }

    response = session.post(ADD_INVENTORY_URL, json=payload_1)
    json = response.json()
    assert response.status_code == 200
    assert "inventory_id" in json

    payload_2 = {
        'accommodation_id': "30ed57e7d8874af2a96bfa96003c04db",
        "name": "inventory 2",
        'description': "inventory 2 des",
        'sell_start_date': '2019-06-10',
        "sell_end_date": '2019-11-10',
        "daily_rates": [
            {
                "date": "2019-07-10",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-09-15",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-08-18",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            },
            {
                "date": "2019-08-20",
                "quantity": 10,
                "remain": 10,
                "rate": 100.0
            }
        ]
    }
    response = session.post(ADD_INVENTORY_URL, json=payload_2)


def test_get_room_inventory():
    response = session.get(GET_ROOM_INVENTORY_URL, params={"hotel_id": "981d8df721044059a7a632220d88b865"})

    assert "room_inventories" in response.json()
    print("pass get room invetory test!")

def test_get_reservation():
    response = session.get(GET_RESERVATION_URL,
                           params={"hotel_id": "981d8df721044059a7a632220d88b865", "status": "pending"})

    assert "reservations" in response.json()
    print("pass get reservation test!")

def test_confirm_reservation():
    response = session.get(CONFIRM_RESERVATION_URL,
                           params={"reservation_id": "51119e312bae4f6f9652851a5308f1c0", "conf_number": 2})

    assert "reservation_id" in response.json()
    assert "status" in response.json()


def booking_reservation():
    payload_1 = {
        'room_inventory_id': "bc2ce44a3b564864966ec02eadc67c44",
        "adults": 5,
        'children': 4,
        'check_in': '2019-08-12',
        'check_out': '2019-08-20',
        'last_name': 'Dung',
        'first_name': 'Do',
        'phone': '0976650613',
        "email": "dung@gmail.com",
        'message': 'text reservation message'
    }
    response = requests.post(BOOKING_RESERVATION_URL, json=payload_1)
    assert response.status_code == 200


def search_room():
    response = requests.get(SEARCH_ROOM_URL, params={"hotel_id": "981d8df721044059a7a632220d88b865",
                                                     "check_in": "2019-08-10",
                                                     "check_out": "2019-08-15",
                                                     "adults": 4})

    assert "rooms" in response.json()
    print("pass search room test!")


if __name__ == "__main__":
    # test_user_register()
    session = get_auth_request()
    test_get_reservation()
    test_get_room_inventory()
    search_room()