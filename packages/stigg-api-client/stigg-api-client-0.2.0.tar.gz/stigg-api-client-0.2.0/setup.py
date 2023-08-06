# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stigg', 'stigg.generated']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.8.0,<23.0.0',
 'flake8>=5.0.4,<6.0.0',
 'graphql-core==3.1.6',
 'requests>=2.28.1,<3.0.0',
 'sgqlc>=16.0,<17.0']

setup_kwargs = {
    'name': 'stigg-api-client',
    'version': '0.2.0',
    'description': '',
    'long_description': '# stigg-api-client\n\nThis library provides a Python wrapper to [Stigg\'s GraphQL API](https://docs.stigg.io/docs/graphql-api) based on \nthe operations that are in use by the [Stigg\'s Node.js SDK](https://docs.stigg.io/docs/nodejs-sdk).\n\nIt leverages the [sgqlc](https://github.com/profusion/sgqlc) library to generate Python classes for GraphQL types, and\nutilizes the `sgqlc.endpoint.requests.RequestsEndpoint` class to send the API requests. The responses are being\nautomatically converted into native Python types.\n\n## Documentation\n\nSee https://docs.stigg.io/docs/python-sdk\n\n## Installation\n\n    pip install stigg-api-client\n\n## Usage\n\nInitialize the client:\n\n```python\n\nimport os\nfrom stigg import Stigg\n\napi_key = os.environ.get("STIGG_SERVER_API_KEY")\n\nstigg_client = Stigg.create_client(api_key)\n\n```\n\nProvision a customer\n\n```python\n\nimport os\nfrom stigg import Stigg\n\napi_key = os.environ.get("STIGG_SERVER_API_KEY")\n\nclient = Stigg.create_client(api_key)\n\ndata = client.request(Stigg.mutation.provision_customer, {\n    "input": {\n        "refId": "customer-id",\n        "name": "Acme",\n        "email": "hello@acme.com",\n        "couponRefId": "coupon-id",\n        "billingInformation": {\n            "language": "en",\n            "timezone": "America/New_York",\n            "billingAddress": {\n                "country": "US",\n                "city": "New York",\n                "state": "NY",\n                "addressLine1": "123 Main Street",\n                "addressLine2": "Apt. 1",\n                "phoneNumber": "+1 212-499-5321",\n                "postalCode": "10164"\n            },\n            "shippingAddress": {\n                "country": "US",\n                "city": "New York",\n                "state": "NY",\n                "addressLine1": "123 Main Street",\n                "addressLine2": "Apt. 1",\n                "phoneNumber": "+1 212-499-5321",\n                "postalCode": "10164"\n            }\n        },\n        "additionalMetaData": {\n            "key": "value"\n        },\n        "subscriptionParams": {\n            "planId": "plan-revvenu-basic"\n        }\n    }\n})\n\nprint(data.provision_customer.customer.name)\n\n```\n\nGet a customer by ID\n\n```python\n\nimport os\nfrom stigg import Stigg\n\napi_key = os.environ.get("STIGG_SERVER_API_KEY")\n\nclient = Stigg.create_client(api_key)\n\ndata = client.request(Stigg.query.get_customer_by_id, {\n  "input": {"customerId": "customer-id"}\n})\n\ncustomer = data.get_customer_by_ref_id\nprint(customer.name)\n\n```\n',
    'author': 'Stigg',
    'author_email': 'support@stigg.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
