# Customates Python SDK

Welcome to Customate's Python SDK repository.
***
***
## More about customate
Customate is an API driven embedded payments platform that safeguards all funds, creates dedicated customer wallets and escrow wallets instantly, verifies your customers and enables you to create automated payment schedules to handle any incoming or outgoing payments.

Read more by visiting our main [website](https://gocustomate.com/)
***
***
## Supported Python Versions
This library supports the following Python implementations:

* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9
* Python 3.10
***
***
## Installation
Using pip:
```
pip install customate-sdk
```
This automatically installs customate v1.0 (or later).

Add API credentials to your settings:

```
#API keys for Customate
CUSTOMATE_KEY = ***Your public key supplied by Customate***
CUSTOMATE_SECRET_KEY = ***Your secret key supplied by Customate***
CUSTOMATE_URL= ***API URL***
CUSTOMATE_VERSION= ***API Version***
```
***
***
## Useage

Create Customate client:
```
#Import settings
CUSTOMATE_KEY = <CUSTOMATE_KEY>
CUSTOMATE_SECRET_KEY = <CUSTOMATE_SECRET_KEY>
CUSTOMATE_URL= <CUSTOMATE_URL>
CUSTOMATE_VERSION= <CUSTOMATE_VERSION>

from customate.rest import Client
client = Client(
    api_key = CUSTOMATE_KEY,
    secret=CUSTOMATE_SECRET_KEY,
    url=CUSTOMATE_URL,
    version=CUSTOMATE_VERSION
    )
```

Testing our client:

>Note: This is our API State endpoint.
```
status_response = client.status.get()
print(status_response.status_code)
```
***
***
## Endpoints

### Profile Management

>Note: Please see [Profile Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management/create-profile):
```
data = {
    "type": "personal",
    "first_name": "Jack",
    "middle_name": "Arthur",
    "last_name": "Smith",
    "email": "smith@customate.com",
    "phone_number": "+12126712234",
    "birth_date": "1990-02-28",
    "title": "mr",
    "gender": "male",
    "address": {
      "line_1": "Haziko",
      "line_2": "Boggs Road",
      "line_3": "",
      "city": "Tranent",
      "locality": "East Lothian",
      "postcode": "EH34 5AZ",
      "country": "GB"
    },
    "metadata": {
      "sample_internal_id": "998440c3-e046-450d-96bd-28b4c1cff11c"
    }
}
profile_response = client.profile.post(
    data=data
)
print(profile_response.status_code)
profile_id = profile_response['json']["id"]
```
***
[Get](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management/get-profile-details):
```
#Returns all profiles
profile_response = client.profile.get()
print(profile_response.status_code)

#Returns all profiles with pagination
profile_response = client.profile.get(
    params = {'page_size':25,'page_number':page_number}
)
print(profile_response.status_code)

#Passing a profile ID will retrieve one record
profile_response = client.profile.get(
    profile_id=profile_id
)
print(profile_response.status_code)
```
***
[Verify](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management/verify-profile):
```
#Force verifies your profile
profile_response = client.verification.post(
    profile_id = profile_id,
    params={"force_verification": 'true'}
)
print(profile_response.status_code)
```
***
[Update](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management/update-profile):
```
data = {
    "type": "personal",
    "first_name": "Jack",
    "middle_name": "Arthur",
    "last_name": "Smith",
    "email": "smith@customate.com",
    "phone_number": "+12126712234",
    "birth_date": "1990-02-28",
    "title": "mr",
    "gender": "male",
    "address": {
      "line_1": "Hazikos",
      "line_2": "Boggs Road",
      "line_3": "",
      "city": "Tranent",
      "locality": "East Lothian",
      "postcode": "EH34 5AZ",
      "country": "GB"
    },
    "metadata": {
      "sample_internal_id": "998440c3-e046-450d-96bd-28b4c1cff11c"
    }
}
profile_response = client.profile.put(
    data=data,
    profile_id=profile_id
)
print(profile_response.status_code)
```
***
[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/profile-management/deactivate-profile)
```
profile_response = client.profile.delete(
    profile_id=profile_id
)
print(profile_response.status_code)
```

***
***

### Wallet Management

>Note: Please see [Wallet Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/wallet-management)

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/wallet-management/get-profile-wallets):
```
#Returns all wallets for profile
wallet_response = client.profile.get(
    profile_id=profile_id
)
print(wallet_response.status_code)

#Returns all wallets for profile with pagination
wallet_response = client.profile.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(wallet_response.status_code)

#Passing a wallet ID will retrieve one record
wallet_response = client.profile.get(
    profile_id=profile_id,
    domain_id = wallet_id
)
print(wallet_response.status_code)
```
***
***

