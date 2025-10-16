import random, os
class ApiClient:
    def __init__(self, base=None):
        self.base = base or os.environ.get('BACKEND_API_BASE', 'MOCK')
    def find_customer(self, first_name, last_name, phone):
        return {'found': not phone.endswith('0000')}
    def list_services(self):
        return [{'id':0, 'name':'Bath','price_cents':3500},
                {'id':1,'name':'Haircut','price_cents':3500},
                {'id':2,'name':'Nail Trim','price_cents':3500},
                ]
    def list_groomers(self):
        return [{'id':0,'name':'Anyone'},
                {"id": 1, "name": "Alex"},
                {"id": 2, "name": "Riley"},
                {"id": 3, "name": "Sam"},
                {"id": 4, "name": "Jordan"},
                {"id": 5, "name": "Taylor"},
                ]
    def list_time_slots(self,date): return ['10:00','11:00','12:00','13:00']
    def submit_appointment_request(self,payload): return {'ok':True,'ref':f"SCOUT-{random.randint(100000,999999)}"}
