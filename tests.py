import unittest
import random
from runtime_utils import create_persons, create_hospitals, create_department_of_health
from person import *
from treatment import *

def get_random_virus():
    return get_infectable(InfectableType(random.randint(1, 3)))
def get_random_state():
    return random.choice([Healthy, Dead, AsymptomaticSick, SymptomaticSick])

class SymptomaticConditionTestCase(unittest.TestCase):

    def setUp(self):      
        min_i, max_i = 0, 100 #this numbers can be arbitrary
        min_j, max_j = 0, 100
        n_persons = 3000
        self.persons = create_persons(min_j, max_j, min_i, max_i, n_persons)
        self.hospitals = create_hospitals(3000)
        for person in self.persons:
            state = get_random_state()
            if (state != Healthy): 
                person.virus = get_random_virus()
                person.set_state(state(person))
        


    def tearDown(self):
        pass


    def test_fromsick2dead(self):
     #make sure there are at least 5 people have a life incompatible condition
        checked_people_count = 0
        dept_of_health = create_department_of_health(self.hospitals, self.persons)
        while  checked_people_count <= 5: 
            for p in self.persons:
                p.day_actions()
                if (p.is_life_incompatible_condition()):
                    checked_people_count += 1
                    self.assertEqual(type(p.state), Dead)

    def test_disease_prog(self):
        dept_of_health = create_department_of_health(self.hospitals, self.persons)
        for i in range(10):
            for p in self.persons:
                old_temp, old_water = p.temperature, p.water
                p.day_actions()
                if type(p.state) == SymptomaticSick:
                    if type(p.virus) == SeasonalFluVirus or type(p.virus) == SARSCoV2:
                        self.assertTrue(p.temperature > old_temp)
                    elif type(p.virus) == Cholera:
                        self.assertTrue(p.water < old_water)
                
if __name__ == '__main__':
    unittest.main()