### Schedule Management

>Note: Please see [Schedule Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/create-schedule):
```
data = {
    "title": "Sample Weekly Schedule",
    "currency": "GBP",
    "purpose": "pay",
    "period": "one_time",
    "number_of_payments": 10,
    "regular_payment_start_date": "2020-06-23",
    "regular_payment_amount": 22000,
    "deposit_payment_date": "2020-06-22",
    "deposit_payment_amount": 1000,
    "description": "Apartment rental agreement 121",
    "metadata": {},
    "funding_source_id": "498752c7-57ba-42cd-88d0-81e1744e22b0",
    "backup_funding_source_id": "f4653129-a50c-42f6-b574-8bad264578e5",
    "payee_id": "cfcd44ad-12d5-4362-a669-2da49b9c6c52"
}
schedule_response = client.schedule.post(
    profile_id=profile_id,
    data=data
)
print(schedule_response.status_code)
schedule_id = schedule_response['json']["id"]
```
***

[Create DD to wallet schedule](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/create-direct-debit-to-wallet-schedule):
```
data = {
    "title": "Sample Weekly Schedule",
    "purpose": "pay",
    "period": "one_time",
    "number_of_payments": 10,
    "regular_payment_start_date": "2020-06-23",
    "regular_payment_amount": 22000,
    "deposit_payment_date": "2020-06-22",
    "deposit_payment_amount": 1000,
    "description": "Apartment rental agreement 121",
    "metadata": {},
    "funding_source_id": "498752c7-57ba-42cd-88d0-81e1744e22b0",
    "payee_id": "cfcd44ad-12d5-4362-a669-2da49b9c6c52"
}
schedule_response = client.direct_debit_to_wallet_schedules.post(
    profile_id=profile_id,
    data=data
)
print(schedule_response.status_code)
schedule_id = schedule_response['json']["id"]
```
***

[Pay overdue payments](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/pay-overdue-payments):
```
schedule_response = client.schedule.post(
    profile_id=profile_id,
    domain_id=schedule_id,
    domain_action=overdue_processing
)
print(schedule_response.status_code)
schedule_id = schedule_response['json']["id"]
```
***

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/get-schedule):
```
#Returns all schedules
schedule_response = client.schedule.get(
    profile_id=profile_id,
)
print(schedule_response.status_code)

#Returns all schedules with pagination
schedule_response = client.schedule.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(schedule_response.status_code)

#Passing a schedule ID will retrieve one record
schedule_response = client.schedule.get(
    profile_id=profile_id,
    domain_id=schedule_id
)
print(schedule_response.status_code)
```
***

[Update](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/update-schedule):
```
data = {
    "title": "Sample Weekly Schedule",
    "number_of_payments": 10,
    "regular_payment_amount": 22000,
    "description": "Apartment rental agreement 121",
    "metadata": {}
}
schedule_response = client.schedule.put(
    data=data,
    profile_id=profile_id,
    domain_id=schedule_id
)
print(schedule_response.status_code)
```
***
[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/schedule-management/delete-schedule)
```
schedule_response = client.schedule.delete(
    profile_id=profile_id,
    domain_id=schedule_id
)
print(schedule_response.status_code)
```


***
***

### Funding Source Management

