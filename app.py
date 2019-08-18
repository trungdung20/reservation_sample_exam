from flask import Flask, request
from flask import Response
import json
from models.auth import *
from models.hotel import *
from models.consts import *

app = Flask(__name__)

VERIFICATION_PASS = 0
UNAUTHENTICATION_ERROR = 1
PERMISSION_DENY_ERROR = 2
app.secret_key = "dungdo"

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def home_page():
    return 'Hotel reservation app'


# ---------------------------AUTHENTICATION API----------------------------------
@app.route('/api/auth/register_user', methods=['POST'])
def register_user():
    user_data = request.get_json()

    first_name = user_data['first_name']
    last_name = user_data['last_name']
    email = user_data['email']
    superuser = bool(user_data['superuser'])
    password = user_data['password']
    role_type = int(user_data['role_type'])
    result = User.register(first_name, last_name, email, superuser, password, role_type)
    session['email'] = email
    if result:
        return Response("User create sucessfully.", status=201, mimetype='application/json')

    return Response("User create failed.", status=400, mimetype='application/json')


@app.route('/api/auth/login', methods=['POST'])
def login():
    login_data = request.get_json()
    email = login_data["email"]
    password = login_data["password"]

    val_result = User.login_validation(email, password)

    if val_result:
        User.login(user_email=email)
        return Response("User login sucessfully.", status=202, mimetype='application/json')

    return Response("User login failed.", status=400, mimetype='application/json')


@app.route('/api/auth/logout', methods=['GET'])
def logout():
    User.logout()


# ---------------------------ADMIN API----------------------------------
@app.route('/api/admin/create_hotel', methods=['POST'])
def create_hotel():
    ver_result = check_authentication(session, permision_type=PERMISSION_HOTEL_ADD)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')

    try:
        hotel_data = request.get_json()
        name = hotel_data['name']
        description = hotel_data['description']
        timezone = hotel_data['timezone']
        address = hotel_data['address']
        website = hotel_data['website']
        logo_url = hotel_data['logo_url']
        cover_url = hotel_data['cover_url']
        loyalty_club = hotel_data['loyalty_club']
        loyalty_url = hotel_data['loyalty_url']
        currency = hotel_data['currency']
        hotel = Hotel(_id=None, name=name, description=description, timezone=timezone, address=address, website=website,
                      logo_url=logo_url, cover_url=cover_url, loyalty_club=loyalty_club, currency=currency,
                      loyalty_url=loyalty_url)
        _id = hotel.create(HOTEL_COLLECTION)
        return Response(json.dumps({"hotel_id": _id}), status=200, mimetype='application/json')
    except:
        return Response("An Error occur.", status=500, mimetype='application/json')


@app.route('/api/admin/create_accommodation', methods=['POST'])
def create_accommodation():
    ver_result = check_authentication(session, permision_type=PERMISSION_ACCOMMODATION_ADD)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')

    try:
        accommdation_data = request.get_json()
        name = accommdation_data['name']
        hotel_id = accommdation_data['hotel_id']
        description = accommdation_data['description']
        max_guests = int(accommdation_data['max_guests'])
        image_url = accommdation_data['image_url']
        accom = Accommodation(_id=None, name=name, description=description, hotel_id=hotel_id,
                              max_guests=max_guests, image_url=image_url)
        _id = accom.create(ACCOMODATION_COLLECTION)
        return Response(json.dumps({"accommodation_id": _id}), status=200, mimetype='application/json')
    except:
        return Response("An Error occur.", status=500, mimetype='application/json')


@app.route('/api/admin/create_room_inventory', methods=['POST'])
def create_room_inventory():
    ver_result = check_authentication(session, permision_type=PERMISSION_ACCOMMODATION_ADD)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')
    try:
        room_inventory_data = request.get_json()
        accommodation_id = room_inventory_data['accommodation_id']
        name = room_inventory_data['name']
        description = room_inventory_data['description']
        sell_start_date = convert_date(room_inventory_data['sell_start_date'])
        sell_end_date = convert_date(room_inventory_data['sell_end_date'])
        daily_rates = room_inventory_data['daily_rates']
        accom = RoomInventory(_id=None, name=name, description=description, accommodation_id=accommodation_id,
                              sell_start_date=sell_start_date, sell_end_date=sell_end_date,
                              daily_rates=daily_rates)
        _id = accom.add_new_room()
        return Response(json.dumps({"inventory_id": _id}), status=200, mimetype='application/json')
    except:
        return Response("An Error occur.", status=500, mimetype='application/json')


