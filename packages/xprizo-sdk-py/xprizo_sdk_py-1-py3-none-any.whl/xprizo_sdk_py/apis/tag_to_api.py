import typing_extensions

from xprizo_sdk_py.apis.tags import TagValues
from xprizo_sdk_py.apis.tags.agent_api import AgentApi
from xprizo_sdk_py.apis.tags.category_api import CategoryApi
from xprizo_sdk_py.apis.tags.contact_api import ContactApi
from xprizo_sdk_py.apis.tags.document_api import DocumentApi
from xprizo_sdk_py.apis.tags.isg_pay_api import ISGPayApi
from xprizo_sdk_py.apis.tags.item_api import ItemApi
from xprizo_sdk_py.apis.tags.merchant_api import MerchantApi
from xprizo_sdk_py.apis.tags.preference_api import PreferenceApi
from xprizo_sdk_py.apis.tags.profile_api import ProfileApi
from xprizo_sdk_py.apis.tags.relationship_api import RelationshipApi
from xprizo_sdk_py.apis.tags.report_api import ReportApi
from xprizo_sdk_py.apis.tags.security_api import SecurityApi
from xprizo_sdk_py.apis.tags.system_api import SystemApi
from xprizo_sdk_py.apis.tags.task_api import TaskApi
from xprizo_sdk_py.apis.tags.transaction_api import TransactionApi
from xprizo_sdk_py.apis.tags.wallet_api import WalletApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.AGENT: AgentApi,
        TagValues.CATEGORY: CategoryApi,
        TagValues.CONTACT: ContactApi,
        TagValues.DOCUMENT: DocumentApi,
        TagValues.ISGPAY: ISGPayApi,
        TagValues.ITEM: ItemApi,
        TagValues.MERCHANT: MerchantApi,
        TagValues.PREFERENCE: PreferenceApi,
        TagValues.PROFILE: ProfileApi,
        TagValues.RELATIONSHIP: RelationshipApi,
        TagValues.REPORT: ReportApi,
        TagValues.SECURITY: SecurityApi,
        TagValues.SYSTEM: SystemApi,
        TagValues.TASK: TaskApi,
        TagValues.TRANSACTION: TransactionApi,
        TagValues.WALLET: WalletApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.AGENT: AgentApi,
        TagValues.CATEGORY: CategoryApi,
        TagValues.CONTACT: ContactApi,
        TagValues.DOCUMENT: DocumentApi,
        TagValues.ISGPAY: ISGPayApi,
        TagValues.ITEM: ItemApi,
        TagValues.MERCHANT: MerchantApi,
        TagValues.PREFERENCE: PreferenceApi,
        TagValues.PROFILE: ProfileApi,
        TagValues.RELATIONSHIP: RelationshipApi,
        TagValues.REPORT: ReportApi,
        TagValues.SECURITY: SecurityApi,
        TagValues.SYSTEM: SystemApi,
        TagValues.TASK: TaskApi,
        TagValues.TRANSACTION: TransactionApi,
        TagValues.WALLET: WalletApi,
    }
)
