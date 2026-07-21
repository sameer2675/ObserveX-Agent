from config import COMPANY_INFO_API
from client.client import post


def get_company_info(secret_token):

    return post(
        COMPANY_INFO_API,
        {
            "secret_token": secret_token
        }
    )