>Note: Please see [Funding Source Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/create-funding-source):
```
data = {
    "title": "Sample DirectDebit Source",
    "currency": "GBP",
    "type": "direct_debit",
    "data": {
      "ownership": "single",
      "payer": {
        "full_name": "Jack Smith"
      },
      "account": {
        "sort_code": "040004",
        "account_number": "37618166"
      }
    }
  }
funding_source_response = client.funding_source.post(
    profile_id=profile_id,
    data=data
)
print(funding_source_response.status_code)
funding_source_id = funding_source_response['json']["id"]
```
***
[Create DD Funding Source](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/create-direct-debit-funding-source):
```
data = {
    "title": "Sample Direct Debit Source",
    "data": {
      "ownership": "single",
      "payer": {
        "full_name": "Jack Smith"
      },
      "account": {
        "sort_code": "040004",
        "account_number": "37618166"
      }
    }
}
funding_source_response = client.direct_debit_funding_source.post(
    profile_id=profile_id,
    data=data
)
print(funding_source_response.status_code)
funding_source_id = funding_source_response['json']["id"]
```
***
[Get](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/get-funding-source-details):
```
#Returns all funding sources
funding_source_response = client.funding_source.get(
    profile_id=profile_id,
)
print(funding_source_response.status_code)

#Returns all funding sources with pagination
funding_source_response = client.funding_source.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(funding_source_response.status_code)

#Passing a funding source ID will retrieve one record
funding_source_response = client.funding_source.get(
    profile_id=profile_id,
    domain_id=funding_source_id
)
print(funding_source_response.status_code)
```
***
[Validate](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/validate-funding-source):
```
#Check the supplied funding source and bank details are valid

data = {
    "title": "Personal DirectDebit",
    "payer": {
      "first_name": "Jack",
      "last_name": "Smith",
      "birth_date": "1980-01-01",
      "email": "joe@email.com",
      "address": {
        "address_line_1": "25 Buckingham Rd",
        "city": "Thorpe",
        "postcode": "YO25 2YH",
        "country": "United Kingdom"
      }
    }
}
funding_source_response = client.funding_source.put(
    data=data,
    profile_id=profile_id,
    domain_id=funding_source_id,
    domain_action="validate_bank_owner"
)
print(funding_source_response.status_code)
```
***
[Update](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/update-funding-source):
```
data = {
    "title": "Personal DirectDebit",
    "payer": {
      "email": "joe@email.com",
      "address": {
        "address_line_1": "25 Buckingham Rd",
        "city": "Thorpe",
        "postcode": "YO25 2YH",
        "country": "United Kingdom"
      }
    }
}
funding_source_response = client.funding_source.put(
    data=data,
    profile_id=profile_id,
    domain_id=funding_source_id
)
print(funding_source_response.status_code)
```
***
[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/funding-sources-management/delete-funding-source)
```
funding_source_response = client.funding_source.delete(
    profile_id=profile_id,
    domain_id=funding_source_id
)
print(funding_source_response.status_code)
```

***
***

### Open Banking Mandates

>Note: Please see [Open Banking Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/open-banking-mandates)

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/open-banking-mandates/get-open-banking-mandate-providers):
```
#Returns all open banking mandate providers
open_banking_response = client.open_banking_mandate_providers.get()
print(open_banking_response.status_code)
```
***

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/open-banking-mandates/create-open-banking-mandate):
```
data = {
    "provider_id": "ob-natwest-vrp-sandbox",
    "country": "GB",
    "currency": "GBP",
    "payer_name": "Mr A Payer",
    "payer_email": "smith@customate.com",
    "beneficiary_name": "Mrs A Receiver",
    "maximum_individual_amount": 10000,
    "maximum_payment_amount": 20000,
    "maximum_payment_period": "daily",
    "reference": "Tenancy agreement 1",
    "redirect_url": "https://www.yoursite.com/mandates",
    "valid_from_date": "2023-01-01",
    "valid_to_date": "2024-12-31"
}
open_banking_response = client.open_banking_to_wallet_mandates.post(
    profile_id=profile_id,
    data=data
)
print(open_banking_response.status_code)
open_banking_id = open_banking_response['json']["id"]
```
***

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/open-banking-mandates/list-open-banking-mandates):
```
#Returns all open banking mandates
open_banking_response = client.open_banking_mandates.get(
    profile_id=profile_id,
)
print(open_banking_response.status_code)

#Returns all open banking with pagination
open_banking_response = client.open_banking_mandates.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(open_banking_response.status_code)

#Passing a open banking mandate ID will retrieve one record
open_banking_response = client.open_banking_mandates.get(
    profile_id=profile_id,
    domain_id=open_banking_mandate_id
)
print(open_banking_response.status_code)
```
***

[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/open-banking-mandates/delete-open-banking-mandate)
```
open_banking_response = client.open_banking_mandates.delete(
    profile_id=profile_id,
    domain_id=open_banking_mandate_id
)
print(open_banking_response.status_code)
```

***
***

### Payee Management

