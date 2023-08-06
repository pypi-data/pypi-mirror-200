# Install
`pip install telegram-pay`

# Use
```python
from telegram_pay import TelegramPay

async def main():
    
    client = TelegramPay(shop_id=SHOP_ID, shop_token=SHOP_TOKEN)
    subscription = await client.get_user_subscription(USER_ID, SUBSCRIPTION_ID)

    if subscription.valid:
        # User is subscribed
    else:
        # User is not subscribed
```