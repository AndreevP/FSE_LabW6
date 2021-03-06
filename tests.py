import unittest
import random
from runtime_utils import create_persons
from person import *

def get_random_virus():
    return get_infectable(InfectableType(random.randint(1, 3)))
def get_random_state():
    return random.choice([Healthy, Dead, AsymptomaticSick, SymptomaticSick])

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
                    
                    
if __name__ == '__main__':
    unittest.main()