from abc import ABC, abstractmethod
from infections import *

class Drug(ABC):
    def apply(self, person):
        # somehow reduce person's symptoms
        pass


class AntipyreticDrug(Drug): pass


class Aspirin(AntipyreticDrug):
    '''A cheaper version of the fever/pain killer.'''
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 0.5
        
    def apply(self, person):
        person.temperature = max(36.6, person.temperature - self.dose * self.efficiency)


class Ibuprofen(AntipyreticDrug):
    '''A more efficient version of the fever/pain killer.'''
    def __init__(self, dose):
        self.dose = dose
        
    def apply(self, person):
        person.temperature = 36.6


class RehydrationDrug(Drug): pass

class Glucose(RehydrationDrug):
    '''A cheaper version of the rehydration drug.'''
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 0.1
        
    def apply(self, person):
        person.water = min(person.water + self.dose * self.efficiency,
                            0.6 * person.weight)


class Rehydron(RehydrationDrug):
    '''A more efficient version of the rehydration drug.'''
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 1.0
        
    def apply(self, person):
        person._water = 0.6 * person.weight


class AntivirusDrug(Drug): pass

class Placebo(AntivirusDrug):
    def __init__(self, dose):
        self.dose = dose

    def apply(self, person): pass


class AntivirusSeasonalFlu(AntivirusDrug):
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 1.0
        
    def apply(self, person):
        if isinstance(person.virus, SeasonalFluVirus):
            person.virus.strength -= self.dose * self.efficiency
            
        elif isinstance(person.virus, SARSCoV2):
            person.virus.strength -= self.dose * self.efficiency / 10.0


class AntivirusSARSCoV2(AntivirusDrug):
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 0.1
        
    def apply(self, person):
        if isinstance(person.virus, SARSCoV2):
            person.virus.strength -= self.dose * self.efficiency


class AntivirusCholera(AntivirusDrug):
    def __init__(self, dose):
        self.dose = dose
        self.efficiency = 0.1
        
    def apply(self, person):
        if isinstance(person.virus, Cholera):
            person.virus.strength -= self.dose * self.efficiency

            
from typing import List


class DrugRepository(ABC):
    def __init__(self):
        self.treatment = []
        
    @abstractmethod
    def get_antifever(self, dose) -> Drug: pass
    
    @abstractmethod
    def get_rehydration(self, dose) -> Drug: pass
    
    @abstractmethod
    def get_seasonal_antivirus(self, dose) -> Drug: pass
    
    @abstractmethod
    def get_sars_antivirus(self, dose) -> Drug: pass
    
    @abstractmethod
    def get_cholera_antivirus(self, dose) -> Drug: pass
    
    def get_treatment(self):
        return self.treatment


class CheapDrugRepository(DrugRepository):
    def get_antifever(self, dose) -> Drug:
        return Aspirin(dose)

    def get_rehydration(self, dose) -> Drug:
        return Glucose(dose)

    def get_seasonal_antivirus(self, dose) -> Drug:
        return Placebo(dose)

    def get_sars_antivirus(self, dose) -> Drug:
        return Placebo(dose)

    def get_cholera_antivirus(self, dose) -> Drug:
        return Placebo(dose)


class ExpensiveDrugRepository(DrugRepository):
    def get_antifever(self, dose) -> Drug:
        return Ibuprofen(dose)

    def get_rehydration(self, dose) -> Drug:
        return Rehydron(dose)

    def get_seasonal_antivirus(self, dose) -> Drug:
        return AntivirusSeasonalFlu(dose)

    def get_sars_antivirus(self, dose) -> Drug:
        return AntivirusSARSCoV2(dose)

    def get_cholera_antivirus(self, dose) -> Drug:
        return AntivirusCholera(dose)            

class AbstractPrescriptor(ABC):
    def __init__(self, drug_repository):
        self.drug_repository = drug_repository
        
    @abstractmethod
    def create_prescription(self) -> List[Drug]:
        pass
    

class SeasonalFluPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, antifever_dose=1, antivirus_dose=1):
        super().__init__(drug_repository)
        self.antifever_dose = antifever_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_antifever(self.antifever_dose),
            self.drug_repository.get_seasonal_antivirus(self.antivirus_dose)
        ]

    
class CovidPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, antifever_dose=1, antivirus_dose=1):
        super().__init__(drug_repository)
        self.antifever_dose = antifever_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_antifever(self.antifever_dose),
            self.drug_repository.get_sars_antivirus(self.antivirus_dose)
        ]


class CholeraPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, rehydradation_dose=1, antivirus_dose=1):
        super().__init__(drug_repository)
        self.rehydradation_dose = rehydradation_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_rehydration(self.rehydradation_dose),
            self.drug_repository.get_cholera_antivirus(self.antivirus_dose)
        ]


def get_prescription_method(disease_type, drug_repository):
    if SeasonalFluVirus == disease_type:
        return SeasonalFluPrescriptor(drug_repository)

    elif SARSCoV2 == disease_type:
        return CovidPrescriptor(drug_repository)

    elif Cholera == disease_type:
        return CholeraPrescriptor(drug_repository)

    else:
        raise ValueError()    
    
    
class Hospital:
    def __init__(self, capacity, drug_repository):
        self.drug_repository = drug_repository
        self.capacity = capacity
        self.patients = []

    def _treat_patient(self, patient):
        # 1. identify disease
        if patient.virus is not None:
             disease_type = type(patient.virus)
        else:
            return
        prescription_method = get_prescription_method(disease_type, self.drug_repository)
        
        # 2. understand dose
        
        # 3. compose treatment
        prescription_drugs = prescription_method.create_prescription()
        
        # 4. apply treatment
        for drug in prescription_drugs:
          #  patient.take_drug(drug)
            drug.apply(patient)

    def treat_patients(self):
        for patient in self.patients:
            self._treat_patient(patient)
            
def singleton(cls):
    instances = {}
    def getinstance(*args):
        if cls not in instances:
            instances[cls] = cls(*args)
        return instances[cls]
    return getinstance

@singleton
class DepartmentOfHealth:
    def __init__(self, hospitals, persons):
        self.hospitals = hospitals
        self.persons = persons
        for p in persons:
            p.registration(self)
        self.situation = {"infected" : 0, "hospitalized":0,
                          "dead":0, "recovered":0}
        self.full = False
    
    def hospitalize(self, Person):
        if self.full:
            return
        succes = False
        for hospital in self.hospitals:
            if hospital.capacity > len(hospital.patients):
                hospital.patients.append(Person)
                succes = True
                self.situation["hospitalized"] += 1
                break
        if not succes: 
            print("Hospitals are full!!")
            self.full = True
    
    def make_policy(self):
        pass
    
    def monitor_situation(self, person, status):
        self.situation[status] += 1 
    