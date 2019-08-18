import uuid
import datetime
from service.database import Database
from models.base import BaseModel
from models.consts import *


class Hotel(BaseModel):

    def __init__(self, _id, name, description, timezone, address, website, logo_url, cover_url, loyalty_url,
                 loyalty_club, currency, create_time=None, update_time=None):
        super(Hotel, self).__init__(_id)
        self.name = name
        self.description = description
        self.timezone = timezone
        self.address = address
        self.website = website
        self.logo_url = logo_url
        self.cover_url = cover_url
        self.loyalty_url = loyalty_url
        self.loyalty_club = loyalty_club
        self.currency = currency
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "description": self.description,
            "timezone": self.timezone,
            "address": self.address,
            "website": self.website,
            "logo_url": self.logo_url,
            "cover_url": self.cover_url,
            "loyalty_url": self.loyalty_url,
            "loyalty_club": self.loyalty_club,
            "currency": self.currency,
            "create_time": self.create_time,
            "update_time": self.update_time
        }


class Accommodation(BaseModel):
    def __init__(self, _id, hotel_id, name, description, max_guests, image_url, create_time=None, update_time=None):
        super(Accommodation, self).__init__(_id)

        self.hotel_id = hotel_id
        self.name = name
        self.description = description
        self.max_guests = max_guests
        self.image_url = image_url
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "hotel_id": self.hotel_id,
            "name": self.name,
            "description": self.description,
            "max_guests": self.max_guests,
            "image_url": self.image_url,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    @staticmethod
    def find_accommodation(hotel_id):
        results = Accommodation.find(ACCOMODATION_COLLECTION, {"hotel_id": hotel_id})
        return results


class RoomInventory(BaseModel):
    def __init__(self, _id, accommodation_id, name, description, sell_start_date, sell_end_date,
                 daily_rates=None, create_time=None, update_time=None):
        super(RoomInventory, self).__init__(_id)
        self.accommodation_id = accommodation_id
        self.name = name
        if daily_rates == None:
            self.daily_rates = DailyRate.get_daily_rate_by_room_id(_id)
        else:
            self.daily_rates = daily_rates

        self.description = description
        self.sell_start_date = sell_start_date
        self.sell_end_date = sell_end_date
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "accommodation_id": self.accommodation_id,
            "name": self.name,
            "daily_rates" : self.daily_rates,
            "description": self.description,
            "sell_start_date": self.sell_start_date,
            "sell_end_date": self.sell_end_date,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    @staticmethod
    def find_rooms(hotel_id):
        accommodations = Accommodation.find_accommodation(hotel_id)
        accommodation_ids = [str(accommodation['_id']) for accommodation in accommodations]
        results = RoomInventory.find(ROOOM_INVENTORY_COLLECTION, {"accommodation_id": {"$in": accommodation_ids}})
        return results

    def add_new_room(self):
        room_id = self.create(ROOOM_INVENTORY_COLLECTION)

        for daily_rate in self.daily_rates:
            daily_rate_ob = DailyRate(_id=None, room_inventory_id=room_id,
                                      date=convert_date(daily_rate['date']),
                                      quantity=int(daily_rate['quantity']),
                                      remain=int(daily_rate['remain']),
                                      rate=int(daily_rate['rate']))
            daily_rate_ob.create(DAILY_RATES_COLLECTION)
        return room_id

    @staticmethod
    def search_room_inventory(hotel_id, check_in, check_out, adults, **kwargs):
        accommodations = Accommodation.find(ACCOMODATION_COLLECTION, {"hotel_id": hotel_id,
                                                                      "max_guests" : {"$gte" : adults}})
        accommodation_ids = [str(accommodation['_id']) for accommodation in accommodations]

        rooms = RoomInventory.find(ROOOM_INVENTORY_COLLECTION, {"accommodation_id": {"$in": accommodation_ids},
                                                        "sell_start_date": {"$lte" : check_in},
                                                        "sell_end_date": {"$gte" : check_out}})

        availabe_rooms = [ room for room in rooms if len(room['daily_rates']) > 0]

        return availabe_rooms


class DailyRate(BaseModel):
    def __init__(self, _id, room_inventory_id, date, quantity, remain, rate, create_time=None, update_time=None):
        super(DailyRate, self).__init__(_id)
        self.room_inventory_id = room_inventory_id
        self.date = date
        self.quantity = quantity
        self.remain = remain
        self.rate = rate
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "room_inventory_id": self.room_inventory_id,
            "date": self.date,
            "quantity": self.quantity,
            "remain": self.remain,
            "rate": self.rate,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    @classmethod
    def get_daily_rate_by_room_id(cls, room_inventory_id, **kwargs):
        query = {"room_inventory_id": room_inventory_id}
        if 'check_in' in kwargs:
            query = {
                'date': {'$gte': kwargs['check_in'], '$lte': kwargs['check_out']},
                'room_inventory_id': room_inventory_id
            }

        daily_rates = cls.Database.find(collection="daily_rate", query=query)

        return [cls(**rate).to_json() for rate in daily_rates]

    @classmethod
    def update_booking_from_json(cls, json_data):
        daily_rate = cls(**json_data)
        if daily_rate.remain < 0:
            return False

        daily_rate.remain -= 1
        query = {"_id": daily_rate._id}
        daily_rate.update(DAILY_RATES_COLLECTION, query=query)

        return True


class Reservation(BaseModel):
    def __init__(self, _id, room_inventory_id, check_in, check_out, adults, children, first_name, last_name,
                 email, phone, message, conf_number, status, create_time=None, update_time=None):
        super(Reservation, self).__init__(_id)
        self.room_inventory_id = room_inventory_id
        self.check_in = check_in
        self.check_out = check_out
        self.adults = adults
        self.children = children
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.phone = phone
        self.message = message
        self.conf_number = conf_number
        self.status = status
        self.create_time = create_time
        self.update_time = update_time

    def to_json(self):
        return {
            "_id": self._id,
            "room_inventory_id": self.room_inventory_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "adults": self.adults,
            "children": self.children,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "phone": self.phone,
            "message": self.message,
            "conf_number": self.conf_number,
            "status": self.status,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

    @staticmethod
    def find_reservation(hotel_id, status):
        rooms = RoomInventory.find_rooms(hotel_id)
        room_inventory_ids = [room['_id'] for room in rooms]
        results = Reservation.find(RESERVATION_COLLECTION,
                                {"room_inventory_id": {"$in": room_inventory_ids}, "status": status})

        return results

    @staticmethod
    def confirm_reservation(reservation_id, conf_number):
        reservation = Reservation.get_one_by_id(RESERVATION_COLLECTION, reservation_id)
        status = RESERVATION_STATUS_ENUM[conf_number]
        reservation = Reservation(**reservation)
        reservation.conf_number = conf_number
        reservation.status = status
        reservation.update(RESERVATION_COLLECTION, {"_id": reservation._id})

        return reservation_id, status

    def guest_booking(self):
        daily_rates = DailyRate.get_daily_rate_by_room_id(self.room_inventory_id,
                                                          check_in=self.check_in, check_out=self.check_out)
        if len(daily_rates) <= 0:
            return False

        daily_rate = daily_rates[0]
        result = DailyRate.update_booking_from_json(daily_rate)

        if not result:
            return False
        self.create(RESERVATION_COLLECTION)
        return True