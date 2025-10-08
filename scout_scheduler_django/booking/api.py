import random, os
class ApiClient:
    def __init__(self, base=None):
        self.base = base or os.environ.get('BACKEND_API_BASE', 'MOCK')
    def find_customer(self, first_name, last_name, phone):
        return {'found': not phone.endswith('0000')}
    def list_services(self):
        return [{'id':1,'name':'Bath','price_cents':3500},{'id':2,'name':'Full Groom','price_cents':7000}]
    def list_groomers(self):
        return [{'id':0,'name':'Anyone'},{'id':1,'name':'Aaron'},{'id':2,'name':'Jody'}]
    def list_time_slots(self,date): return ['10:00','11:00','12:00','13:00']
    def submit_appointment_request(self,payload): return {'ok':True,'ref':f"SCOUT-{random.randint(100000,999999)}"}
