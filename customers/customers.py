# created: 2025-10-09
# updated: 2025-10-10
# author: Aaron Stichter
"""
This module is for parsing and CRUD operations of our Customer and Pet objects from our customer database (customers.json).

This is part of the Snout Scheduler program for SDEV 220
"""

# imports
import json
from typing import List, Dict


class Pet:
    """This class creates Pet objects and provides parsing functions used by Repository class"""
    
    def __init__(self, name: str, species: str, treatment: List[str]):
        """initialize object"""

        self.name = name
        self.species = species
        self.treatment = treatment


    def from_json(data: Dict):
        """PARSING FUNC: create Pet object from dict data (or our customers.json in this case)"""

        return Pet(name=data["name"],
                   species=data["species"],
                   treatment=data.get("treatment", [])
                   )
    

    def to_json(self):
        """PARSING FUNC: serializes objects so they can be written back to json file"""

        return {"name": self.name,
                "species": self.species,
                "treatment": self.treatment
                }


    def __repr__(self):
        """return str of Pet object info"""

        return f"Pet(name={self.name!r}, species={self.species!r}, treatment={self.treatment!r})"



class Customer:
    """This class creates Customer objects and provides parsing functions used by Repository class"""

    def __init__(self, custID: int, last_name: str, first_name: str, phone_number: int, email: str, pets: List[Pet]):
        """initialize object"""
        
        self.custID = custID
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number
        self.email = email
        self.pets = pets


    def from_json(data: Dict):
        """PARSING FUNC: creates Customer object from dict data (or our customers.json in this case)"""

        pets = [Pet.from_json(p) for p in data.get("pets", [])]

        return Customer(custID=data["custID"],
                        last_name=data["last_name"],
                        first_name=data["first_name"],
                        phone_number=data["phone_number"],
                        email=data["email"],
                        pets=pets
                        )
    

    def to_json(self):
        """PARSING FUNC: serializes objects so they can be written back to json file"""

        return {
            "custID": self.custID,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "pets": [p.to_json() for p in self.pets]
                }


    def __repr__(self):
        """returns str of Customer object info"""

        return f"Customer(custID={self.custID!r}, last_name={self.last_name!r}, first_name={self.first_name!r}, phone_number={self.phone_number!r}, email={self.email!r}, pets={self.pets!r})"
    

    def add_pet(self, pet: Pet):
        """adds a pet to Customer object or raises error if pet with same name already exists"""

        if any(duplicate.name == pet.name for duplicate in self.pets):
            raise ValueError(f"This customer already has a pet named {pet.name}.")
        
        self.pets.append(pet)


    def remove_pet(self, pet_name: str):
        """removes pet from Customer object"""

        self.pets = [p for p in self.pets if p.name != pet_name]



class Repository:
    """
    This class acts as an intermediary between the db (customers.json) and the program,
    parsing the data and performing all CRUD operations
    """

    def __init__(self, path: str = "customers.json"):
        """sets path to our json file"""

        self.path = path

    
    def load_all(self):
        """reads and returns list of all Customer objects from json file"""

        with open(self.path, "r") as f:
            data = json.load(f)
        
        return [Customer.from_json(object) for object in data.get("customers", [])]
    

    def save_all(self, customers: List[Customer]):
        """writes the list of Customer objects back to json file"""

        objects = {"customers": [c.to_json() for c in customers]}

        with open(self.path, "w") as f:
            json.dump(objects, f, indent=4, sort_keys=True)


    # CRUD Operations
    def add_customer(self, customer: Customer):
        """saves a new Customer object to our json file"""

        db = self.load_all()

        if any(c.custID == customer.custID for c in db):
            raise ValueError(f"Customer with ID: {customer.custID} already exists")
        
        db.append(customer)
        self.save_all(db)

    
    def get_customer(self, cust_id: int):
        """retreives Customer object from json file or returns error message if no Customer exists at that custID"""

        for c in self.load_all():
            if c.custID == cust_id:
                return c
        
        return f"Customer does not exist"
    

    def update_customer(self, updated_cust: Customer):
        """replaces updated Customer object with current Customer object"""

        db = self.load_all()

        for index, current in enumerate(db):
            if current.custID == updated_cust.custID:
                db[index] = updated_cust
                break
        else:
            raise KeyError(f"No Customer with ID:{updated_cust.custID}")
        
        self.save_all(db)


    def delete_customer(self, cust_id: int):
        """removes Customer object from our json file"""

        db = self.load_all()
        customer_list = [c for c in db if c.custID != cust_id]

        if len(customer_list) == len(db):
            raise KeyError(f"Customer with ID:{cust_id}")
        
        self.save_all(db)