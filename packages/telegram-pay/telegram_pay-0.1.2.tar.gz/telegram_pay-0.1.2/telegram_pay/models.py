from __future__ import annotations
from typing import Optional
from decimal import Decimal
from datetime import datetime
import pytz
    
import aiohttp
from pydantic import BaseModel

from .enums import Currency, Interval, SubscriptionStatus, TransactionStatus

class TelegramPay():
    url = 'https://api.pay.4u.studio/'
    shop_id: str
    shop_token: str

    def __init__(self, shop_id: str, shop_token: str):
        self.shop_id = shop_id
        self.shop_token = shop_token

    @classmethod
    async def make_request(cls, endpoint: str, params: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.url + endpoint, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def make_request_auth(self, endpoint: str, params: dict = None) -> dict:
        headers = {'X-API-Key': self.shop_token}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + endpoint, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
            
    @classmethod
    async def get_subscription(cls, subscription_id: str):
        endpoint = f"subscriptions/predefined/{subscription_id}"
        subscription_json = await cls.make_request(endpoint)

        return SubscriptionDescription(**subscription_json)

    async def get_user_subscription(self, user_id: int, subscription_id: str) -> Subscription:
        endpoint = "subscriptions/search"
        params = {
            "user_id": user_id,
            "subscription_id": subscription_id
        }
        subscription_json = await self.make_request_auth(endpoint, params)

        if len(subscription_json) > 0:
            subscription_json[0]["exists"] = True
            subscription_json[0]["client"] = self
            return Subscription(**(subscription_json[0]))
        
        return Subscription(client=self, subscription_id=subscription_id, exists=False, user_id=user_id)

    async def cancel_subscription(self, subscription_unique_id: str):
        endpoint = f"subscriptions/{subscription_unique_id}/cancel"
        return await self.make_request(endpoint)

class Subscription(BaseModel):
    client: TelegramPay
    subscription_id: str
    exists: bool
    test_mode: Optional[bool]
    user_id: int
    unique_id: Optional[str]
    valid_until: Optional[datetime]
    amount: Optional[Decimal]
    currency: Optional[Currency]
    interval: Optional[Interval]
    status: Optional[SubscriptionStatus]
    description: Optional[str]
    start_date: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    @property
    def valid(self) -> bool:
        return self.exists and datetime.now(tz=pytz.UTC) < self.valid_until
    
    @property
    def expired(self) -> bool:
        return self.exists and self.status in [SubscriptionStatus.REJECTED,
                                               SubscriptionStatus.PAST_DUE,
                                               SubscriptionStatus.EXPIRED]
    
    @property
    def canceled(self) -> bool:
        return self.exists and self.status == SubscriptionStatus.CANCELLED
    
    @property
    def cancellable(self):
        return self.exists and self.status in [SubscriptionStatus.ACTIVE, 
                                               SubscriptionStatus.PAST_DUE]
    
    async def cancel(self):
        if self.cancellable:
            await self.client.cancel_subscription(self.unique_id)

class SubscriptionDescription(BaseModel):
    id: str
    shop_id: str
    description: str
    start_amount: Decimal
    start_currency: Currency
    start_period: int
    start_interval: Interval
    amount: Decimal
    currency: Currency
    period: int
    interval: Interval
    max_periods: Optional[int]
    email: bool
    require_confirmation: bool