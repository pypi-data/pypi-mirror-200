# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_pay']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'pydantic>=1.10.6,<2.0.0', 'pytz>=2022.7.1,<2023.0.0']

setup_kwargs = {
    'name': 'telegram-pay',
    'version': '0.1.1',
    'description': 'Wrapper for api.pay.4u.studio',
    'long_description': '# Install\n`pip install telegram-pay`\n\n# Use\n```python\nfrom telegram_pay import TelegramPay\n\nasync def main():\n    \n    client = TelegramPay(shop_id=SHOP_ID, shop_token=SHOP_TOKEN)\n    subscription = await client.get_user_subscription(USER_ID, SUBSCRIPTION_ID)\n\n    if subscription.valid:\n        # User is subscribed\n    else:\n        # User is not subscribed\n```',
    'author': 'Snimshchikov Ilya',
    'author_email': 'snimshchikov.ilya@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
