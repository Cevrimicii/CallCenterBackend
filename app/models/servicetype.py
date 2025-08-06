from enum import Enum

class ServiceType(str, Enum):
    MOBILE = "mobile"
    HOME_INTERNET = "home_internet"
    BUSINESS_INTERNET = "business_internet"
