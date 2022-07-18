from time import sleep

from germany import Germany

users_dict = [
    {"status": 0, "reason": "Посещение родственников/друзей/знакомых", "surname": "Hvzodzeu", "name": "Yauheni",
     "email": "kojio6ok@tut.by",
     "passport_number": "MP4140001", "birth_day": "10/10/1985", "passport_issued": "13/04/2021",
     "passport_expired": "13/4/2031", "issued_by": "MIA", "phone_number": "375296090090", "nationality": "Belarus",
     "travel_date": "05/11/2022", "date_from": "13/07/2022", "date_to": "25/10/2022", "family": "1"}]


g = Germany(['TERMIN325', 'TERMIN340'], '375', users_dict)
date_slots = g.get_dates()
family_list = g.get_users_with_dates(date_slots)
g.register_users(family_list, date_slots)

