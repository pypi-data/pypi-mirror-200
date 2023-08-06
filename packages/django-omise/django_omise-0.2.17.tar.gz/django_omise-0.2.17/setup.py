# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_omise',
 'django_omise.admin',
 'django_omise.migrations',
 'django_omise.models',
 'django_omise.tests',
 'django_omise.tests.mockdata',
 'django_omise.utils']

package_data = \
{'': ['*'],
 'django_omise': ['locale/th/LC_MESSAGES/django.po',
                  'static/django_omise/css/*',
                  'static/django_omise/images/creditcardproviders/*',
                  'static/django_omise/js/*',
                  'templates/admin/django_omise/charge/*',
                  'templates/django_omise/*']}

install_requires = \
['omise>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'django-omise',
    'version': '0.2.17',
    'description': 'Django models for Omise',
    'long_description': '# django-omise Django + Omise\n\n![Test](https://github.com/jamesx00/django-omise/actions/workflows/tests.yml/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/jamesx00/django-omise/badge.svg?branch=master)](https://coveralls.io/github/jamesx00/django-omise?branch=master)\n[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/jamesx00/django-omise/issues)\n\nDjango models for Omise. Currently, we support the following features:\n\n- Creating a customer\n- Allowing customer to add/delete credit/debit cards\n- Collect payments with new card with the option to keep the card\n- Collect payments with saved cards\n- Collect payments with [Internet Banking](https://www.omise.co/internet-banking)\n- Collect payments with [TrueMoney Wallet](https://www.omise.co/truemoney-wallet)\n- Collect payments with [Promptpay](https://www.omise.co/promptpay)\n- Collect payments with [Rabbit LINE Pay](https://www.omise.co/rabbit-linepay)\n- Webhook handler, saving raw data as an Event object and update related objects, currently supporting\n\n  - Customer\n  - Card\n  - Charge\n  - Source\n  - Refund\n  - Schedule\n  - Scheduled Charge\n  - Schedule Occurrence\n\n- 3DS pending charges handling\n\nSee the [roadmap](#roadmap-and-contributions) for the plan of this project. Contributions are welcome!\n\n### Quick start\n\n---\n\n1. Add "django_omise" to your INSTALLED_APPS setting like this:\n\n```\n    INSTALLED_APPS = [\n        ...\n        "django_omise",\n    ]\n```\n\n2. Include the django_omise URLconf in your project urls.py like this:\n\n```\n    path("payments/", include("django_omise.urls")),\n```\n\n3. Add Omise keys and operating mode in settings.py:\n\n```python\nOMISE_PUBLIC_KEY = xxxx\nOMISE_SECRET_KEY = xxxx\nOMISE_LIVE_MODE = True | False\nOMISE_CHARGE_RETURN_HOST = localhost:8000\n\n# Optional. The default payment method is credit/debit card only.\n# You must specify additional payment methods.\nOMISE_PAYMENT_METHODS = [\n    "card",\n    "internet_banking", # Internet Banking\n    "truemoney_wallet", # TrueMoney Wallet\n    "promptpay", # Promptpay\n    "rabbit_linepay", # Rabbit LINE Pay\n]\n```\n\n4. Run `python manage.py migrate` to create the Omise models.\n\n5. Add Omise endpoint webhook url `https://www.your-own-domain.com/payments/webhook/`\n\n### Basic usage\n\n---\n\n1. Create an Omise customer from User:\n\n   ```python\n   from django.contrib.auth import get_user_model\n   from django_omise.models.core import Customer\n\n   User = get_user_model()\n   user = User.objects.first()\n   customer = Customer.get_or_create(user=user)\n   ```\n\n2. Add card to Customer\n\n   2.1 With the built-in view (Recommended)\n\n   We have built a basic card collecting view where logged in users can add and remove their cards. Run Django server and visit _/payments/payment_methods/_ to see it in action. You could override the template used in the view by creating a new template in your project\'s directory _/templates/django_omise/manage_payment_methods.html_.\n\n   2.2 Manually\n\n   ```python\n   from django_omise.models.core import Customer\n   from django_omise.omise import omise\n\n   omise_token = omise.Token.retrieve(token_id)\n   Customer.objects.live().first().add_card(token=omise_token)\n   ```\n\n3. Charge a customer (Currently supporting new/saved cards, [Internet Banking](https://www.omise.co/internet-banking), [TrueMoney Wallet](https://www.omise.co/truemoney-wallet), [Promptpay](https://www.omise.co/promptpay))\n\n   3.1 With the build-in mixin\n\n   This package comes with a built-in mixin, with which you can create a class-based-view and write a few methods to charge a customer. See below for an example or see [Example 1](./examples/):\n\n   ```python\n   from django.contrib.auth.mixins import LoginRequiredMixin\n   from django_omise.mixins import CheckoutMixin\n   from django_omise.models.choices import Currency\n\n   # Your own class-based-view\n   class CheckoutView(LoginRequiredMixin, CheckoutMixin):\n\n       template_name = "yourapp/template.html"\n       success_url = ...\n\n       def get_charge_details(self):\n           return {\n               "amount": 100000,\n               "currency": Currency.THB,\n           }\n\n       def process_charge_and_form(self, charge, form):\n           if charge.status in [ChargeStatus.SUCCESSFUL, ChargeStatus.PENDING]:\n               # Create new order and attach a charge object\n               # And handle form data\n               handle_form_data(form.cleaned_data)\n   ```\n\n   3.2 Manually\n\n   ```python\n   from django_omise.models.choices import Currency, ChargeStatus\n   from django_omise.models.core import Customer\n\n   customer = Customer.objects.first()\n   card = customer.cards.live().first()\n\n   charge = customer.charge_with_card(\n       amount=100000,\n       currency=Currency.THB,\n       card=card,\n   )\n\n   if charge.status == ChargeStatus.SUCCESSFUL:\n       # Do something\n   elif charge.status == ChargeStatus.FAILED:\n       # Do something else\n   ```\n\n4. Create a charge schedule for a customer:\n\nAt the moment, you can create a new schedule for a customer manually by calling the method create_schedule from a Custoemr object. See below for an example:\n\n```python\nimport datetime\nfrom django_omise.models.choices import Currency\nfrom django_omise.models.core import Customer\n\ncustomer = Customer.objects.first()\ncard = customer.default_card\n\ncustomer.create_schedule(\n    amount=100000,\n    currency=Currency.THB,\n    card=card,\n    every=1,\n    period="month",\n    start_date=datetime.date(year=2022, month=5, day=22),\n    end_date=datetime.date(year=2032, month=5, day=22),\n    on={\n        \'days_of_month\': [22],\n    },\n    description="Monthly subscription",\n)\n```\n\n### Roadmap and contributions\n\n---\n\nHere are our immediate plans for this package, and more will be added! All contributions are welcome. I am new to publishing a public package, so if you have any recommendations, please feel free to create an issue on this repository or feel free to send me an email at siwatjames@gmail.com.\n\nOmise Features\n\n- [x] Handle refunds API\n- Handle webhook events and update related objects\n- Create charge with Sources\n  - [x] Internet banking\n  - [x] TrueMoney Wallet\n  - [x] Promptpay\n  - [x] Rabbit LINE Pay\n  - [ ] Installment\n- Schedule\n  - [x] Scheduled Charges\n  - [ ] Scheduled Transfer\n\nOthers\n\n- Implement tests\n- Add documentations\n\n### Development\n\n---\n\nYou can run tests with either coverage or pytest.\n\nTo run with pytest\n\n```shell\npip install pytest-django\npython -m pytest [path_to_file] [--verbose -s --cov-report=html --cov=.]\n```\n\nTo run with coverage\n\n```shell\npip install coverage\ncoverage run run_tests.py\ncoverage report\ncoverage html\n```\n',
    'author': 'James Tansiri',
    'author_email': 'tansirijames@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jamesx00/django-omise',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
