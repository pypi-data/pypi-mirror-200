import hashlib
import json

from urllib.parse import urlencode

def create_params(**kwargs):
    '''
    Used to create url parameters for API call
    '''
    url = kwargs.get("url")
    params = kwargs.get("params")
    if params:
        query_string = urlencode(eval(params))
    return f'{url}?{query_string}'

def hex_api_body(body):
    #convert body to hex (sha1)
    #https://www.freeformatter.com/hmac-generator.html
    encoded_body = dict_json_convertor(body).encode('utf-8')
    sha_1 = hashlib.sha1()
    sha_1.update(encoded_body)
    hex_body = sha_1.hexdigest()
    return hex_body

def dict_json_convertor(my_dict):
    '''
	Ensure the body matches the encoded hex
	'''
    return json.dumps(my_dict, indent=4)


class PathBuilder:

    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url')
        self.domain = kwargs.get('domain')
        self.version = kwargs.get('version')
        self.profile_id = kwargs.get("profile_id")
        self.domain_id = kwargs.get("domain_id")
        self.domain_action = kwargs.get("domain_action")
        self.params = kwargs.get('params')
        

    def build(self):
        paths = {
            "domains":{
                "status": { 
                    "path": f'{self.version}/status',
                    "name": None
                },
                "profile": {
                    "path": f'{self.version}/profiles',
                    "name": None
                },
                "verification": {
                    "path": f'{self.version}/profiles',
                    "name": "verification"
                },
                "business": {
                    "path": f'{self.version}/profiles',
                    "name": "business"
                },
                "funding_sources": {
                    "path": f'{self.version}/profiles',
                    "name": "funding_sources"
                },
                "direct_debit_funding_sources": {
                    "path": f'{self.version}/profiles',
                    "name": "direct_debit_funding_sources"
                },
                "payees": {
                    "path": f'{self.version}/profiles',
                    "name": "payees"
                },
                "direct_debit_to_wallet_schedules": {
                    "path": f'{self.version}/profiles',
                    "name": "direct_debit_to_wallet_schedules"
                },
                "payments": {
                    "path": f'{self.version}/profiles',
                    "name": "payments"
                },
                "wallet_to_wallet_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "wallet_to_wallet_payments"
                },
                "direct_debit_to_wallet_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "direct_debit_to_wallet_payments"
                },
                "wallet_to_bank_account_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "wallet_to_bank_account_payments"
                },
                "open_banking_providers": {
                    "path": f'{self.version}/open_banking_providers',
                    "name": None
                },
                "open_banking_to_wallet_mandate_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "open_banking_to_wallet_mandate_payments"
                },
                "open_banking_to_wallet_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "open_banking_to_wallet_payments"
                },
                "open_banking_mandate_providers": {
                    "path": f'{self.version}/open_banking_mandate_providers',
                    "name": None
                },
                "open_banking_to_wallet_mandates": {
                    "path": f'{self.version}/profiles',
                    "name": "open_banking_to_wallet_mandates"
                },
                "open_banking_mandates": {
                    "path": f'{self.version}/profiles',
                    "name": "open_banking_mandates"
                },
                
                "service_payments": {
                    "path": f'{self.version}/profiles',
                    "name": "service_payments"
                },
                
                "p2p_currency_exchanges":{
                    "path": f'{self.version}/profiles',
                    "name": "p2p_currency_exchanges"
                },
                "currency_exchanges":{
                    "path": f'{self.version}/profiles',
                    "name": "currency_exchanges"
                },
                "wallets": {
                    "path": f'{self.version}/profiles',
                    "name": "wallets"
                },
                "schedules": {
                    "path": f'{self.version}/profiles',
                    "name": "schedules"
                },
                "transactions": {
                    "path": f'{self.version}/profiles',
                    "name": "transactions"
                },
                "webhooks": {
                    "path": f'{self.version}/webhooks',
                    "name": None
                },
                "non_processing_dates": {
                    "path": f'{self.version}/non_processing_dates',
                    "name": None
                },
            },
        }
        domain_info = paths['domains'][self.domain]
        sections = [domain_info['path']]
        if self.profile_id:
            sections.append(self.profile_id)
        if domain_info["name"]:
            sections.append(domain_info["name"])
            if self.domain_id:
                sections.append(self.domain_id)
                if self.domain_action:
                    sections.append(self.domain_action)
        
        path = f'/{"/".join(sections)}'
        url = f'{self.base_url}{path}'
        #manage params
        params = {}
        if "page_number" in self.params:
            params['page[number]'] = self.params["page_number"]
        if "page_size" in self.params:
            params['page[size]'] = self.params["page_size"]
        if "force_verification" in self.params:
            params['force_verification'] = self.params["force_verification"]
        if "validate_bank_owner" in self.params:
            params['validate_bank_owner'] = self.params["validate_bank_owner"]
        if "currency" in self.params:
            params['currency[Currency]'] = self.params["currency"]
        if "country" in self.params:
            params['country[string]'] = self.params["country"]
        if "funding_source_id" in self.params:
            params['funding_source_id'] = self.params["funding_source_id"]
        if "funding_source_type" in self.params:
            params['funding_source_type'] = self.params["funding_source_type"]
        if "payee_id" in self.params:
            params['payee_id'] = self.params["payee_id"]
        if "business_id" in self.params:
            params['business_id'] = self.params["business_id"]
        if "payee_type" in self.params:
            params['payee_type'] = self.params["payee_type"]
        if "interval_start_date" in self.params:
            params['interval_start_date'] = self.params["interval_start_date"]
        if "interval_end_date" in self.params:
            params['interval_end_date'] = self.params["interval_end_date"]
        if "sort" in self.params:
            params['sort'] = self.params["sort"]
        if "filters" in self.params:
            for key, value in self.params["filters"].items():
                params[f'filter[{key}]'] = value
        if params:
            url = create_params(params=json.dumps(params), url=url)

        return [path, url]