>Note: Please see [Payee Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management/create-payee):
```
data = {
    "title": "Sample Bank Ltd.",
    "type": "bank_account",
    "currency": "GBP",
    "data": {
      "recipient": {
        "full_name": "",
        "email": "",
        "address": {
          "line_1": "Haziko",
          "line_2": "Boggs Road",
          "line_3": "",
          "city": "Tranent",
          "locality": "East Lothian",
          "postcode": "EH34 5AZ",
          "country": "GB"
        }
      },
      "account": {
        "iban": "SAPYGB2L40000031000001",
        "sort_code": "040004",
        "account_number": "37618166"
      }
    }
}
payee_response = client.payee.post(
    profile_id=profile_id,
    data=data
)
print(payee_response.status_code)
payee_id = payee_response['json']["id"]
```
***
[Get](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management/get-payee-details):
```
#Returns all payees
payee_response = client.payee.get(
    profile_id=profile_id,
)
print(payee_response.status_code)

#Returns all payees with pagination
payee_response = client.payee.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(payee_response.status_code)

#Passing a payee ID will retrieve one record
payee_response = client.payee.get(
    profile_id=profile_id,
    domain_id=payee_id
)
print(payee_response.status_code)
```
***
[Validate](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management/validate-payee):
```
#Check the supplied payee and bank details are valid

data = {
    "title": "Personal DirectDebit",
    "recipient": {
      "first_name": "Jack",
      "last_name": "Smith",
      "birth_date": "1980-01-01",
      "email": "joe@email.com",
      "address": {
        "address_line_1": "25 Buckingham Rd",
        "city": "Thorpe",
        "postcode": "YO25 2YH",
        "country": "United Kingdom"
      }
    }
}
payee_response = client.payee.put(
    data=data,
    profile_id=profile_id,
    domain_id=payee_id,
    domain_action="validate_bank_owner"
)
print(payee_response.status_code)
```
***
[Update](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management/update-payee):
```
data = {
    "title": "Payee",
    "recipient": {
      "email": "joe@email.com",
      "address": {
        "address_line_1": "25 Buckingham Rd",
        "city": "Thorpe",
        "postcode": "YO25 2YH",
        "country": "United Kingdom"
      }
    }
}
payee_response = client.payee.put(
    data=data,
    profile_id=profile_id,
    domain_id=payee_id
)
print(payee_response.status_code)
```
***
[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/payee-management/delete-payee)
```
payee_response = client.payee.delete(
    profile_id=profile_id,
    domain_id=payee_id
)
print(payee_response.status_code)
```


***
***

### Payment Management

