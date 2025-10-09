# created: 2025-10-09
# updated: 2025-10-09
# author: Aaron Stichter
"""
This module is for creating, reading, updating and removing Customers and Pets from our customer database (customers.json).

This is part of the Snout Scheduler program for SDEV 220
"""

# imports
import json
from typing import List, Dict, Any


class Pet:
    """create Pet objects"""
    
    def __init__(self, name: str, species: str, treatment: List[str] | None = None):
        """initialize object"""

        self.name = name
        self.species = species
        self.treatment = treatment if treatment is not None else []

    
    def __repr__(self) -> str:
        """return Pet info"""

        return f"Pet(name={self.name!r}, species={self.species!r}, treatment={self.treatment!r})"



class Customer:
    """create Customer object"""

    def __init__(self, custID: int, last_name: str, first_name: str, phone_number: int, email: str, pets: List[Pet]):
        """initialize object"""
        
        self.custID = custID
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number
        self.email = email
        self.pets = pets


    


    def get_customer():

        with open('customers.json') as f:
            customers = json.load(f)