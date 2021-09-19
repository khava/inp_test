import json
import sys
from os import path, environ


from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from mptt.exceptions import InvalidMove

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
environ['DJANGO_SETTINGS_MODULE'] = 'inp_test.settings'
import django
django.setup()

from employees.models import Employee

with open('data.json', 'r', encoding='utf-8') as f:
    employees = json.load(f)

    # for employee in employees:
    #     (surname, name, third_name) = employee['name'].split()
    #     Employee.objects.create(
    #         name=name,
    #         surname=surname,
    #         third_name=third_name,
    #         position=employee['position'],
    #         salary=employee['salary'],
    #         employment_date=employee['date'],
    #     )
    
    for employee in employees:
        (chief_surname, chief_name, chief_third_name) = employee['chief'].split()
        (surname, name, third_name) = employee['name'].split()

        chief_id = Employee.objects.get(name=chief_name, surname=chief_surname, third_name=chief_third_name)
        
        if (chief_surname != surname and chief_name != name and chief_third_name != third_name):
            try:
                e = Employee.objects.get(name=name, surname=surname, third_name=third_name)
                e.chief = chief_id  
                e.save()                
            except ValidationError:
                if len(e.get_ancestors()) >= 3:
                    print(e, e.get_ancestors())
                    e.move_to(e.get_ancestors()[1])
                    e.save()
            except InvalidMove:
                pass
