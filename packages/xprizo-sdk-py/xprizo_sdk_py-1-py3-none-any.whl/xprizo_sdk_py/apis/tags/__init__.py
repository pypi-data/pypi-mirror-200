# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from xprizo_sdk_py.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    AGENT = "Agent"
    CATEGORY = "Category"
    CONTACT = "Contact"
    DOCUMENT = "Document"
    ISGPAY = "ISGPay"
    ITEM = "Item"
    MERCHANT = "Merchant"
    PREFERENCE = "Preference"
    PROFILE = "Profile"
    RELATIONSHIP = "Relationship"
    REPORT = "Report"
    SECURITY = "Security"
    SYSTEM = "System"
    TASK = "Task"
    TRANSACTION = "Transaction"
    WALLET = "Wallet"
