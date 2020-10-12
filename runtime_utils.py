from person import *
from infections import *
from treatment import *

class GlobalContext:
    def __init__(self, canvas, persons, health_dept):
        self.canvas = canvas
        self.persons = persons
        self.health_dept = health_dept

def simulate_day(context):
    persons, health_dept, hospitals = context.persons, context.health_dept, context.health_dept.hospitals

    health_dept.make_policy()
    
    for hospital in hospitals:
        hospital.treat_patients()
    
    for person in persons:
        person.day_actions()
    
    for person in persons:
        for other in persons:
            if person is not other and person.is_close_to(other):
                person.interact(other)
                
    for person in persons:
        person.night_actions()
        
from random import randint


def create_persons(min_j, max_j, min_i, max_i, n_persons):
    min_age, max_age = 1, 90
    min_weight, max_weight = 30, 120
    persons = [
        Person(
            home_position=(randint(min_j, max_j), randint(min_i, max_i)),
            age=randint(min_age, max_age),
            weight=randint(min_weight, max_weight),
        )
        for i in range(n_persons)
    ]
    return persons


def create_department_of_health(hospitals, persons):
    return DepartmentOfHealth(hospitals, persons)


def create_hospitals(n_hospitals):
    hospitals = [
        Hospital(capacity=100, drug_repository=ExpensiveDrugRepository())
        for i in range(n_hospitals)
    ]
    return hospitals


def initialize():
    # our little country
    min_i, max_i = 0, 100
    min_j, max_j = 0, 100
    
    # our citizen
    n_persons = 1000
    persons = create_persons(min_j, max_j, min_i, max_i, n_persons)
        
    # our healthcare system
    n_hospitals = 4
    hospitals = create_hospitals(n_hospitals)
    
    health_dept = create_department_of_health(hospitals, persons)
    
    # global context
    context = GlobalContext(
        (min_j, max_j, min_i, max_i),
        persons,
        health_dept
    )

    return context