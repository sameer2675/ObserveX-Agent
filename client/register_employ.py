from config import REGISTER_EMPLOYEE_API
from client.client import post

def register_employee(data):
    return post(
       REGISTER_EMPLOYEE_API,
        data
    )