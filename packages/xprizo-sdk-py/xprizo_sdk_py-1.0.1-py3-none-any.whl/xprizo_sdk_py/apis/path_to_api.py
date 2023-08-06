import typing_extensions

from xprizo_sdk_py.paths import PathValues
from xprizo_sdk_py.apis.paths.api_agent_sub_agent_list import ApiAgentSubAgentList
from xprizo_sdk_py.apis.paths.api_agent_locations import ApiAgentLocations
from xprizo_sdk_py.apis.paths.api_agent_wallet_account_id import ApiAgentWalletAccountId
from xprizo_sdk_py.apis.paths.api_agent_transactions_account_id import ApiAgentTransactionsAccountId
from xprizo_sdk_py.apis.paths.api_agent_trade_limit_request import ApiAgentTradeLimitRequest
from xprizo_sdk_py.apis.paths.api_agent_cash_request import ApiAgentCashRequest
from xprizo_sdk_py.apis.paths.api_agent_add_sub_agent_request import ApiAgentAddSubAgentRequest
from xprizo_sdk_py.apis.paths.api_agent_agent_send_payment import ApiAgentAgentSendPayment
from xprizo_sdk_py.apis.paths.api_agent_agent_request_payment import ApiAgentAgentRequestPayment
from xprizo_sdk_py.apis.paths.api_agent_reference_request import ApiAgentReferenceRequest
from xprizo_sdk_py.apis.paths.api_agent_reference_endorse import ApiAgentReferenceEndorse
from xprizo_sdk_py.apis.paths.api_agent_sub_agent_approved import ApiAgentSubAgentApproved
from xprizo_sdk_py.apis.paths.api_agent_set_wallet_access import ApiAgentSetWalletAccess
from xprizo_sdk_py.apis.paths.api_agent_set_sub_agent_commission import ApiAgentSetSubAgentCommission
from xprizo_sdk_py.apis.paths.api_agent_delete_sub_agent import ApiAgentDeleteSubAgent
from xprizo_sdk_py.apis.paths.api_category_get_model import ApiCategoryGetModel
from xprizo_sdk_py.apis.paths.api_category_list import ApiCategoryList
from xprizo_sdk_py.apis.paths.api_category_list_all import ApiCategoryListAll
from xprizo_sdk_py.apis.paths.api_category_set_name import ApiCategorySetName
from xprizo_sdk_py.apis.paths.api_category_set_description import ApiCategorySetDescription
from xprizo_sdk_py.apis.paths.api_category_set_public import ApiCategorySetPublic
from xprizo_sdk_py.apis.paths.api_category_set_data_hash_id import ApiCategorySetDataHashId
from xprizo_sdk_py.apis.paths.api_category_set_pdf_attachment import ApiCategorySetPdfAttachment
from xprizo_sdk_py.apis.paths.api_category_add_item import ApiCategoryAddItem
from xprizo_sdk_py.apis.paths.api_category_delete_hash_id import ApiCategoryDeleteHashId
from xprizo_sdk_py.apis.paths.api_category_get_properties import ApiCategoryGetProperties
from xprizo_sdk_py.apis.paths.api_category_update_property import ApiCategoryUpdateProperty
from xprizo_sdk_py.apis.paths.api_category_add_property import ApiCategoryAddProperty
from xprizo_sdk_py.apis.paths.api_category_delete_property_hash_id import ApiCategoryDeletePropertyHashId
from xprizo_sdk_py.apis.paths.api_contact_search import ApiContactSearch
from xprizo_sdk_py.apis.paths.api_contact_get_id import ApiContactGetId
from xprizo_sdk_py.apis.paths.api_contact_get_business_hash_id import ApiContactGetBusinessHashId
from xprizo_sdk_py.apis.paths.api_contact_name_id import ApiContactNameId
from xprizo_sdk_py.apis.paths.api_contact_tax_country_code import ApiContactTaxCountryCode
from xprizo_sdk_py.apis.paths.api_contact_banks import ApiContactBanks
from xprizo_sdk_py.apis.paths.api_contact_update import ApiContactUpdate
from xprizo_sdk_py.apis.paths.api_contact_updat_business import ApiContactUpdatBusiness
from xprizo_sdk_py.apis.paths.api_contact_set_mobile import ApiContactSetMobile
from xprizo_sdk_py.apis.paths.api_contact_set_email import ApiContactSetEmail
from xprizo_sdk_py.apis.paths.api_contact_set_tax_country_code import ApiContactSetTaxCountryCode
from xprizo_sdk_py.apis.paths.api_contact_tasks_id import ApiContactTasksId
from xprizo_sdk_py.apis.paths.api_contact_messages import ApiContactMessages
from xprizo_sdk_py.apis.paths.api_contact_messages_unread_count import ApiContactMessagesUnreadCount
from xprizo_sdk_py.apis.paths.api_contact_messages_set_read import ApiContactMessagesSetRead
from xprizo_sdk_py.apis.paths.api_contact_send_message import ApiContactSendMessage
from xprizo_sdk_py.apis.paths.api_contact_add_ticket import ApiContactAddTicket
from xprizo_sdk_py.apis.paths.api_document_types import ApiDocumentTypes
from xprizo_sdk_py.apis.paths.api_document_list_contact_id import ApiDocumentListContactId
from xprizo_sdk_py.apis.paths.api_document_add_contact_id import ApiDocumentAddContactId
from xprizo_sdk_py.apis.paths.api_document_delete_id import ApiDocumentDeleteId
from xprizo_sdk_py.apis.paths.api_isg_pay_card_deposit import ApiISGPayCardDeposit
from xprizo_sdk_py.apis.paths.api_isg_pay_card_deposit_response import ApiISGPayCardDepositResponse
from xprizo_sdk_py.apis.paths.api_isg_pay_request_payment import ApiISGPayRequestPayment
from xprizo_sdk_py.apis.paths.api_isg_pay_request_payment_response import ApiISGPayRequestPaymentResponse
from xprizo_sdk_py.apis.paths.api_isg_pay_send import ApiISGPaySend
from xprizo_sdk_py.apis.paths.api_isg_pay_send_response import ApiISGPaySendResponse
from xprizo_sdk_py.apis.paths.api_isg_pay_check_status import ApiISGPayCheckStatus
from xprizo_sdk_py.apis.paths.api_item_model import ApiItemModel
from xprizo_sdk_py.apis.paths.api_item_list import ApiItemList
from xprizo_sdk_py.apis.paths.api_item_merge_template import ApiItemMergeTemplate
from xprizo_sdk_py.apis.paths.api_item_transaction_report_transaction_id import ApiItemTransactionReportTransactionId
from xprizo_sdk_py.apis.paths.api_item_set_image import ApiItemSetImage
from xprizo_sdk_py.apis.paths.api_item_set_amount import ApiItemSetAmount
from xprizo_sdk_py.apis.paths.api_item_set_property import ApiItemSetProperty
from xprizo_sdk_py.apis.paths.api_item_set_property_image import ApiItemSetPropertyImage
from xprizo_sdk_py.apis.paths.api_item_set_name import ApiItemSetName
from xprizo_sdk_py.apis.paths.api_item_set_description import ApiItemSetDescription
from xprizo_sdk_py.apis.paths.api_item_set_detail import ApiItemSetDetail
from xprizo_sdk_py.apis.paths.api_item_add import ApiItemAdd
from xprizo_sdk_py.apis.paths.api_item_deletehash_id import ApiItemDeletehashId
from xprizo_sdk_py.apis.paths.api_item_subscriptions import ApiItemSubscriptions
from xprizo_sdk_py.apis.paths.api_item_subscribe_hash_id import ApiItemSubscribeHashId
from xprizo_sdk_py.apis.paths.api_item_unsubscribe_hash_id import ApiItemUnsubscribeHashId
from xprizo_sdk_py.apis.paths.api_item_pin_subscription import ApiItemPinSubscription
from xprizo_sdk_py.apis.paths.api_item_unpin_subscription import ApiItemUnpinSubscription
from xprizo_sdk_py.apis.paths.api_merchant_request_payment import ApiMerchantRequestPayment
from xprizo_sdk_py.apis.paths.api_merchant_add import ApiMerchantAdd
from xprizo_sdk_py.apis.paths.api_merchant_get_data import ApiMerchantGetData
from xprizo_sdk_py.apis.paths.api_preference import ApiPreference
from xprizo_sdk_py.apis.paths.api_preference_profile_picture import ApiPreferenceProfilePicture
from xprizo_sdk_py.apis.paths.api_preference_notification_count import ApiPreferenceNotificationCount
from xprizo_sdk_py.apis.paths.api_preference_set_allow_marketing_emails import ApiPreferenceSetAllowMarketingEmails
from xprizo_sdk_py.apis.paths.api_preference_set_visible_by_user_name import ApiPreferenceSetVisibleByUserName
from xprizo_sdk_py.apis.paths.api_preference_set_visible_by_email import ApiPreferenceSetVisibleByEmail
from xprizo_sdk_py.apis.paths.api_preference_set_visible_by_phone import ApiPreferenceSetVisibleByPhone
from xprizo_sdk_py.apis.paths.api_preference_set_location_visible import ApiPreferenceSetLocationVisible
from xprizo_sdk_py.apis.paths.api_preference_set_find_option import ApiPreferenceSetFindOption
from xprizo_sdk_py.apis.paths.api_preference_set_notify_on_new_approval import ApiPreferenceSetNotifyOnNewApproval
from xprizo_sdk_py.apis.paths.api_preference_set_notify_on_new_transaction import ApiPreferenceSetNotifyOnNewTransaction
from xprizo_sdk_py.apis.paths.api_preference_set_notify_via_email import ApiPreferenceSetNotifyViaEmail
from xprizo_sdk_py.apis.paths.api_preference_set_lat_lng import ApiPreferenceSetLatLng
from xprizo_sdk_py.apis.paths.api_preference_set_language import ApiPreferenceSetLanguage
from xprizo_sdk_py.apis.paths.api_preference_set_pay_fees_from_savings import ApiPreferenceSetPayFeesFromSavings
from xprizo_sdk_py.apis.paths.api_preference_set_default_otp_type import ApiPreferenceSetDefaultOTPType
from xprizo_sdk_py.apis.paths.api_preference_set_profile_picture import ApiPreferenceSetProfilePicture
from xprizo_sdk_py.apis.paths.api_preference_set_notification_push_token import ApiPreferenceSetNotificationPushToken
from xprizo_sdk_py.apis.paths.api_preference_set_approval_webhook import ApiPreferenceSetApprovalWebhook
from xprizo_sdk_py.apis.paths.api_preference_set_payment_webhook import ApiPreferenceSetPaymentWebhook
from xprizo_sdk_py.apis.paths.api_preference_set_request_payment_webhook import ApiPreferenceSetRequestPaymentWebhook
from xprizo_sdk_py.apis.paths.api_preference_notification_count_clear import ApiPreferenceNotificationCountClear
from xprizo_sdk_py.apis.paths.api_profile_get import ApiProfileGet
from xprizo_sdk_py.apis.paths.api_profile_get_full import ApiProfileGetFull
from xprizo_sdk_py.apis.paths.api_profile_log import ApiProfileLog
from xprizo_sdk_py.apis.paths.api_profile_set_user_name import ApiProfileSetUserName
from xprizo_sdk_py.apis.paths.api_profile_set_password import ApiProfileSetPassword
from xprizo_sdk_py.apis.paths.api_profile_set_pin import ApiProfileSetPin
from xprizo_sdk_py.apis.paths.api_profile_clear_pin import ApiProfileClearPin
from xprizo_sdk_py.apis.paths.api_profile_unlock import ApiProfileUnlock
from xprizo_sdk_py.apis.paths.api_profile_lock import ApiProfileLock
from xprizo_sdk_py.apis.paths.api_relationship_list import ApiRelationshipList
from xprizo_sdk_py.apis.paths.api_relationship_get_model import ApiRelationshipGetModel
from xprizo_sdk_py.apis.paths.api_relationship_default_wallet import ApiRelationshipDefaultWallet
from xprizo_sdk_py.apis.paths.api_relationship_default_wallets import ApiRelationshipDefaultWallets
from xprizo_sdk_py.apis.paths.api_relationship_wallets import ApiRelationshipWallets
from xprizo_sdk_py.apis.paths.api_relationship_linked_wallets import ApiRelationshipLinkedWallets
from xprizo_sdk_py.apis.paths.api_relationship_get_wallet_access import ApiRelationshipGetWalletAccess
from xprizo_sdk_py.apis.paths.api_relationship_transactions import ApiRelationshipTransactions
from xprizo_sdk_py.apis.paths.api_relationship_add import ApiRelationshipAdd
from xprizo_sdk_py.apis.paths.api_relationship_set_status_active import ApiRelationshipSetStatusActive
from xprizo_sdk_py.apis.paths.api_relationship_set_status_hidden import ApiRelationshipSetStatusHidden
from xprizo_sdk_py.apis.paths.api_relationship_set_status_blocked import ApiRelationshipSetStatusBlocked
from xprizo_sdk_py.apis.paths.api_relationship_set_access import ApiRelationshipSetAccess
from xprizo_sdk_py.apis.paths.api_report_get import ApiReportGet
from xprizo_sdk_py.apis.paths.api_report_save import ApiReportSave
from xprizo_sdk_py.apis.paths.api_security_get_token import ApiSecurityGetToken
from xprizo_sdk_py.apis.paths.api_security_firebase_login import ApiSecurityFirebaseLogin
from xprizo_sdk_py.apis.paths.api_security_google_login import ApiSecurityGoogleLogin
from xprizo_sdk_py.apis.paths.api_security_apple_login import ApiSecurityAppleLogin
from xprizo_sdk_py.apis.paths.api_security_logout import ApiSecurityLogout
from xprizo_sdk_py.apis.paths.api_security_register import ApiSecurityRegister
from xprizo_sdk_py.apis.paths.api_security_validate_user import ApiSecurityValidateUser
from xprizo_sdk_py.apis.paths.api_security_send_otp_to_email import ApiSecuritySendOtpToEmail
from xprizo_sdk_py.apis.paths.api_security_send_otp_to_sms import ApiSecuritySendOtpToSMS
from xprizo_sdk_py.apis.paths.api_security_check_otp import ApiSecurityCheckOtp
from xprizo_sdk_py.apis.paths.api_security_send_otp import ApiSecuritySendOtp
from xprizo_sdk_py.apis.paths.api_security_send_new_otp import ApiSecuritySendNewOtp
from xprizo_sdk_py.apis.paths.api_security_get_captcha import ApiSecurityGetCaptcha
from xprizo_sdk_py.apis.paths.api_security_activate_account import ApiSecurityActivateAccount
from xprizo_sdk_py.apis.paths.api_security_get_reset_key import ApiSecurityGetResetKey
from xprizo_sdk_py.apis.paths.api_security_reset_password import ApiSecurityResetPassword
from xprizo_sdk_py.apis.paths.api_system_info import ApiSystemInfo
from xprizo_sdk_py.apis.paths.api_system_merchants import ApiSystemMerchants
from xprizo_sdk_py.apis.paths.api_system_country_list import ApiSystemCountryList
from xprizo_sdk_py.apis.paths.api_system_currencies import ApiSystemCurrencies
from xprizo_sdk_py.apis.paths.api_system_banks import ApiSystemBanks
from xprizo_sdk_py.apis.paths.api_system_bank_count import ApiSystemBankCount
from xprizo_sdk_py.apis.paths.api_system_bank import ApiSystemBank
from xprizo_sdk_py.apis.paths.api_task_get_id import ApiTaskGetId
from xprizo_sdk_py.apis.paths.api_task_add_comment_id import ApiTaskAddCommentId
from xprizo_sdk_py.apis.paths.api_task_add_attachment_id import ApiTaskAddAttachmentId
from xprizo_sdk_py.apis.paths.api_task_hide_id import ApiTaskHideId
from xprizo_sdk_py.apis.paths.api_task_show_id import ApiTaskShowId
from xprizo_sdk_py.apis.paths.api_task_cancel_id import ApiTaskCancelId
from xprizo_sdk_py.apis.paths.api_task_one_off_withdrawal_amount_request_account_id import ApiTaskOneOffWithdrawalAmountRequestAccountId
from xprizo_sdk_py.apis.paths.api_task_daily_withdrawal_limit_request_account_id import ApiTaskDailyWithdrawalLimitRequestAccountId
from xprizo_sdk_py.apis.paths.api_transaction_status_by_reference_account_id import ApiTransactionStatusByReferenceAccountId
from xprizo_sdk_py.apis.paths.api_transaction_instant_payment_qr_code import ApiTransactionInstantPaymentQRCode
from xprizo_sdk_py.apis.paths.api_transaction_approval_cancel import ApiTransactionApprovalCancel
from xprizo_sdk_py.apis.paths.api_transaction_approval_accept import ApiTransactionApprovalAccept
from xprizo_sdk_py.apis.paths.api_transaction_approval_reject import ApiTransactionApprovalReject
from xprizo_sdk_py.apis.paths.api_transaction_send_payment import ApiTransactionSendPayment
from xprizo_sdk_py.apis.paths.api_transaction_request_payment import ApiTransactionRequestPayment
from xprizo_sdk_py.apis.paths.api_transaction_wallet_exchange import ApiTransactionWalletExchange
from xprizo_sdk_py.apis.paths.api_transaction_bank_deposit import ApiTransactionBankDeposit
from xprizo_sdk_py.apis.paths.api_transaction_agent_deposit import ApiTransactionAgentDeposit
from xprizo_sdk_py.apis.paths.api_transaction_agent_withdrawal import ApiTransactionAgentWithdrawal
from xprizo_sdk_py.apis.paths.api_transaction_savings_deposit import ApiTransactionSavingsDeposit
from xprizo_sdk_py.apis.paths.api_transaction_savings_withdrawal import ApiTransactionSavingsWithdrawal
from xprizo_sdk_py.apis.paths.api_wallet_list import ApiWalletList
from xprizo_sdk_py.apis.paths.api_wallet_savings_list import ApiWalletSavingsList
from xprizo_sdk_py.apis.paths.api_wallet_account_id import ApiWalletAccountId
from xprizo_sdk_py.apis.paths.api_wallet_info import ApiWalletInfo
from xprizo_sdk_py.apis.paths.api_wallet_info_list import ApiWalletInfoList
from xprizo_sdk_py.apis.paths.api_wallet_owner import ApiWalletOwner
from xprizo_sdk_py.apis.paths.api_wallet_options import ApiWalletOptions
from xprizo_sdk_py.apis.paths.api_wallet_transactions_account_id import ApiWalletTransactionsAccountId
from xprizo_sdk_py.apis.paths.api_wallet_transaction_transaction_id import ApiWalletTransactionTransactionId
from xprizo_sdk_py.apis.paths.api_wallet_transaction_by_reference_account_id import ApiWalletTransactionByReferenceAccountId
from xprizo_sdk_py.apis.paths.api_wallet_transaction_summary import ApiWalletTransactionSummary
from xprizo_sdk_py.apis.paths.api_wallet_monthly_balances import ApiWalletMonthlyBalances
from xprizo_sdk_py.apis.paths.api_wallet_total_withdrawals import ApiWalletTotalWithdrawals
from xprizo_sdk_py.apis.paths.api_wallet_add import ApiWalletAdd
from xprizo_sdk_py.apis.paths.api_wallet_set_default_account_id import ApiWalletSetDefaultAccountId
from xprizo_sdk_py.apis.paths.api_wallet_clear_new_transaction_count_account_id import ApiWalletClearNewTransactionCountAccountId
from xprizo_sdk_py.apis.paths.api_wallet_statement_report_account_id import ApiWalletStatementReportAccountId
from xprizo_sdk_py.apis.paths.api_wallet_transaction_report_transaction_id import ApiWalletTransactionReportTransactionId
from xprizo_sdk_py.apis.paths.api_wallet_id import ApiWalletId
from xprizo_sdk_py.apis.paths.api_wallet_approval_status import ApiWalletApprovalStatus

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_AGENT_SUB_AGENT_LIST: ApiAgentSubAgentList,
        PathValues.API_AGENT_LOCATIONS: ApiAgentLocations,
        PathValues.API_AGENT_WALLET_ACCOUNT_ID: ApiAgentWalletAccountId,
        PathValues.API_AGENT_TRANSACTIONS_ACCOUNT_ID: ApiAgentTransactionsAccountId,
        PathValues.API_AGENT_TRADE_LIMIT_REQUEST: ApiAgentTradeLimitRequest,
        PathValues.API_AGENT_CASH_REQUEST: ApiAgentCashRequest,
        PathValues.API_AGENT_ADD_SUB_AGENT_REQUEST: ApiAgentAddSubAgentRequest,
        PathValues.API_AGENT_AGENT_SEND_PAYMENT: ApiAgentAgentSendPayment,
        PathValues.API_AGENT_AGENT_REQUEST_PAYMENT: ApiAgentAgentRequestPayment,
        PathValues.API_AGENT_REFERENCE_REQUEST: ApiAgentReferenceRequest,
        PathValues.API_AGENT_REFERENCE_ENDORSE: ApiAgentReferenceEndorse,
        PathValues.API_AGENT_SUB_AGENT_APPROVED: ApiAgentSubAgentApproved,
        PathValues.API_AGENT_SET_WALLET_ACCESS: ApiAgentSetWalletAccess,
        PathValues.API_AGENT_SET_SUB_AGENT_COMMISSION: ApiAgentSetSubAgentCommission,
        PathValues.API_AGENT_DELETE_SUB_AGENT: ApiAgentDeleteSubAgent,
        PathValues.API_CATEGORY_GET_MODEL: ApiCategoryGetModel,
        PathValues.API_CATEGORY_LIST: ApiCategoryList,
        PathValues.API_CATEGORY_LIST_ALL: ApiCategoryListAll,
        PathValues.API_CATEGORY_SET_NAME: ApiCategorySetName,
        PathValues.API_CATEGORY_SET_DESCRIPTION: ApiCategorySetDescription,
        PathValues.API_CATEGORY_SET_PUBLIC: ApiCategorySetPublic,
        PathValues.API_CATEGORY_SET_DATA_HASH_ID: ApiCategorySetDataHashId,
        PathValues.API_CATEGORY_SET_PDF_ATTACHMENT: ApiCategorySetPdfAttachment,
        PathValues.API_CATEGORY_ADD_ITEM: ApiCategoryAddItem,
        PathValues.API_CATEGORY_DELETE_HASH_ID: ApiCategoryDeleteHashId,
        PathValues.API_CATEGORY_GET_PROPERTIES: ApiCategoryGetProperties,
        PathValues.API_CATEGORY_UPDATE_PROPERTY: ApiCategoryUpdateProperty,
        PathValues.API_CATEGORY_ADD_PROPERTY: ApiCategoryAddProperty,
        PathValues.API_CATEGORY_DELETE_PROPERTY_HASH_ID: ApiCategoryDeletePropertyHashId,
        PathValues.API_CONTACT_SEARCH: ApiContactSearch,
        PathValues.API_CONTACT_GET_ID: ApiContactGetId,
        PathValues.API_CONTACT_GET_BUSINESS_HASH_ID: ApiContactGetBusinessHashId,
        PathValues.API_CONTACT_NAME_ID: ApiContactNameId,
        PathValues.API_CONTACT_TAX_COUNTRY_CODE: ApiContactTaxCountryCode,
        PathValues.API_CONTACT_BANKS: ApiContactBanks,
        PathValues.API_CONTACT_UPDATE: ApiContactUpdate,
        PathValues.API_CONTACT_UPDAT_BUSINESS: ApiContactUpdatBusiness,
        PathValues.API_CONTACT_SET_MOBILE: ApiContactSetMobile,
        PathValues.API_CONTACT_SET_EMAIL: ApiContactSetEmail,
        PathValues.API_CONTACT_SET_TAX_COUNTRY_CODE: ApiContactSetTaxCountryCode,
        PathValues.API_CONTACT_TASKS_ID: ApiContactTasksId,
        PathValues.API_CONTACT_MESSAGES: ApiContactMessages,
        PathValues.API_CONTACT_MESSAGES_UNREAD_COUNT: ApiContactMessagesUnreadCount,
        PathValues.API_CONTACT_MESSAGES_SET_READ: ApiContactMessagesSetRead,
        PathValues.API_CONTACT_SEND_MESSAGE: ApiContactSendMessage,
        PathValues.API_CONTACT_ADD_TICKET: ApiContactAddTicket,
        PathValues.API_DOCUMENT_TYPES: ApiDocumentTypes,
        PathValues.API_DOCUMENT_LIST_CONTACT_ID: ApiDocumentListContactId,
        PathValues.API_DOCUMENT_ADD_CONTACT_ID: ApiDocumentAddContactId,
        PathValues.API_DOCUMENT_DELETE_ID: ApiDocumentDeleteId,
        PathValues.API_ISGPAY_CARD_DEPOSIT: ApiISGPayCardDeposit,
        PathValues.API_ISGPAY_CARD_DEPOSIT_RESPONSE: ApiISGPayCardDepositResponse,
        PathValues.API_ISGPAY_REQUEST_PAYMENT: ApiISGPayRequestPayment,
        PathValues.API_ISGPAY_REQUEST_PAYMENT_RESPONSE: ApiISGPayRequestPaymentResponse,
        PathValues.API_ISGPAY_SEND: ApiISGPaySend,
        PathValues.API_ISGPAY_SEND_RESPONSE: ApiISGPaySendResponse,
        PathValues.API_ISGPAY_CHECK_STATUS: ApiISGPayCheckStatus,
        PathValues.API_ITEM_MODEL: ApiItemModel,
        PathValues.API_ITEM_LIST: ApiItemList,
        PathValues.API_ITEM_MERGE_TEMPLATE: ApiItemMergeTemplate,
        PathValues.API_ITEM_TRANSACTION_REPORT_TRANSACTION_ID: ApiItemTransactionReportTransactionId,
        PathValues.API_ITEM_SET_IMAGE: ApiItemSetImage,
        PathValues.API_ITEM_SET_AMOUNT: ApiItemSetAmount,
        PathValues.API_ITEM_SET_PROPERTY: ApiItemSetProperty,
        PathValues.API_ITEM_SET_PROPERTY_IMAGE: ApiItemSetPropertyImage,
        PathValues.API_ITEM_SET_NAME: ApiItemSetName,
        PathValues.API_ITEM_SET_DESCRIPTION: ApiItemSetDescription,
        PathValues.API_ITEM_SET_DETAIL: ApiItemSetDetail,
        PathValues.API_ITEM_ADD: ApiItemAdd,
        PathValues.API_ITEM_DELETEHASH_ID: ApiItemDeletehashId,
        PathValues.API_ITEM_SUBSCRIPTIONS: ApiItemSubscriptions,
        PathValues.API_ITEM_SUBSCRIBE_HASH_ID: ApiItemSubscribeHashId,
        PathValues.API_ITEM_UNSUBSCRIBE_HASH_ID: ApiItemUnsubscribeHashId,
        PathValues.API_ITEM_PIN_SUBSCRIPTION: ApiItemPinSubscription,
        PathValues.API_ITEM_UNPIN_SUBSCRIPTION: ApiItemUnpinSubscription,
        PathValues.API_MERCHANT_REQUEST_PAYMENT: ApiMerchantRequestPayment,
        PathValues.API_MERCHANT_ADD: ApiMerchantAdd,
        PathValues.API_MERCHANT_GET_DATA: ApiMerchantGetData,
        PathValues.API_PREFERENCE: ApiPreference,
        PathValues.API_PREFERENCE_PROFILE_PICTURE: ApiPreferenceProfilePicture,
        PathValues.API_PREFERENCE_NOTIFICATION_COUNT: ApiPreferenceNotificationCount,
        PathValues.API_PREFERENCE_SET_ALLOW_MARKETING_EMAILS: ApiPreferenceSetAllowMarketingEmails,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_USER_NAME: ApiPreferenceSetVisibleByUserName,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_EMAIL: ApiPreferenceSetVisibleByEmail,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_PHONE: ApiPreferenceSetVisibleByPhone,
        PathValues.API_PREFERENCE_SET_LOCATION_VISIBLE: ApiPreferenceSetLocationVisible,
        PathValues.API_PREFERENCE_SET_FIND_OPTION: ApiPreferenceSetFindOption,
        PathValues.API_PREFERENCE_SET_NOTIFY_ON_NEW_APPROVAL: ApiPreferenceSetNotifyOnNewApproval,
        PathValues.API_PREFERENCE_SET_NOTIFY_ON_NEW_TRANSACTION: ApiPreferenceSetNotifyOnNewTransaction,
        PathValues.API_PREFERENCE_SET_NOTIFY_VIA_EMAIL: ApiPreferenceSetNotifyViaEmail,
        PathValues.API_PREFERENCE_SET_LAT_LNG: ApiPreferenceSetLatLng,
        PathValues.API_PREFERENCE_SET_LANGUAGE: ApiPreferenceSetLanguage,
        PathValues.API_PREFERENCE_SET_PAY_FEES_FROM_SAVINGS: ApiPreferenceSetPayFeesFromSavings,
        PathValues.API_PREFERENCE_SET_DEFAULT_OTPTYPE: ApiPreferenceSetDefaultOTPType,
        PathValues.API_PREFERENCE_SET_PROFILE_PICTURE: ApiPreferenceSetProfilePicture,
        PathValues.API_PREFERENCE_SET_NOTIFICATION_PUSH_TOKEN: ApiPreferenceSetNotificationPushToken,
        PathValues.API_PREFERENCE_SET_APPROVAL_WEBHOOK: ApiPreferenceSetApprovalWebhook,
        PathValues.API_PREFERENCE_SET_PAYMENT_WEBHOOK: ApiPreferenceSetPaymentWebhook,
        PathValues.API_PREFERENCE_SET_REQUEST_PAYMENT_WEBHOOK: ApiPreferenceSetRequestPaymentWebhook,
        PathValues.API_PREFERENCE_NOTIFICATION_COUNT_CLEAR: ApiPreferenceNotificationCountClear,
        PathValues.API_PROFILE_GET: ApiProfileGet,
        PathValues.API_PROFILE_GET_FULL: ApiProfileGetFull,
        PathValues.API_PROFILE_LOG: ApiProfileLog,
        PathValues.API_PROFILE_SET_USER_NAME: ApiProfileSetUserName,
        PathValues.API_PROFILE_SET_PASSWORD: ApiProfileSetPassword,
        PathValues.API_PROFILE_SET_PIN: ApiProfileSetPin,
        PathValues.API_PROFILE_CLEAR_PIN: ApiProfileClearPin,
        PathValues.API_PROFILE_UNLOCK: ApiProfileUnlock,
        PathValues.API_PROFILE_LOCK: ApiProfileLock,
        PathValues.API_RELATIONSHIP_LIST: ApiRelationshipList,
        PathValues.API_RELATIONSHIP_GET_MODEL: ApiRelationshipGetModel,
        PathValues.API_RELATIONSHIP_DEFAULT_WALLET: ApiRelationshipDefaultWallet,
        PathValues.API_RELATIONSHIP_DEFAULT_WALLETS: ApiRelationshipDefaultWallets,
        PathValues.API_RELATIONSHIP_WALLETS: ApiRelationshipWallets,
        PathValues.API_RELATIONSHIP_LINKED_WALLETS: ApiRelationshipLinkedWallets,
        PathValues.API_RELATIONSHIP_GET_WALLET_ACCESS: ApiRelationshipGetWalletAccess,
        PathValues.API_RELATIONSHIP_TRANSACTIONS: ApiRelationshipTransactions,
        PathValues.API_RELATIONSHIP_ADD: ApiRelationshipAdd,
        PathValues.API_RELATIONSHIP_SET_STATUS_ACTIVE: ApiRelationshipSetStatusActive,
        PathValues.API_RELATIONSHIP_SET_STATUS_HIDDEN: ApiRelationshipSetStatusHidden,
        PathValues.API_RELATIONSHIP_SET_STATUS_BLOCKED: ApiRelationshipSetStatusBlocked,
        PathValues.API_RELATIONSHIP_SET_ACCESS: ApiRelationshipSetAccess,
        PathValues.API_REPORT_GET: ApiReportGet,
        PathValues.API_REPORT_SAVE: ApiReportSave,
        PathValues.API_SECURITY_GET_TOKEN: ApiSecurityGetToken,
        PathValues.API_SECURITY_FIREBASE_LOGIN: ApiSecurityFirebaseLogin,
        PathValues.API_SECURITY_GOOGLE_LOGIN: ApiSecurityGoogleLogin,
        PathValues.API_SECURITY_APPLE_LOGIN: ApiSecurityAppleLogin,
        PathValues.API_SECURITY_LOGOUT: ApiSecurityLogout,
        PathValues.API_SECURITY_REGISTER: ApiSecurityRegister,
        PathValues.API_SECURITY_VALIDATE_USER: ApiSecurityValidateUser,
        PathValues.API_SECURITY_SEND_OTP_TO_EMAIL: ApiSecuritySendOtpToEmail,
        PathValues.API_SECURITY_SEND_OTP_TO_SMS: ApiSecuritySendOtpToSMS,
        PathValues.API_SECURITY_CHECK_OTP: ApiSecurityCheckOtp,
        PathValues.API_SECURITY_SEND_OTP: ApiSecuritySendOtp,
        PathValues.API_SECURITY_SEND_NEW_OTP: ApiSecuritySendNewOtp,
        PathValues.API_SECURITY_GET_CAPTCHA: ApiSecurityGetCaptcha,
        PathValues.API_SECURITY_ACTIVATE_ACCOUNT: ApiSecurityActivateAccount,
        PathValues.API_SECURITY_GET_RESET_KEY: ApiSecurityGetResetKey,
        PathValues.API_SECURITY_RESET_PASSWORD: ApiSecurityResetPassword,
        PathValues.API_SYSTEM_INFO: ApiSystemInfo,
        PathValues.API_SYSTEM_MERCHANTS: ApiSystemMerchants,
        PathValues.API_SYSTEM_COUNTRY_LIST: ApiSystemCountryList,
        PathValues.API_SYSTEM_CURRENCIES: ApiSystemCurrencies,
        PathValues.API_SYSTEM_BANKS: ApiSystemBanks,
        PathValues.API_SYSTEM_BANK_COUNT: ApiSystemBankCount,
        PathValues.API_SYSTEM_BANK: ApiSystemBank,
        PathValues.API_TASK_GET_ID: ApiTaskGetId,
        PathValues.API_TASK_ADD_COMMENT_ID: ApiTaskAddCommentId,
        PathValues.API_TASK_ADD_ATTACHMENT_ID: ApiTaskAddAttachmentId,
        PathValues.API_TASK_HIDE_ID: ApiTaskHideId,
        PathValues.API_TASK_SHOW_ID: ApiTaskShowId,
        PathValues.API_TASK_CANCEL_ID: ApiTaskCancelId,
        PathValues.API_TASK_ONE_OFF_WITHDRAWAL_AMOUNT_REQUEST_ACCOUNT_ID: ApiTaskOneOffWithdrawalAmountRequestAccountId,
        PathValues.API_TASK_DAILY_WITHDRAWAL_LIMIT_REQUEST_ACCOUNT_ID: ApiTaskDailyWithdrawalLimitRequestAccountId,
        PathValues.API_TRANSACTION_STATUS_BY_REFERENCE_ACCOUNT_ID: ApiTransactionStatusByReferenceAccountId,
        PathValues.API_TRANSACTION_INSTANT_PAYMENT_QRCODE: ApiTransactionInstantPaymentQRCode,
        PathValues.API_TRANSACTION_APPROVAL_CANCEL: ApiTransactionApprovalCancel,
        PathValues.API_TRANSACTION_APPROVAL_ACCEPT: ApiTransactionApprovalAccept,
        PathValues.API_TRANSACTION_APPROVAL_REJECT: ApiTransactionApprovalReject,
        PathValues.API_TRANSACTION_SEND_PAYMENT: ApiTransactionSendPayment,
        PathValues.API_TRANSACTION_REQUEST_PAYMENT: ApiTransactionRequestPayment,
        PathValues.API_TRANSACTION_WALLET_EXCHANGE: ApiTransactionWalletExchange,
        PathValues.API_TRANSACTION_BANK_DEPOSIT: ApiTransactionBankDeposit,
        PathValues.API_TRANSACTION_AGENT_DEPOSIT: ApiTransactionAgentDeposit,
        PathValues.API_TRANSACTION_AGENT_WITHDRAWAL: ApiTransactionAgentWithdrawal,
        PathValues.API_TRANSACTION_SAVINGS_DEPOSIT: ApiTransactionSavingsDeposit,
        PathValues.API_TRANSACTION_SAVINGS_WITHDRAWAL: ApiTransactionSavingsWithdrawal,
        PathValues.API_WALLET_LIST: ApiWalletList,
        PathValues.API_WALLET_SAVINGS_LIST: ApiWalletSavingsList,
        PathValues.API_WALLET_ACCOUNT_ID: ApiWalletAccountId,
        PathValues.API_WALLET_INFO: ApiWalletInfo,
        PathValues.API_WALLET_INFO_LIST: ApiWalletInfoList,
        PathValues.API_WALLET_OWNER: ApiWalletOwner,
        PathValues.API_WALLET_OPTIONS: ApiWalletOptions,
        PathValues.API_WALLET_TRANSACTIONS_ACCOUNT_ID: ApiWalletTransactionsAccountId,
        PathValues.API_WALLET_TRANSACTION_TRANSACTION_ID: ApiWalletTransactionTransactionId,
        PathValues.API_WALLET_TRANSACTION_BY_REFERENCE_ACCOUNT_ID: ApiWalletTransactionByReferenceAccountId,
        PathValues.API_WALLET_TRANSACTION_SUMMARY: ApiWalletTransactionSummary,
        PathValues.API_WALLET_MONTHLY_BALANCES: ApiWalletMonthlyBalances,
        PathValues.API_WALLET_TOTAL_WITHDRAWALS: ApiWalletTotalWithdrawals,
        PathValues.API_WALLET_ADD: ApiWalletAdd,
        PathValues.API_WALLET_SET_DEFAULT_ACCOUNT_ID: ApiWalletSetDefaultAccountId,
        PathValues.API_WALLET_CLEAR_NEW_TRANSACTION_COUNT_ACCOUNT_ID: ApiWalletClearNewTransactionCountAccountId,
        PathValues.API_WALLET_STATEMENT_REPORT_ACCOUNT_ID: ApiWalletStatementReportAccountId,
        PathValues.API_WALLET_TRANSACTION_REPORT_TRANSACTION_ID: ApiWalletTransactionReportTransactionId,
        PathValues.API_WALLET_ID: ApiWalletId,
        PathValues.API_WALLET_APPROVAL_STATUS: ApiWalletApprovalStatus,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_AGENT_SUB_AGENT_LIST: ApiAgentSubAgentList,
        PathValues.API_AGENT_LOCATIONS: ApiAgentLocations,
        PathValues.API_AGENT_WALLET_ACCOUNT_ID: ApiAgentWalletAccountId,
        PathValues.API_AGENT_TRANSACTIONS_ACCOUNT_ID: ApiAgentTransactionsAccountId,
        PathValues.API_AGENT_TRADE_LIMIT_REQUEST: ApiAgentTradeLimitRequest,
        PathValues.API_AGENT_CASH_REQUEST: ApiAgentCashRequest,
        PathValues.API_AGENT_ADD_SUB_AGENT_REQUEST: ApiAgentAddSubAgentRequest,
        PathValues.API_AGENT_AGENT_SEND_PAYMENT: ApiAgentAgentSendPayment,
        PathValues.API_AGENT_AGENT_REQUEST_PAYMENT: ApiAgentAgentRequestPayment,
        PathValues.API_AGENT_REFERENCE_REQUEST: ApiAgentReferenceRequest,
        PathValues.API_AGENT_REFERENCE_ENDORSE: ApiAgentReferenceEndorse,
        PathValues.API_AGENT_SUB_AGENT_APPROVED: ApiAgentSubAgentApproved,
        PathValues.API_AGENT_SET_WALLET_ACCESS: ApiAgentSetWalletAccess,
        PathValues.API_AGENT_SET_SUB_AGENT_COMMISSION: ApiAgentSetSubAgentCommission,
        PathValues.API_AGENT_DELETE_SUB_AGENT: ApiAgentDeleteSubAgent,
        PathValues.API_CATEGORY_GET_MODEL: ApiCategoryGetModel,
        PathValues.API_CATEGORY_LIST: ApiCategoryList,
        PathValues.API_CATEGORY_LIST_ALL: ApiCategoryListAll,
        PathValues.API_CATEGORY_SET_NAME: ApiCategorySetName,
        PathValues.API_CATEGORY_SET_DESCRIPTION: ApiCategorySetDescription,
        PathValues.API_CATEGORY_SET_PUBLIC: ApiCategorySetPublic,
        PathValues.API_CATEGORY_SET_DATA_HASH_ID: ApiCategorySetDataHashId,
        PathValues.API_CATEGORY_SET_PDF_ATTACHMENT: ApiCategorySetPdfAttachment,
        PathValues.API_CATEGORY_ADD_ITEM: ApiCategoryAddItem,
        PathValues.API_CATEGORY_DELETE_HASH_ID: ApiCategoryDeleteHashId,
        PathValues.API_CATEGORY_GET_PROPERTIES: ApiCategoryGetProperties,
        PathValues.API_CATEGORY_UPDATE_PROPERTY: ApiCategoryUpdateProperty,
        PathValues.API_CATEGORY_ADD_PROPERTY: ApiCategoryAddProperty,
        PathValues.API_CATEGORY_DELETE_PROPERTY_HASH_ID: ApiCategoryDeletePropertyHashId,
        PathValues.API_CONTACT_SEARCH: ApiContactSearch,
        PathValues.API_CONTACT_GET_ID: ApiContactGetId,
        PathValues.API_CONTACT_GET_BUSINESS_HASH_ID: ApiContactGetBusinessHashId,
        PathValues.API_CONTACT_NAME_ID: ApiContactNameId,
        PathValues.API_CONTACT_TAX_COUNTRY_CODE: ApiContactTaxCountryCode,
        PathValues.API_CONTACT_BANKS: ApiContactBanks,
        PathValues.API_CONTACT_UPDATE: ApiContactUpdate,
        PathValues.API_CONTACT_UPDAT_BUSINESS: ApiContactUpdatBusiness,
        PathValues.API_CONTACT_SET_MOBILE: ApiContactSetMobile,
        PathValues.API_CONTACT_SET_EMAIL: ApiContactSetEmail,
        PathValues.API_CONTACT_SET_TAX_COUNTRY_CODE: ApiContactSetTaxCountryCode,
        PathValues.API_CONTACT_TASKS_ID: ApiContactTasksId,
        PathValues.API_CONTACT_MESSAGES: ApiContactMessages,
        PathValues.API_CONTACT_MESSAGES_UNREAD_COUNT: ApiContactMessagesUnreadCount,
        PathValues.API_CONTACT_MESSAGES_SET_READ: ApiContactMessagesSetRead,
        PathValues.API_CONTACT_SEND_MESSAGE: ApiContactSendMessage,
        PathValues.API_CONTACT_ADD_TICKET: ApiContactAddTicket,
        PathValues.API_DOCUMENT_TYPES: ApiDocumentTypes,
        PathValues.API_DOCUMENT_LIST_CONTACT_ID: ApiDocumentListContactId,
        PathValues.API_DOCUMENT_ADD_CONTACT_ID: ApiDocumentAddContactId,
        PathValues.API_DOCUMENT_DELETE_ID: ApiDocumentDeleteId,
        PathValues.API_ISGPAY_CARD_DEPOSIT: ApiISGPayCardDeposit,
        PathValues.API_ISGPAY_CARD_DEPOSIT_RESPONSE: ApiISGPayCardDepositResponse,
        PathValues.API_ISGPAY_REQUEST_PAYMENT: ApiISGPayRequestPayment,
        PathValues.API_ISGPAY_REQUEST_PAYMENT_RESPONSE: ApiISGPayRequestPaymentResponse,
        PathValues.API_ISGPAY_SEND: ApiISGPaySend,
        PathValues.API_ISGPAY_SEND_RESPONSE: ApiISGPaySendResponse,
        PathValues.API_ISGPAY_CHECK_STATUS: ApiISGPayCheckStatus,
        PathValues.API_ITEM_MODEL: ApiItemModel,
        PathValues.API_ITEM_LIST: ApiItemList,
        PathValues.API_ITEM_MERGE_TEMPLATE: ApiItemMergeTemplate,
        PathValues.API_ITEM_TRANSACTION_REPORT_TRANSACTION_ID: ApiItemTransactionReportTransactionId,
        PathValues.API_ITEM_SET_IMAGE: ApiItemSetImage,
        PathValues.API_ITEM_SET_AMOUNT: ApiItemSetAmount,
        PathValues.API_ITEM_SET_PROPERTY: ApiItemSetProperty,
        PathValues.API_ITEM_SET_PROPERTY_IMAGE: ApiItemSetPropertyImage,
        PathValues.API_ITEM_SET_NAME: ApiItemSetName,
        PathValues.API_ITEM_SET_DESCRIPTION: ApiItemSetDescription,
        PathValues.API_ITEM_SET_DETAIL: ApiItemSetDetail,
        PathValues.API_ITEM_ADD: ApiItemAdd,
        PathValues.API_ITEM_DELETEHASH_ID: ApiItemDeletehashId,
        PathValues.API_ITEM_SUBSCRIPTIONS: ApiItemSubscriptions,
        PathValues.API_ITEM_SUBSCRIBE_HASH_ID: ApiItemSubscribeHashId,
        PathValues.API_ITEM_UNSUBSCRIBE_HASH_ID: ApiItemUnsubscribeHashId,
        PathValues.API_ITEM_PIN_SUBSCRIPTION: ApiItemPinSubscription,
        PathValues.API_ITEM_UNPIN_SUBSCRIPTION: ApiItemUnpinSubscription,
        PathValues.API_MERCHANT_REQUEST_PAYMENT: ApiMerchantRequestPayment,
        PathValues.API_MERCHANT_ADD: ApiMerchantAdd,
        PathValues.API_MERCHANT_GET_DATA: ApiMerchantGetData,
        PathValues.API_PREFERENCE: ApiPreference,
        PathValues.API_PREFERENCE_PROFILE_PICTURE: ApiPreferenceProfilePicture,
        PathValues.API_PREFERENCE_NOTIFICATION_COUNT: ApiPreferenceNotificationCount,
        PathValues.API_PREFERENCE_SET_ALLOW_MARKETING_EMAILS: ApiPreferenceSetAllowMarketingEmails,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_USER_NAME: ApiPreferenceSetVisibleByUserName,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_EMAIL: ApiPreferenceSetVisibleByEmail,
        PathValues.API_PREFERENCE_SET_VISIBLE_BY_PHONE: ApiPreferenceSetVisibleByPhone,
        PathValues.API_PREFERENCE_SET_LOCATION_VISIBLE: ApiPreferenceSetLocationVisible,
        PathValues.API_PREFERENCE_SET_FIND_OPTION: ApiPreferenceSetFindOption,
        PathValues.API_PREFERENCE_SET_NOTIFY_ON_NEW_APPROVAL: ApiPreferenceSetNotifyOnNewApproval,
        PathValues.API_PREFERENCE_SET_NOTIFY_ON_NEW_TRANSACTION: ApiPreferenceSetNotifyOnNewTransaction,
        PathValues.API_PREFERENCE_SET_NOTIFY_VIA_EMAIL: ApiPreferenceSetNotifyViaEmail,
        PathValues.API_PREFERENCE_SET_LAT_LNG: ApiPreferenceSetLatLng,
        PathValues.API_PREFERENCE_SET_LANGUAGE: ApiPreferenceSetLanguage,
        PathValues.API_PREFERENCE_SET_PAY_FEES_FROM_SAVINGS: ApiPreferenceSetPayFeesFromSavings,
        PathValues.API_PREFERENCE_SET_DEFAULT_OTPTYPE: ApiPreferenceSetDefaultOTPType,
        PathValues.API_PREFERENCE_SET_PROFILE_PICTURE: ApiPreferenceSetProfilePicture,
        PathValues.API_PREFERENCE_SET_NOTIFICATION_PUSH_TOKEN: ApiPreferenceSetNotificationPushToken,
        PathValues.API_PREFERENCE_SET_APPROVAL_WEBHOOK: ApiPreferenceSetApprovalWebhook,
        PathValues.API_PREFERENCE_SET_PAYMENT_WEBHOOK: ApiPreferenceSetPaymentWebhook,
        PathValues.API_PREFERENCE_SET_REQUEST_PAYMENT_WEBHOOK: ApiPreferenceSetRequestPaymentWebhook,
        PathValues.API_PREFERENCE_NOTIFICATION_COUNT_CLEAR: ApiPreferenceNotificationCountClear,
        PathValues.API_PROFILE_GET: ApiProfileGet,
        PathValues.API_PROFILE_GET_FULL: ApiProfileGetFull,
        PathValues.API_PROFILE_LOG: ApiProfileLog,
        PathValues.API_PROFILE_SET_USER_NAME: ApiProfileSetUserName,
        PathValues.API_PROFILE_SET_PASSWORD: ApiProfileSetPassword,
        PathValues.API_PROFILE_SET_PIN: ApiProfileSetPin,
        PathValues.API_PROFILE_CLEAR_PIN: ApiProfileClearPin,
        PathValues.API_PROFILE_UNLOCK: ApiProfileUnlock,
        PathValues.API_PROFILE_LOCK: ApiProfileLock,
        PathValues.API_RELATIONSHIP_LIST: ApiRelationshipList,
        PathValues.API_RELATIONSHIP_GET_MODEL: ApiRelationshipGetModel,
        PathValues.API_RELATIONSHIP_DEFAULT_WALLET: ApiRelationshipDefaultWallet,
        PathValues.API_RELATIONSHIP_DEFAULT_WALLETS: ApiRelationshipDefaultWallets,
        PathValues.API_RELATIONSHIP_WALLETS: ApiRelationshipWallets,
        PathValues.API_RELATIONSHIP_LINKED_WALLETS: ApiRelationshipLinkedWallets,
        PathValues.API_RELATIONSHIP_GET_WALLET_ACCESS: ApiRelationshipGetWalletAccess,
        PathValues.API_RELATIONSHIP_TRANSACTIONS: ApiRelationshipTransactions,
        PathValues.API_RELATIONSHIP_ADD: ApiRelationshipAdd,
        PathValues.API_RELATIONSHIP_SET_STATUS_ACTIVE: ApiRelationshipSetStatusActive,
        PathValues.API_RELATIONSHIP_SET_STATUS_HIDDEN: ApiRelationshipSetStatusHidden,
        PathValues.API_RELATIONSHIP_SET_STATUS_BLOCKED: ApiRelationshipSetStatusBlocked,
        PathValues.API_RELATIONSHIP_SET_ACCESS: ApiRelationshipSetAccess,
        PathValues.API_REPORT_GET: ApiReportGet,
        PathValues.API_REPORT_SAVE: ApiReportSave,
        PathValues.API_SECURITY_GET_TOKEN: ApiSecurityGetToken,
        PathValues.API_SECURITY_FIREBASE_LOGIN: ApiSecurityFirebaseLogin,
        PathValues.API_SECURITY_GOOGLE_LOGIN: ApiSecurityGoogleLogin,
        PathValues.API_SECURITY_APPLE_LOGIN: ApiSecurityAppleLogin,
        PathValues.API_SECURITY_LOGOUT: ApiSecurityLogout,
        PathValues.API_SECURITY_REGISTER: ApiSecurityRegister,
        PathValues.API_SECURITY_VALIDATE_USER: ApiSecurityValidateUser,
        PathValues.API_SECURITY_SEND_OTP_TO_EMAIL: ApiSecuritySendOtpToEmail,
        PathValues.API_SECURITY_SEND_OTP_TO_SMS: ApiSecuritySendOtpToSMS,
        PathValues.API_SECURITY_CHECK_OTP: ApiSecurityCheckOtp,
        PathValues.API_SECURITY_SEND_OTP: ApiSecuritySendOtp,
        PathValues.API_SECURITY_SEND_NEW_OTP: ApiSecuritySendNewOtp,
        PathValues.API_SECURITY_GET_CAPTCHA: ApiSecurityGetCaptcha,
        PathValues.API_SECURITY_ACTIVATE_ACCOUNT: ApiSecurityActivateAccount,
        PathValues.API_SECURITY_GET_RESET_KEY: ApiSecurityGetResetKey,
        PathValues.API_SECURITY_RESET_PASSWORD: ApiSecurityResetPassword,
        PathValues.API_SYSTEM_INFO: ApiSystemInfo,
        PathValues.API_SYSTEM_MERCHANTS: ApiSystemMerchants,
        PathValues.API_SYSTEM_COUNTRY_LIST: ApiSystemCountryList,
        PathValues.API_SYSTEM_CURRENCIES: ApiSystemCurrencies,
        PathValues.API_SYSTEM_BANKS: ApiSystemBanks,
        PathValues.API_SYSTEM_BANK_COUNT: ApiSystemBankCount,
        PathValues.API_SYSTEM_BANK: ApiSystemBank,
        PathValues.API_TASK_GET_ID: ApiTaskGetId,
        PathValues.API_TASK_ADD_COMMENT_ID: ApiTaskAddCommentId,
        PathValues.API_TASK_ADD_ATTACHMENT_ID: ApiTaskAddAttachmentId,
        PathValues.API_TASK_HIDE_ID: ApiTaskHideId,
        PathValues.API_TASK_SHOW_ID: ApiTaskShowId,
        PathValues.API_TASK_CANCEL_ID: ApiTaskCancelId,
        PathValues.API_TASK_ONE_OFF_WITHDRAWAL_AMOUNT_REQUEST_ACCOUNT_ID: ApiTaskOneOffWithdrawalAmountRequestAccountId,
        PathValues.API_TASK_DAILY_WITHDRAWAL_LIMIT_REQUEST_ACCOUNT_ID: ApiTaskDailyWithdrawalLimitRequestAccountId,
        PathValues.API_TRANSACTION_STATUS_BY_REFERENCE_ACCOUNT_ID: ApiTransactionStatusByReferenceAccountId,
        PathValues.API_TRANSACTION_INSTANT_PAYMENT_QRCODE: ApiTransactionInstantPaymentQRCode,
        PathValues.API_TRANSACTION_APPROVAL_CANCEL: ApiTransactionApprovalCancel,
        PathValues.API_TRANSACTION_APPROVAL_ACCEPT: ApiTransactionApprovalAccept,
        PathValues.API_TRANSACTION_APPROVAL_REJECT: ApiTransactionApprovalReject,
        PathValues.API_TRANSACTION_SEND_PAYMENT: ApiTransactionSendPayment,
        PathValues.API_TRANSACTION_REQUEST_PAYMENT: ApiTransactionRequestPayment,
        PathValues.API_TRANSACTION_WALLET_EXCHANGE: ApiTransactionWalletExchange,
        PathValues.API_TRANSACTION_BANK_DEPOSIT: ApiTransactionBankDeposit,
        PathValues.API_TRANSACTION_AGENT_DEPOSIT: ApiTransactionAgentDeposit,
        PathValues.API_TRANSACTION_AGENT_WITHDRAWAL: ApiTransactionAgentWithdrawal,
        PathValues.API_TRANSACTION_SAVINGS_DEPOSIT: ApiTransactionSavingsDeposit,
        PathValues.API_TRANSACTION_SAVINGS_WITHDRAWAL: ApiTransactionSavingsWithdrawal,
        PathValues.API_WALLET_LIST: ApiWalletList,
        PathValues.API_WALLET_SAVINGS_LIST: ApiWalletSavingsList,
        PathValues.API_WALLET_ACCOUNT_ID: ApiWalletAccountId,
        PathValues.API_WALLET_INFO: ApiWalletInfo,
        PathValues.API_WALLET_INFO_LIST: ApiWalletInfoList,
        PathValues.API_WALLET_OWNER: ApiWalletOwner,
        PathValues.API_WALLET_OPTIONS: ApiWalletOptions,
        PathValues.API_WALLET_TRANSACTIONS_ACCOUNT_ID: ApiWalletTransactionsAccountId,
        PathValues.API_WALLET_TRANSACTION_TRANSACTION_ID: ApiWalletTransactionTransactionId,
        PathValues.API_WALLET_TRANSACTION_BY_REFERENCE_ACCOUNT_ID: ApiWalletTransactionByReferenceAccountId,
        PathValues.API_WALLET_TRANSACTION_SUMMARY: ApiWalletTransactionSummary,
        PathValues.API_WALLET_MONTHLY_BALANCES: ApiWalletMonthlyBalances,
        PathValues.API_WALLET_TOTAL_WITHDRAWALS: ApiWalletTotalWithdrawals,
        PathValues.API_WALLET_ADD: ApiWalletAdd,
        PathValues.API_WALLET_SET_DEFAULT_ACCOUNT_ID: ApiWalletSetDefaultAccountId,
        PathValues.API_WALLET_CLEAR_NEW_TRANSACTION_COUNT_ACCOUNT_ID: ApiWalletClearNewTransactionCountAccountId,
        PathValues.API_WALLET_STATEMENT_REPORT_ACCOUNT_ID: ApiWalletStatementReportAccountId,
        PathValues.API_WALLET_TRANSACTION_REPORT_TRANSACTION_ID: ApiWalletTransactionReportTransactionId,
        PathValues.API_WALLET_ID: ApiWalletId,
        PathValues.API_WALLET_APPROVAL_STATUS: ApiWalletApprovalStatus,
    }
)
