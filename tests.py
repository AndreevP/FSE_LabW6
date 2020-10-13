import unittest
import random
from runtime_utils import create_persons
from person import *

def get_random_virus():
    return get_infectable(InfectableType(random.randint(1, 3)))
def get_random_state():
    return random.choice([Healthy, Dead, AsymptomaticSick, SymptomaticSick])
def get_random_state2():
    return random.choice([Healthy, AsymptomaticSick, SymptomaticSick])

class ContactingTestCase(unittest.TestCase):

    def setUp(self):      
        min_i, max_i = 0, 100 #this numbers can be arbitrary
        min_j, max_j = 0, 100
        n_persons = 3000
        self.persons = create_persons(min_j, max_j, min_i, max_i, n_persons)  
        for person in self.persons:
            state = get_random_state()
            if (state != Healthy): 
                person.virus = get_random_virus()
                person.set_state(state(person))
            elif (random.random() > 0.5): #a half of healthy people have antibodies
                person.antibody_types.add(type(get_random_virus()))

    def tearDown(self):
        pass

    def test_transmition(self):
        for p1 in self.persons:
            for p2 in self.persons:
                if (p1 is not p2) and (type(p2.state) == Healthy) and \
                   (type(p1.state) in [AsymptomaticSick, SymptomaticSick]) and \
                   (type(p1.virus) not in p2.antibody_types):
                    p1.interact(p2)
                    self.assertEqual(type(p2.state), AsymptomaticSick)
                    self.assertEqual(type(p1.virus), type(p2.virus))
                    
    def test_healthy_interaction(self):
        for p1 in self.persons:
            for p2 in self.persons:
                if (p1 is not p2) and (type(p2.state) == Healthy) and (type(p1.state) == Healthy):
                    p1.interact(p2)
                    self.assertEqual(type(p1.state), Healthy)
                    self.assertEqual(type(p2.state), Healthy)
                    
    def test_antibodies(self):
        for p1 in self.persons:
            for p2 in self.persons:
                if (p1 is not p2) and (type(p1.virus) in p2.antibody_types):
                    t = type(p2.state)
                    p1.interact(p2)
                    self.assertEqual(type(p2.state), t)
class HealthStateTestCase(unittest.TestCase):
    def setUp(self):
        min_i, max_i = 0, 100 #this numbers can be arbitrary
        min_j, max_j = 0, 100
        n_persons = 3000
        self.persons = create_persons(min_j, max_j, min_i, max_i, n_persons)
        for person in self.persons:
            state = get_random_state2()
            if (state != Healthy):
                person.virus = get_random_virus()
                person.set_state(state(person))
    def tearDown(self):
        pass

    def test_changingstate(self):
        for p1 in self.persons:
            p1.night_actions()
            if  (type(p1.state)==AsymptomaticSick):
                if (p1.state.days_sick ==1):
                    self.assertEqual(type(p1.state),AsymptomaticSick)
            p1.night_actions()
            if(type(p1.state)==SymptomaticSick):
                self.assertEqual(type(p1.state),SymptomaticSick)
    def test_fromsick2healthy(self):
        for p1 in self.persons:
            p1.night_actions()
            if (type(p1.state)==AsymptomaticSick):
                p1.night_actions()
                if(type(p1.state)==SymptomaticSick) and (p1.virus.strength >0):
                    self.assertEqual(type(p1.state), SymptomaticSick)
                elif (p1.virus.strength <0):
                    self.assertEqual(type(p1.state), Healthy)

if __name__ == '__main__':
    unittest.main()
