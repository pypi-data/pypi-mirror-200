import os
from customate.error import APIError
from customate.api_resources.mixins import hex_api_body, dict_json_convertor, PathBuilder
from customate.api_resources.api_requester import APIRequestor
import base64
import hmac
import hashlib
from datetime import datetime
from uuid import uuid4
import json
import requests



class Client(object):
    """ 
    A client for accessing the Customate API. 
    """
    
    def __init__(
        self, 
            api_key=None,
            secret=None, 
            version=None,
            environ=None,
            url=None,
            log=None,
        ):
        """
        Initializes the Customate Client
        :param str api_key: Key to authenticate with
        :param str secret: Secret to authenticate with
        :param str version: Customate version
        :param dict environ: Environment to look for auth details, defaults to os.environ
        :param str url: The url that API calls will be made
        :param bool log: If true will print helpful logs in terminal
        :returns: Customate Client
        :rtype: customate.rest.Client
        """
        environ = environ or os.environ
        self.api_key = api_key or environ.get('CUSTOMATE_KEY')
        self.secret = secret or environ.get('CUSTOMATE_SECRET_KEY')
        self.customate_version = version or environ.get('CUSTOMATE_VERSION')
        self.url = url or environ.get('CUSTOMATE_URL')
        self.log = log


        try:
            self.base_url = self.url
        except AttributeError:
            raise APIError("Use 'https://sandbox-api.gocustomate.com' or 'https://api.gocustomate.com' as CUSTOMATE_URL")
        

        if not self.api_key or not self.secret:
            raise APIError("Credentials are required to create a Customate Client")

        self.auth = (self.api_key, self.secret)

        # Domains
        self._profile = None
        self._status = None
        self._verification = None
        self._wallet = None
        self._schedule = None
        self._direct_debit_to_wallet_schedule = None
        self._wallet_to_wallet_payment = None
        self._direct_debit_to_wallet_payment = None
        self._wallet_to_bank_account_payment = None
        self._open_banking_to_wallet_mandate = None
        self._open_banking_to_wallet_mandate_payment = None
        self._open_banking_provider = None
        self._open_banking_mandate_provider = None
        self._open_banking_mandate = None
        self._open_banking_to_wallet_payment = None
        self._p2p_currency_exchange = None
        self._currency_exchange = None
        self._service_payment = None
        self._funding_source = None
        self._direct_debit_funding_source = None
        self._payee = None
        self._payment = None
        self._transaction = None
        self._webhook = None
        self._non_processing_date = None
        self._business = None


    def request(self, method, base_url, domain, version, profile_id=None, domain_id=None, domain_action=None, params=None, data=None, headers=None, auth=None):

        auth = auth or self.auth
        headers = headers or {}
        params = params or {}
        method = method.upper()

        path, url = PathBuilder(
            base_url=base_url,
            domain=domain,
            version=version,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action,
            params=params).build()

        nonce = str(uuid4())
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        custom_headers = {
            'Content-Type': '',
            'PaymentService-Date': now,
            'PaymentService-Nonce': nonce,
            'PaymentService-ContentHash': ''
        }

        base_path = f'{method}\n{path}'

        #add Httpmethod, Httppath and ContentType
        if method == "POST" or method == "PUT":
            custom_headers["Content-Type"] = "application/json"
            custom_headers["PaymentService-ContentHash"] = hex_api_body(data)
            content_type = custom_headers["Content-Type"]
        else:
            content_type = ""
        #FormattedCustomateHttpHeaders
        content_hash = f'paymentservice-contenthash:{custom_headers["PaymentService-ContentHash"]}'
        date = f'paymentservice-date:{custom_headers["PaymentService-Date"]}'
        nonce = f'paymentservice-nonce:{custom_headers["PaymentService-Nonce"]}'

        signature = "\n".join(
                [
                    method, # GET, POST, PUT, DELETE
                    path, # /v1/profiles/
                    content_type, # application/json or \n
                    content_hash, # json body sha1 hexed
                    date, # "2020-07-13T07:37:08-05:00"
                    nonce # "6110fb81-1247-4aa8-908d-11a9d5eda561"
                ]
            )

        if self.log:
            #sanity check
            print("API RESULTS:\n")
            print(f'Signature before encoding: \n{signature}\n\n')

        #convert to hex(sha256)
        hmac_hash = hmac.new(auth[1].encode('utf-8'), signature.encode('utf-8'), hashlib.sha256)

        #decode utf-8 base64
        hmac_signature = base64.b64encode(hmac_hash.digest()).decode('utf-8')

        #add hmac_signature to headers
        custom_headers['Authorization'] = f'Signature {auth[0]}:{hmac_signature}'

        if self.log:
            print(f'Custom headers: \n{custom_headers}\n\n')
            print(f'Endpoint (url): \n{url}\n\n')
        if data:
            new_data = dict_json_convertor(data)
            if self.log:
                print(f'Body: \n{new_data}\n\n')

        api = APIRequestor(
            url = url,
            headers = custom_headers,
            data = data,
        )

        if method == "POST":
            response = api.post()
        elif method == "PUT":
            response = api.put()
        elif method == "GET":
            response = api.get()
        elif method == "DELETE":
            response = api.delete()

        if method == "DELETE":
            if self.log:
                print(
                    f'Response:\nStatus:\n{response.status_code}\nMessage:\nObject deleted'
                )
            json_response = {}
        else:
            if self.log:
                print(
                    f'Response:\nStatus:\n{response.status_code}\nJson Response:\n{response.json()}'
                )
            json_response = response.json()
        return {
            "status": response.status_code,
            "json": json_response
        }
        

    @property
    def status(self):
        """
        Access the Customate Status API
        """
        if self._status is None:
            from customate.rest.status import Status
            self._status = Status(self, self.base_url, 'status', self.customate_version)
        return self._status


    @property
    def profile(self):
        """
        Access the Customate Profile API
        """
        if self._profile is None:
            from customate.rest.profile import Profile
            self._profile = Profile(self, self.base_url, 'profile',self.customate_version)
        return self._profile

    
    @property
    def verification(self):
        """
        Access the Customate Verification API
        """
        if self._verification is None:
            from customate.rest.verification import Verification
            self._verification = Verification(self, self.base_url, 'verification',self.customate_version)
        return self._verification
    
    @property
    def business(self):
        """
        Access the Customate Business API
        """
        if self._business is None:
            from customate.rest.business import Business
            self._business = Business(self, self.base_url, 'business', self.customate_version)
        return self._business

    @property
    def direct_debit_to_wallet_schedule(self):
        """
        Access the Customate Direct Debit To Wallet Payment API
        """
        if self._direct_debit_to_wallet_schedule is None:
            from customate.rest.direct_debit_to_wallet_schedule import DirectDebitToWalletSchedule
            self._direct_debit_to_wallet_schedule = DirectDebitToWalletSchedule(self, self.base_url, 'direct_debit_to_wallet_schedules', self.customate_version)
        return self._direct_debit_to_wallet_schedule

    @property
    def funding_source(self):
        """
        Access the Customate FundingSource API
        """
        if self._funding_source is None:
            from customate.rest.funding_source import FundingSource
            self._funding_source = FundingSource(self, self.base_url, 'funding_sources', self.customate_version)
        return self._funding_source

    @property
    def direct_debit_funding_source(self):
        """
        Access the Customate FundingSource API
        """
        if self._direct_debit_funding_source is None:
            from customate.rest.direct_debit_funding_source import DirectDebitFundingSource
            self._direct_debit_funding_source = DirectDebitFundingSource(self, self.base_url, 'direct_debit_funding_sources', self.customate_version)
        return self._direct_debit_funding_source

    @property
    def payee(self):
        """
        Access the Customate Payee API
        """
        if self._payee is None:
            from customate.rest.payee import Payee
            self._payee = Payee(self, self.base_url, 'payees', self.customate_version)
        return self._payee

    @property
    def payment(self):
        """
        Access the Customate Payment API
        """
        if self._payment is None:
            from customate.rest.payment import Payment
            self._payment = Payment(self, self.base_url, 'payment', self.customate_version)
        return self._payment

    @property
    def wallet_to_wallet_payment(self):
        """
        Access the Customate Wallet To Wallet Payment API
        """
        if self._wallet_to_wallet_payment is None:
            from customate.rest.wallet_to_wallet_payment import WalletToWalletPayment
            self._wallet_to_wallet_payment = WalletToWalletPayment(self, self.base_url, 'wallet_to_wallet_payments', self.customate_version)
        return self._wallet_to_wallet_payment

    @property
    def direct_debit_to_wallet_payment(self):
        """
        Access the Customate Direct Debit To Wallet Payment API
        """
        if self._direct_debit_to_wallet_payment is None:
            from customate.rest.direct_debit_to_wallet_payment import DirectDebitToWalletPayment
            self._direct_debit_to_wallet_payment = DirectDebitToWalletPayment(self, self.base_url, 'direct_debit_to_wallet_payments', self.customate_version)
        return self._direct_debit_to_wallet_payment

    @property
    def wallet_to_bank_account_payment(self):
        """
        Access the Customate Wallet To Bank Account Payment API
        """
        if self._wallet_to_bank_account_payment is None:
            from customate.rest.wallet_to_bank_account_payment import WalletToBankAccountPayment
            self._wallet_to_bank_account_payment = WalletToBankAccountPayment(self, self.base_url, 'wallet_to_bank_account_payments', self.customate_version)
        return self._wallet_to_bank_account_payment

    @property
    def open_banking_mandate(self):
        """
        Access the Customate Open Banking Mandate API
        """
        if self._open_banking_mandate is None:
            from customate.rest.open_banking_mandate import OpenBankingMandate
            self._open_banking_mandate = OpenBankingMandate(self, self.base_url, 'open_banking_mandates', self.customate_version)
        return self._open_banking_mandate

    @property
    def open_banking_to_wallet_mandate(self):
        """
        Access the Customate Open Banking To Wallet Mandate API
        """
        if self._open_banking_to_wallet_mandate is None:
            from customate.rest.open_banking_to_wallet_mandate import OpenBankingToWalletMandate
            self._open_banking_to_wallet_mandate = OpenBankingToWalletMandate(self, self.base_url, 'open_banking_to_wallet_mandates', self.customate_version)
        return self._open_banking_to_wallet_mandate

    @property
    def open_banking_to_wallet_mandate_payment(self):
        """
        Access the Customate Open Banking Mandate Payment API
        """
        if self._open_banking_to_wallet_mandate_payment is None:
            from customate.rest.open_banking_to_wallet_mandate_payment import OpenBankingToWalletMandatePayment
            self._open_banking_to_wallet_mandate_payment = OpenBankingToWalletMandatePayment(self, self.base_url, 'open_banking_to_wallet_mandate_payments', self.customate_version)
        return self._open_banking_to_wallet_mandate_payment

    @property
    def open_banking_provider(self):
        """
        Access the Customate Open Banking Provider API
        """
        if self._open_banking_provider is None:
            from customate.rest.open_banking_provider import OpenBankingProvider
            self._open_banking_provider = OpenBankingProvider(self, self.base_url, 'open_banking_providers', self.customate_version)
        return self._open_banking_provider

    @property
    def open_banking_mandate_provider(self):
        """
        Access the Customate Open Banking Mandate Provider API
        """
        if self._open_banking_mandate_provider is None:
            from customate.rest.open_banking_mandate_provider import OpenBankingMandateProvider
            self._open_banking_mandate_provider = OpenBankingMandateProvider(self, self.base_url, 'open_banking_mandate_providers', self.customate_version)
        return self._open_banking_mandate_provider

    @property
    def open_banking_to_wallet_payment(self):
        """
        Access the Customate Open Banking To Wallet Payment API
        """
        if self._open_banking_to_wallet_payment is None:
            from customate.rest.open_banking_to_wallet_payment import OpenBankingToWalletPayment
            self._open_banking_to_wallet_payment = OpenBankingToWalletPayment(self, self.base_url, 'open_banking_to_wallet_payments', self.customate_version)
        return self._open_banking_to_wallet_payment


    @property
    def service_payment(self):
        """
        Access the Customate Service Payment API
        """
        if self._service_payment is None:
            from customate.rest.service_payment import ServicePayment
            self._service_payment = ServicePayment(self, self.base_url, 'service_payments', self.customate_version)
        return self._service_payment

    @property
    def non_processing_date(self):
        """
        Access the Customate Non Processing Date Payment API
        """
        if self._non_processing_date is None:
            from customate.rest.non_processing_date import NoneProcessingDate
            self._non_processing_date = NoneProcessingDate(self, self.base_url, 'non_processing_dates', self.customate_version)
        return self._non_processing_date


    @property
    def p2p_currency_exchange(self):
        """
        Access the Customate P2P Currency Exchange API
        """
        if self._p2p_currency_exchange is None:
            from customate.rest.p2p_currency_exchange import P2PCurrencyExchange
            self._p2p_currency_exchange = P2PCurrencyExchange(self, self.base_url, 'p2p_currency_exchanges', self.customate_version)
        return self._p2p_currency_exchange

    @property
    def currency_exchange(self):
        """
        Access the Customate Currency Exchange API
        """
        if self._currency_exchange is None:
            from customate.rest.currency_exchange import CurrencyExchange
            self._currency_exchange = CurrencyExchange(self, self.base_url, 'currency_exchanges', self.customate_version)
        return self._currency_exchange


    @property
    def wallet(self):
        """
        Access the Customate Wallet API
        """
        if self._wallet is None:
            from customate.rest.wallet import Wallet
            self._wallet = Wallet(self, self.base_url, 'wallets', self.customate_version)
        return self._wallet

    @property
    def schedule(self):
        """
        Access the Customate Schedule API
        """
        if self._schedule is None:
            from customate.rest.schedule import Schedule
            self._schedule = Schedule(self, self.base_url, 'schedules', self.customate_version)
        return self._schedule


    @property
    def payment(self):
        """
        Access the Customate Payment API
        """
        if self._payment is None:
            from customate.rest.payment import Payment
            self._payment = Payment(self, self.base_url, 'payments', self.customate_version)
        return self._payment

    @property
    def transaction(self):
        """
        Access the Customate Transaction API
        """
        if self._transaction is None:
            from customate.rest.transaction import Transaction
            self._transaction = Transaction(self, self.base_url, 'transactions', self.customate_version)
        return self._transaction

    @property
    def webhook(self):
        """
        Access the Customate Webhook API
        """
        if self._webhook is None:
            from customate.rest.webhook import Webhook
            self._webhook = Webhook(self, self.base_url, 'webhooks', self.customate_version)
        return self._webhook