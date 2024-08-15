import random

import requests
from django.conf import settings


def check_and_redeem_voucher(voucher_token):
    api_url = 'http://cloudscript.business/api/voucher/'
    headers = {
        'Authorization': f'Token {settings.CLOUDSCRIPT_API_KEY}',  # Use "Token" prefix
    }

    # Ensure the voucher_token is correctly inserted into the URL
    check_url = f'{api_url}/check/{voucher_token}/'
    check_response = requests.get(check_url, headers=headers)

    if check_response.status_code == 200:
        voucher_data = check_response.json()
        if voucher_data.get('valid'):
            # Redeem the voucher (using POST method)
            redeem_url = f'{api_url}/redeem/{voucher_token}/'
            redeem_response = requests.post(redeem_url, headers=headers)

            if redeem_response.status_code == 200:
                return redeem_response.json()  # Successfully redeemed
            else:
                redeem_response.raise_for_status()
        else:
            return {'error': 'Invalid voucher token', 'voucher': voucher_data.get('valid')}
    else:
        check_response.raise_for_status()


def create_voucher_snippet(discount_amount):
    api_url = 'https://cloudscript.business/api/voucher/create/'  # Replace with the actual API URL
    headers = {
        'Authorization': f'Token {settings.CLOUDSCRIPT_API_KEY}',  # Use your API key
    }

    voucher_id = "MYTET557"
    payload = {

        "voucher_id": voucher_id,
        "voucher_name": "Test Voucher 2",
        "organisation": "Cloud Script",
        "facility": "string",
        "valid_from": "2024-08-13T14:15:22Z",
        "valid_to": "2025-08-24T14:15:22Z",
        "active": True,
        "voucher_type": "Discount",
        "product_type": "Food",
        "redeem_limit": 10000,
        "percent_off": 10,
        "amount_off": 0,
        "unit_off": 0,
        "currency": "tzs"

    }

    try:
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()  # Return the JSON response containing the voucher token

    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        return {'error': f'Other error occurred: {err}'}
