from enum import Enum

class TransactionStatus(str, Enum):
    AWAITING_AUTHENTICATION = 'AwaitingAuthentication'
    AUTHORIZED = 'Authorized'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    DECLINED = 'Declined'


class SubscriptionStatus(str, Enum):
    ACTIVE = 'Active'
    PAST_DUE = 'PastDue'
    CANCELLED = 'Cancelled'
    REJECTED = 'Rejected'
    EXPIRED = 'Expired'


class Currency(str, Enum):
    RUB = 'RUB' # Российский рубль 	
    EUR = 'EUR' # Евро 	              
    USD = 'USD' # Доллар США 	       
    GBP = 'GBP' # Фунт стерлингов 	
    UAH = 'UAH' # Украинская гривна 	
    BYN = 'BYN' # Белорусский рубль 	
    KZT = 'KZT' # Казахский тенге 	
    AZN = 'AZN' # Азербайджанский манат
    CHF = 'CHF' # Швейцарский франк 	
    CZK = 'CZK' # Чешская крона 	
    CAD = 'CAD' # Канадский доллар 	
    PLN = 'PLN' # Польский злотый 	
    SEK = 'SEK' # Шведская крона 	
    TRY = 'TRY' # Турецкая лира 	
    CNY = 'CNY' # Китайский юань 	
    INR = 'INR' # Индийская рупия 	
    BRL = 'BRL' # Бразильский реал 	
    ZAR = 'ZAR' # Южноафриканский рэнд 
    UZS = 'UZS' # Узбекский сум 	
    BGN = 'BGN' # Болгарский лев 	
    RON = 'RON' # Румынский лей 	
    AUD = 'AUD' # Австралийский доллар 
    HKD = 'HKD' # Гонконгский доллар 	
    GEL = 'GEL' # Грузинский лари 	
    KGS = 'KGS' # Киргизский сом 	
    AMD = 'AMD' # Армянский драм 	
    AED = 'AED' # Дирхам ОАЭ 	       


class Interval(str, Enum):
    Day = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'