@app.route('/api/admin/get_inventory_list', methods=['GET'])
def get_inventory_list():
    ver_result = check_authentication(session, permision_type=PERMISSION_VIEW_INVETORY)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')

    hotel_id = request.args.get('hotel_id')
    room_inventories = RoomInventory.find_rooms(hotel_id)

    return Response(json.dumps({"room_inventories": room_inventories}, indent=4, sort_keys=True, default=str),
                    status=200, mimetype='application/json')


@app.route('/api/admin/get_reservation_list', methods=['GET'])
def get_reservation_list():
    ver_result = check_authentication(session, permision_type=PERMISSION_RESERVATION_VIEW)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')
    
    hotel_id = request.args.get('hotel_id')
    status = request.args.get("status")
    reservations = Reservation.find_reservation(hotel_id, status)
    return Response(json.dumps({"reservations": reservations}, indent=4, sort_keys=True, default=str), status=200, mimetype='application/json')


@app.route('/api/admin/confirm_reservation', methods=['GET'])
def confirm_reservation():
    ver_result = check_authentication(session, permision_type=PERMISSION_VIEW_INVETORY)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')

    reservation_id = request.args.get('reservation_id')
    conf_number = int(request.args.get("conf_number"))
    reservation_id, status = Reservation.confirm_reservation(reservation_id, conf_number)
    return Response(json.dumps({"reservation_id": reservation_id, "status": status}, indent=4, sort_keys=True, default=str), status=200, mimetype='application/json')


# ---------------------------VIEWERS API----------------------------------
@app.route('/api/guest/create_reservation', methods=['POST'])
def create_reservation():
    try:
        reservation_data = request.get_json()
        room_inventory_id = reservation_data['room_inventory_id']
        adults = int(reservation_data['adults'])
        children = int(reservation_data['children'])
        check_in = convert_date(reservation_data['check_in'])
        check_out = convert_date(reservation_data['check_out'])
        last_name = reservation_data['last_name']
        first_name = reservation_data['first_name']
        phone = reservation_data['phone']
        email = reservation_data['email']
        message = reservation_data['message']
        conf_number = 1
        status = RESERVATION_STATUS_PENDING

        reservation = Reservation(_id=None, adults=adults, children=children, room_inventory_id=room_inventory_id,
                                  check_in=check_in, check_out=check_out, last_name=last_name, first_name=first_name,
                                  phone=phone, message=message, conf_number=conf_number, status=status, email=email)
        result = reservation.guest_booking()

        if result:
            return Response(status=200, mimetype='application/json')
        return Response("An Error occur.", status=500, mimetype='application/json')
    except:
        return Response("An Error occur.", status=500, mimetype='application/json')


@app.route('/api/guest/search_available_room', methods=['GET'])
def search_available_room():
    hotel_id = request.args.get('hotel_id')
    check_in = convert_date(request.args.get('check_in'))
    check_out = convert_date(request.args.get("check_out"))
    adults = int(request.args.get("adults"))

    availabe_rooms = RoomInventory.search_room_inventory(hotel_id, check_in=check_in, check_out=check_out,
                                                         adults=adults)
    return Response(json.dumps({"rooms": availabe_rooms}, indent=4, sort_keys=True, default=str), status=200, mimetype='application/json')


# ---------------------------COMMON FUNCTION----------------------------------
def check_authentication(session, permision_type):
    if 'email' in session:
        user = User.find_user(session['email'])
        role = Role.get_role(user._id)
        permissions = role.find_permissions()
        permissions_name = [name['name'] for name in permissions]

        if permision_type not in permissions_name:
            return PERMISSION_DENY_ERROR
        else:
            return VERIFICATION_PASS

    return UNAUTHENTICATION_ERROR

def login_verify_handling(permision_type):
    ver_result = check_authentication(session, permision_type=permision_type)
    if ver_result == PERMISSION_DENY_ERROR:
        return Response("permission denied.", status=403, mimetype='application/json')
    elif ver_result == UNAUTHENTICATION_ERROR:
        return Response("Unauthorized access.", status=401, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