>Note: Please see [Payment Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-payment):
```
data = {
    "amount": 1200,
    "description": "Deposit for apartment 121",
    "execution_date": "2022-04-12",
    "metadata": {
      "sample_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "funding_source_id": "12d24482-fbb1-4d9d-b41d-0d506ea4bc9b",
    "payee_id": "fdbf7995-84f6-4c28-b5e8-9ebec78c8edc"
}
payment_response = client.payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***
[Create wallet to wallet payment](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-wallet-to-wallet-payment):
```
data = {
    "amount": 1200,
    "description": "Deposit for apartment 121",
    "currency": "GBP",
    "execution_date": "2022-04-12",
    "metadata": {
      "sample_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "payee_id": "fdbf7995-84f6-4c28-b5e8-9ebec78c8edc"
}
payment_response = client.wallet_to_wallet_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***
[Create DD to wallet payment](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-direct-debit-to-wallet-payment):
```
data = {
    "amount": 1200,
    "description": "Deposit for apartment 121",
    "execution_date": "2022-04-12",
    "metadata": {
      "sample_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "funding_source_id": "12d24482-fbb1-4d9d-b41d-0d506ea4bc9b",
    "payee_id": "fdbf7995-84f6-4c28-b5e8-9ebec78c8edc"
}
payment_response = client.direct_debit_to_wallet_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***
[Create wallet to bank account payment](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-wallet-to-bank-account-payment):
```
data = {
    "amount": 1200,
    "description": "Deposit for apartment 121",
    "currency": "GBP",
    "execution_date": "2022-04-12",
    "metadata": {
      "sample_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "payee_id": "fdbf7995-84f6-4c28-b5e8-9ebec78c8edc"
}
payment_response = client.wallet_to_bank_account_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***

[Create open banking to wallet payment](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-open-banking-to-wallet-payment):
```
data = {
    "amount": 10000,
    "description": "Deposit for Flat 1",
    "country": "GB",
    "currency": "GBP",
    "redirect_url": "https://www.yoursite.com/payments",
    "metadata": {
      "client_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "provider_id": "mock-payments-gb-redirect",
    "payer_iban": "ES13ABBY09012606978360",
    "payer_name": "Mr A Payer",
    "beneficiary": "Mrs A Receiver"
}
payment_response = client.open_banking_to_wallet_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***


[Create (variable) open banking to mandate payment](https://customatepublicapi.docs.apiary.io/#reference/0/payments/create-(variable)-open-banking-to-wallet-mandate-payment):
```
data = {
    "amount": 10000,
    "description": "Deposit for Flat 1",
    "currency": "GBP",
    "metadata": {
      "sample_internal_id": "d2f148cf-901c-4fee-8792-21016da755a0"
    },
    "beneficiary_name": "Mrs A Receiver",
    "mandate_id": "ebfd76ac-6fc4-4661-9719-ff7bb3cc0360"
}

payment_response = client.open_banking_to_wallet_mandate_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***

[Create service payment](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/create-service-payment):
```
data = {
    "amount": 1200,
    "scenario": "IncomingBankTransfer",
    "description": "Deposit for apartment 121",
    "payee_id": "fdbf7995-84f6-4c28-b5e8-9ebec78c8edc"
}
payment_response = client.service_payment.post(
    profile_id=profile_id,
    data=data
)
print(payment_response.status_code)
payment_id = payment_response['json']["id"]
```
***

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/get-payment-details):
```
#Returns all payments
payment_response = client.payment.get(
    profile_id=profile_id,
)
print(payment_response.status_code)

#Returns all payments with pagination
payment_response = client.payment.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(payment_response.status_code)

#Passing a payments ID will retrieve one record
payment_response = client.payment.get(
    profile_id=profile_id,
    domain_id=payment_id
)
print(payment_response.status_code)
```

***
[Get open banking providers (for single payment)](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/get-open-banking-providers):
```
#Returns all banking providers
payment_response = client.open_banking_provider.get()
print(payment_response.status_code)

#Returns all banking providers for defined country and currency
payment_response = client.open_banking_provider.get(
    params = {'currency':'GBP','country':'UK'}
)
print(payment_response.status_code)

```

***

[Get non-processing dates](https://customatepublicapi.docs.apiary.io/#reference/0/payment-management/get-non-processing-dates):
```
#Returns all non-processing dates
payment_response = client.non_processing_date.get()
print(payment_response.status_code)

#Returns all non-processing dates with pagination
payment_response = client.non_processing_date.get(
    params = {'page_size':25,'page_number':page_number}
)
print(payment_response.status_code)

```

***
***

### Transaction Management

>Note: Please see [Transaction Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/transaction-management)

[Get](https://customatepublicapi.docs.apiary.io/#reference/0/transaction-management/get-transaction-details):
```
#Returns all transactions
transaction_response = client.transaction.get(
    profile_id=profile_id,
)
print(transaction_response.status_code)

#Returns all transactions with pagination
transaction_response = client.transaction.get(
    profile_id=profile_id,
    params = {'page_size':25,'page_number':page_number}
)
print(transaction_response.status_code)

#Returns all transactions with pagination and filtering and sorting
transaction_response = client.transaction.get(
    profile_id=profile_id,
    params = {
        'page_size':10,
        'page_number':1, 
        "sort": "-completion_date",
        "filters": {
            "amount.lte": 750,
            "creation_date.gte": "1564032580000",
            "creation_date.lte": "1564032592299",
            "completion_date.gte":"1564032580000",
            "completion_date.lte":"1564032592299",
        }}
)
print(transaction_response.status_code)

#Passing a transaction ID will retrieve one record
transaction_response = client.transaction.get(
    profile_id=profile_id,
    domain_id=transaction_id
)
print(transaction_response.status_code)
```

***
***

### Webhook Management

>Note: Please see [Webhook Management API Documentation](https://customatepublicapi.docs.apiary.io/#reference/0/webhook-management)

[Create](https://customatepublicapi.docs.apiary.io/#reference/0/webhook-management/create-webhook):
```
data = {
    "callback_url": "https://your-callback-url.com/webhook",
}
webhook_response = client.webhook.post(
    data=data
)
print(webhook_response.status_code)
webhook_id = webhook_response['json']["id"]
```
***
[Get](https://customatepublicapi.docs.apiary.io/#reference/0/webhook-management/get-webhook-details):
```
#Returns all webhooks
webhook_response = client.webhook.get()
print(webhook_response.status_code)

#Returns all webhooks with pagination
webhook_response = client.webhook.get(
    params = {'page_size':25,'page_number':page_number}
)
print(webhook_response.status_code)

#Passing a webhook ID will retrieve one record
webhook_response = client.webhook.get(
    domain_id=webhook_id
)
print(webhook_response.status_code)
```
***
[Update](https://customatepublicapi.docs.apiary.io/#reference/0/webhook-management/update-webhook):
```
data = {
    "callback_url": "https://your-callback-url.com/webhooks",
}
webhook_response = client.webhook.put(
    data=data,
    domain_id=webhook_id
)
print(webhook_response.status_code)
```
***
[Deactivate](https://customatepublicapi.docs.apiary.io/#reference/0/webhook-management/deactivate-webhook)
```
webhook_response = client.webhook.delete(
    domain_id=webhook_id
)
print(webhook_response.status_code)
```

***
***