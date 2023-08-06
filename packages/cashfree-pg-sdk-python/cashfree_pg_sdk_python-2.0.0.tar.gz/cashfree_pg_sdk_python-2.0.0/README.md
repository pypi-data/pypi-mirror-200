# cashfree-pg-sdk-python

- API version: 2022-01-01
- Package version: 2.0.0

---

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage

### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```

(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:

```python
import cashfree_pg_sdk_python
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```

(or `sudo python setup.py install` to install the package for all users)

Then import the package:

```python
import cashfree_pg_sdk_python
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function

import time
import cashfree_pg_sdk_python
from cashfree_pg_sdk_python.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sandbox.cashfree.com/pg
# See configuration.py for a list of all supported configuration parameters.
configuration = CFPython_sdk.Configuration(
    host = "https://sandbox.cashfree.com/pg"
)



# Enter a context with an instance of the API client
with CFPython_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = CFPython_sdk.OrdersApi(api_client)
    x_client_id = 'x_client_id_example' # str |
x_client_secret = 'x_client_secret_example' # str |
x_api_version = '2022-01-01' # str |  (optional) (default to '2022-01-01')
x_idempotency_replayed = False # bool |  (optional) (default to False)
x_idempotency_key = 'x_idempotency_key_example' # str |  (optional)
x_request_id = 'x_request_id_example' # str |  (optional)
cf_order_request = CFPython_sdk.CFOrderRequest() # CFOrderRequest |  (optional)

    try:
        # Create Order
        api_response = api_instance.create_order(x_client_id, x_client_secret, x_api_version=x_api_version, x_idempotency_replayed=x_idempotency_replayed, x_idempotency_key=x_idempotency_key, x_request_id=x_request_id, cf_order_request=cf_order_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrdersApi->create_order: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://sandbox.cashfree.com/pg*

| Class             | Method                                                                                         | HTTP request                                                            | Description                           |
| ----------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------- |
| _OrdersApi_       | [**create_order**](docs/OrdersApi.md#create_order)                                             | **POST** /orders                                                        | Create Order                          |
| _OrdersApi_       | [**get_order**](docs/OrdersApi.md#get_order)                                                   | **GET** /orders/{order_id}                                              | Get Order                             |
| _OrdersApi_       | [**order_pay**](docs/OrdersApi.md#order_pay)                                                   | **POST** /orders/sessions                                               | Order Pay                             |
| _OrdersApi_       | [**preauthorization**](docs/OrdersApi.md#preauthorization)                                     | **POST** /orders/{order_id}/authorization                               | Preauthorization                      |
| _PaymentLinksApi_ | [**cancel_payment_link**](docs/PaymentLinksApi.md#cancel_payment_link)                         | **POST** /links/{link_id}/cancel                                        | Cancel Payment Link                   |
| _PaymentLinksApi_ | [**create_payment_link**](docs/PaymentLinksApi.md#create_payment_link)                         | **POST** /links                                                         | Create Payment Link                   |
| _PaymentLinksApi_ | [**get_payment_link_details**](docs/PaymentLinksApi.md#get_payment_link_details)               | **GET** /links/{link_id}                                                | Fetch Payment Link Details            |
| _PaymentLinksApi_ | [**get_payment_link_orders**](docs/PaymentLinksApi.md#get_payment_link_orders)                 | **GET** /links/{link_id}/orders                                         | Get Orders for a Payment Link         |
| _PaymentsApi_     | [**get_paymentby_id**](docs/PaymentsApi.md#get_paymentby_id)                                   | **GET** /orders/{order_id}/payments/{cf_payment_id}                     | Get Payment by ID                     |
| _PaymentsApi_     | [**get_paymentsfororder**](docs/PaymentsApi.md#get_paymentsfororder)                           | **GET** /orders/{order_id}/payments                                     | Get Payments for an Order             |
| _RefundsApi_      | [**createrefund**](docs/RefundsApi.md#createrefund)                                            | **POST** /orders/{order_id}/refunds                                     | Create Refund                         |
| _RefundsApi_      | [**get_refund**](docs/RefundsApi.md#get_refund)                                                | **GET** /orders/{order_id}/refunds/{refund_id}                          | Get Refund                            |
| _RefundsApi_      | [**getallrefundsfororder**](docs/RefundsApi.md#getallrefundsfororder)                          | **GET** /orders/{order_id}/refunds                                      | Get All Refunds for an Order          |
| _SettlementsApi_  | [**getsettlements**](docs/SettlementsApi.md#getsettlements)                                    | **GET** /orders/{order_id}/settlements                                  | Get Settlements                       |
| _TokenVaultApi_   | [**delete_specific_saved_instrument**](docs/TokenVaultApi.md#delete_specific_saved_instrument) | **DELETE** /customers/{customer_id}/instruments/{instrument_id}         | Delete Saved Instrument               |
| _TokenVaultApi_   | [**fetch_all_saved_instruments**](docs/TokenVaultApi.md#fetch_all_saved_instruments)           | **GET** /customers/{customer_id}/instruments                            | Fetch All Saved Instruments           |
| _TokenVaultApi_   | [**fetch_cryptogram**](docs/TokenVaultApi.md#fetch_cryptogram)                                 | **GET** /customers/{customer_id}/instruments/{instrument_id}/cryptogram | Fetch cryptogram for saved instrument |
| _TokenVaultApi_   | [**fetch_specific_saved_instrument**](docs/TokenVaultApi.md#fetch_specific_saved_instrument)   | **GET** /customers/{customer_id}/instruments/{instrument_id}            | Fetch Single Saved Instrument         |

## Documentation For Models

- [CFApp](docs/CFApp.md)
- [CFAppPayment](docs/CFAppPayment.md)
- [CFAuthorizationInPaymentsEntity](docs/CFAuthorizationInPaymentsEntity.md)
- [CFAuthorizationRequest](docs/CFAuthorizationRequest.md)
- [CFCard](docs/CFCard.md)
- [CFCardEMI](docs/CFCardEMI.md)
- [CFCardPayment](docs/CFCardPayment.md)
- [CFCardlessEMI](docs/CFCardlessEMI.md)
- [CFCardlessEMIPayment](docs/CFCardlessEMIPayment.md)
- [CFCryptogram](docs/CFCryptogram.md)
- [CFCustomerDetails](docs/CFCustomerDetails.md)
- [CFEMIPayment](docs/CFEMIPayment.md)
- [CFError](docs/CFError.md)
- [CFFetchAllSavedInstruments](docs/CFFetchAllSavedInstruments.md)
- [CFLink](docs/CFLink.md)
- [CFLinkCancelledResponse](docs/CFLinkCancelledResponse.md)
- [CFLinkCustomerDetailsEntity](docs/CFLinkCustomerDetailsEntity.md)
- [CFLinkMetaEntity](docs/CFLinkMetaEntity.md)
- [CFLinkNotifyEntity](docs/CFLinkNotifyEntity.md)
- [CFLinkOrders](docs/CFLinkOrders.md)
- [CFLinkRequest](docs/CFLinkRequest.md)
- [CFNetbanking](docs/CFNetbanking.md)
- [CFNetbankingPayment](docs/CFNetbankingPayment.md)
- [CFOrder](docs/CFOrder.md)
- [CFOrderMeta](docs/CFOrderMeta.md)
- [CFOrderPayData](docs/CFOrderPayData.md)
- [CFOrderPayRequest](docs/CFOrderPayRequest.md)
- [CFOrderPayResponse](docs/CFOrderPayResponse.md)
- [CFOrderRequest](docs/CFOrderRequest.md)
- [CFPaylater](docs/CFPaylater.md)
- [CFPaylaterPayment](docs/CFPaylaterPayment.md)
- [CFPaymentMethod](docs/CFPaymentMethod.md)
- [CFPaymentURLObject](docs/CFPaymentURLObject.md)
- [CFPaymentsEntity](docs/CFPaymentsEntity.md)
- [CFPaymentsEntityApp](docs/CFPaymentsEntityApp.md)
- [CFPaymentsEntityAppPayment](docs/CFPaymentsEntityAppPayment.md)
- [CFPaymentsEntityCard](docs/CFPaymentsEntityCard.md)
- [CFPaymentsEntityCardPayment](docs/CFPaymentsEntityCardPayment.md)
- [CFPaymentsEntityCardlessEMI](docs/CFPaymentsEntityCardlessEMI.md)
- [CFPaymentsEntityCardlessEMIPayment](docs/CFPaymentsEntityCardlessEMIPayment.md)
- [CFPaymentsEntityMethod](docs/CFPaymentsEntityMethod.md)
- [CFPaymentsEntityNetbankingPayment](docs/CFPaymentsEntityNetbankingPayment.md)
- [CFPaymentsEntityPaylater](docs/CFPaymentsEntityPaylater.md)
- [CFPaymentsEntityPaylaterPayment](docs/CFPaymentsEntityPaylaterPayment.md)
- [CFPaymentsEntityUPI](docs/CFPaymentsEntityUPI.md)
- [CFPaymentsEntityUPIPayment](docs/CFPaymentsEntityUPIPayment.md)
- [CFRefund](docs/CFRefund.md)
- [CFRefundRequest](docs/CFRefundRequest.md)
- [CFRefundURLObject](docs/CFRefundURLObject.md)
- [CFSavedInstrumentMeta](docs/CFSavedInstrumentMeta.md)
- [CFSettlementURLObject](docs/CFSettlementURLObject.md)
- [CFSettlementsEntity](docs/CFSettlementsEntity.md)
- [CFUPI](docs/CFUPI.md)
- [CFUPIAuthorizeDetails](docs/CFUPIAuthorizeDetails.md)
- [CFUPIPayment](docs/CFUPIPayment.md)
- [CFVendorSplit](docs/CFVendorSplit.md)
- [LinkCancelledError](docs/LinkCancelledError.md)
- [RefundSpeed](docs/RefundSpeed.md)

## Documentation For Authorization

All endpoints do not require authorization.

## Author

nextgenapi@cashfree.com
