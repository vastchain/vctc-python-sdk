from VctcClient  import VctcClient


# Api Client for Vastchain API erface.

class VctcApiClient:
    API_PREFIX = 'https://v1.api.tc.vastchain.ltd'
    COMMON_CHAIN_UPLOAD_PATH = '/common-chain-upload'
    COMMON_CHAIN_UPLOAD_FETCH_ON_CHAIN_IDS_PATH = '/common-chain-upload/fetchOnChainIds'
    SUBMERCHANT_PAY_PATH = '/submerchant-pay/'
    SUBMERCHANT_PAY_PRE_PAY_PREPAYID_PATH = '/submerchant-pay/prePay/'
    SUBMERCHANT_PAY_WECHAT_PAY_NATIVE_PATH = '/submerchant-pay/wechatPayNative'
    SUBMERCHANT_PAY_WECHAT_MINI_PAY_PATH = '/submerchant-pay/wechatPay'
    SUBMERCHANT_PAY_WECHAT_APP_PAY_PATH = '/submerchant-pay/wechatPayApp'
    SUBMERCHANT_PAY_REFUND_PATH = '/submerchant-pay/refund'
    MERCHANT_PAYMENT_PARAMS_PATH = '/merchant/paymentParams'
    FUNGIBLE_TOKEN_BALANCE_PATH = '/fungible-token/balance'
    FUNGIBLE_TOKEN_EVERI_PAY_PATH = '/fungible-token/everiPay'
    CREATE_DONATION_PROJECT_PATH = '/donation/project'
    CREATE_DONATION_DONATION_PATH = '/donation/donate'
    CREATE_DONATION_FETCH_ONCHAINIDS_PATH = '/donation/fetchOnChainIds'
    SEND_SMS_VERIFICATIONCODE_PATH = '/sms/verificationCode'
    COMMON_SIGN_EXPLORER_PATH = '/common-chain-upload/blockchain-explorer/special/voluntary-activity-sign'
    DONATION_EXPLORER_PATH = '/common-chain-upload/blockchain-explorer/special/donation'
    MERCHANT_LOGIN_PATH = '/merchant/login'
    CREATE_MERCHANT_PATH = '/merchant'
    CLIENT = None

    def __init__(self, appId, appSecret):
        self.apiPrefix = self.API_PREFIX
        self.appId = appId
        self.appSecret = appSecret
        if not self.CLIENT:
            self.CLIENT = VctcClient(self.API_PREFIX, appId, appSecret)

    # region erfaces to On-chain process

    # Submit a batch of information to the blockchain individually or in batches, supporting plaext and encrypted data
    # :param  items dict Containing following keys. A maximum of 500 records can be uploaded in a batch. The size of each item in the items  cannot exceed 50 KB.
    # :param  type The action category of the on-chain, such as voluntary-activity-register, represents public activity registration.For the definition of each action, please refer to the relevant page ending with "Action" in API Reference.
    # :param  args The specific parameters of the action on the chain. For different on-chain actions, the parameter field definitions are different. However, any item has an id. self id is recommended to use the relevant id of the data in your local database.For specific parameter requirements, please refer to the relevant pages ending with "Action" in the API Reference.
    # :return mixed
    # :throws VctcException

    def uploadCommonChain(self, items, itemStruct={}):
        return self.CLIENT.post(self.COMMON_CHAIN_UPLOAD_PATH, {}, {'items': items})

    # self erface is used to query the results of the on-chain synchronously, including the on-chain ID (OnChainId), block ID (Block Num), and transaction ID (Transaction Id). It is used to obtain the final confirmation status of the on-chain.
    # For different actions on the chain, the delay required to obtain the chain ID is different.For everiPay and everiPass actions, it usually takes only 1 second to complete.Some requests may not receive the on-chain ID until 3-4 minutes after the on-chain.
    # :param  items An  containing one or more on-chain items. A maximum of 500 records can be uploaded in a batch.
    # :return mixed
    # :throws VctcException

    def fetchOnChainIds(self, items):
        itemStruct = {"type": "", "queryType": "", "id": ""}
        return self.CLIENT.post(self.COMMON_CHAIN_UPLOAD_FETCH_ON_CHAIN_IDS_PATH, {}, {'items': items})

    # Submitting everiPay in EvtLink format, mainly used for debit of stored value cards / trusted pos / digital assets.
    # :param  items dict Containing following keys
    # :param  args dict Containing following keys
    # :param  type ="everiPay"
    # :param  id Cannot be repeated, it is recommended to use a completely strong random
    # :param  evtLink Required.For example, the QR code presented by the customer
    # :param float amount Required, the amount to be deducted (the precision of self quantity must be the same as the precision set when the egral or stored value was created, for example, if the precision is 2 decimal places, there must be 2 decimal places here)
    # :param  payee An valid public key
    # :return mixed
    # :throws VctcException

    def everiPay(self, items):
        itemStruct = {
            "type": "everiPay",
            "args": {
                "id": "",
                "evtLink": "",
                "amount": ""
            }
        }

        return self.uploadCommonChain(items, itemStruct)

    # Data exists on the blockchain in the form of "data buckets-data items-data fields (keys)".To upload data, you just need to create a bucket first, and then create a data item when there is data.Each data item can contain zero or more data fields (keys).
    # :param  items dict Containing following keys
    # :param  args dict Containing following keys
    # :param  type ="data-bucket-register"
    # :param  id Required. The ID of self bucket cannot exceed 32 characters. It can only consist of uppercase and lowercase letters or numbers.
    # :return mixed
    # :throws VctcException

    def registerDataBucket(self, items):
        itemStruct = {"type": "data-bucket-register", "args": {"id": ""}}
        return self.uploadCommonChain(items, itemStruct)

    # Data exists on the blockchain in the form of "data buckets-data items-data fields (keys)".To upload data, you just need to create a bucket first, and then create a data item when there is data.
    # :param  items dict Containing following keys
    # :param  type ="data-item-create"
    # :param  args dict Containing following keys
    # :param  parentId The id where the bucket is
    # :param  id Required. The ID of self bucket cannot exceed 32 characters. It can only consist of uppercase and lowercase letters or numbers.
    # :param  data array Containing following keys
    # :param  key
    # :param  type ="publicText" type Currently only publicText
    # :param  value
    #
    # :return mixed
    # :throws VctcException

    def createDataitem(self, items):
        itemStruct = {"type": "data-item-create",
                      "args": {
                          "id": "",
                          "parentId": "",
                          "data": [
                              {
                                  "key": "",
                                  "type": "",
                                  "value": ""
                              }
                          ]
                      }}
        return self.uploadCommonChain(items, itemStruct)

    # Support non-profit / volunteer / public activities.
    # :param  items dict Containing following keys
    # :param  type ="voluntary-activity-register"
    # :param  args dict Containing following keys
    # :param  id Required, the project's activity id can be uniquely found in the project's database. Please ensure that the id is not duplicated in the same `appId` and can be queried for the project. It can only consist of uppercase and lowercase letters or numbers, and the length cannot exceed 32 bit
    # :param  createTime NotRequired, the creation time of the event (UNIX timestamp to milliseconds), pass it as a numeric value
    # :param  title NotRequired,activity name
    # :param  desc NotRequired,Activity description
    # :param  organization Name of the organization that initiated the event
    # :param  organizationId Required, unique ID of event organization
    # :param  openTime Not Required,Active start time (milliseconds UNIX timestamp)
    # :param  closeTime Required, Active end time (milliseconds UNIX timestamp)
    # :param  district Not Required, Active area
    # :param  address Not Required, Active Location
    # :param  memo Not Required, Active notes
    # :param  categories array Activity category, please provide as an
    # :param  x If you want to encrypt the optional fields in the above fields, move them directly o the x attribute (id and organizationId do not allow encryption)
    # :return mixed
    # :throws VctcException

    def registerVoluntaryActivity(self, items):
        itemStruct = {"type": "voluntary-activity-register",
                      "args": {
                          "id": "",
                          "createTime": "",
                          "organizationId": "",
                          "title": "",
                          "desc": "",
                          "organization": "",
                          "organizationId": "",
                          "openTime": "",
                          "closeTime": "",
                          "district": "",
                          "address": "",
                          "memo": "",
                          "categories": [],
                          "x": [],
                      }
                      }
        return self.uploadCommonChain(items, itemStruct)

    # Check-in for non-profit / volunteer / public events, optional GPS or other note information.
    # :param  items dict Containing following keys
    # :param  type ="voluntary-activity-signIn"or "voluntary-activity-signOut"
    # :param  args dict Containing following keys
    # @para  id Required, The project's activity id can be uniquely found in the project's database. Please make sure that the id is not duplicated in the same `appId` and can be queried for the project. It can only consist of uppercase and lowercase letters or numbers, and the length does not exceed 32 bits.
    # :param  parentId Activity id
    # :param  userId UserId of the checked-in user, the same user id must be the same
    # :param  createTime Check-in / check-out time (UNIX millisecond timestamp)
    # :param  durationInMinutes Required when checking out, the online duration of self event (in milliseconds, must be equal to the difference between the `createTime` time of the check out and check in)
    # :param  memo remark
    # :param  x Containing following keys
    # :param  signerName Encrypted, optional, signed in user's name
    # :param  gps array Encrypted, optional, signed-in user's GPS
    # :return mixed
    # :throws VctcException

    def signVoluntaryActivity(self, items):
        itemStruct = {"type": "voluntary-activity-signIn",
                      "args": {
                          "id": "",
                          "parentId": "",
                          "userId": "",
                          "durationInMinutes": "",
                          "memo": "",
                          "createTime": "",
                          "x": {
                              "signerName": "",
                              "gps": [],
                          }
                      }
                      }
        return self.uploadCommonChain(items, itemStruct)

    # Register a door lock model.
    # :param  items dict Containing following keys
    # :param  type ="elligent-doorlock-model"
    # :param  args dict Containing following keys
    # :param  id Required, door lock model, cannot be repeated in the same appId
    # :param  memo Not Required, remark
    # :return mixed
    # :throws VctcException

    def ModelelligentDoorlock(self, items):
        itemStruct = {"type": "elligent-doorlock-model", "args": {"id": ""}}
        return self.uploadCommonChain(items, itemStruct)

    # Register a door lock with a U-chain security chip.
    # :param  items dict Containing following keys
    # :param  type ="elligent-doorlock-register"
    # :param  args dict Containing following keys
    # :param  id Required, Door lock ID, cannot be duplicated in the same appId
    # :param  ownerUserId Required, Public key of the security chip, the assets on the chain will belong to self address
    # :param  memo Not Required, remark
    # :return mixed
    # :throws VctcException

    def RegisterelligentDoorlock(self, items):
        itemStruct = {
            "type": "elligent-doorlock-register",
            "args": {
                "id": "",
                "ownerUserId": "",
                "memo": ""
            }
        }
        return self.uploadCommonChain(items, itemStruct)

    # Submit everiPass, which is mainly used for pass verification, such as door locks, degree entry, school tickets, movie tickets, etc., optional destruction.
    # :param  items dict Containing following keys
    # :param  type ="everiPass"
    # :param  args dict Containing following keys
    # :param  evtLink Reference https://www.everitoken.io/developers/deep_dive/evtlink,everipay,everipass。
    # :param  actionMemo Not Required, remark
    # :return mixed
    # :throws VctcException

    def everiPass(self, items):
        itemStruct = {"type": "everiPass", "args": {"evtLink": "", "actionMemo": ""}}
        return self.uploadCommonChain(items, itemStruct)

    # Trusted Credit is an innovative on-chain homogenization token. All issuance and circulation are on the chain, but it is safe and controllable and is not a digital currency. It is widely used in po cards, coupons, stored-value cards, and cross-industry alliances, Credit reporting, poverty alleviation, etc.
    # :param  items dict Containing following keys
    # :param  type ="fungible-token-symbol-register"
    # :param  args dict Containing following keys
    # :param  id Token ID, please keep in mind that it cannot be duplicated within one appId
    # :param  name The token name can only consist of uppercase and lowercase letters, numbers, or dots (.) And (-), and 3 to 12 characters are recommended (up to 21 characters)
    # :param  fullName The full name of the token, which can only consist of uppercase and lowercase letters, numbers, or dots (.) And (-). 6-21 characters are recommended (up to 21 characters)
    # :param  totalSupply The maximum issuance of tokens, as it cannot be tampered, please reserve the demand for the next 100 years
    # :param  precision Precision is the maximum number of digits after the decimal po, which must be between 0-8
    # :param  icon Icon, png format, in order to keep the performance picture below 10 KB, it must conform to the DATAURL specification (RFC2397). There are many roductions and tools on the ernet.
    # :return mixed
    # :throws VctcException

    def registerFungibleTokenSymbol(self, items):
        itemStruct = {
            "type": "fungible-token-symbol-register",
            "args": {
                "id": "",
                "name": "",
                "fullName": "",
                "totalSupply": "",
                "precision": "",
                "icon": ""
            }
        }
        return self.uploadCommonChain(items, itemStruct)

    # After you have created trusted pos, you can issue some or all of the tokens to the designated user account.Each user account is represented by a userId, which is common in the entire YuChain Cloud erface, and each appId is isolated from each other.
    # :param  items dict Containing following keys
    # :param  type ="fungible-token-issue"
    # :param  args dict Containing following keys
    # :param  id Represents the unique id of self operation, cannot be repeated within the same appId range
    # :param  tokenAppId Create the AppId for the trusted credit
    # :param  userId User ID to issue pos / tokens, cannot be duplicated in the same appId
    # :param  tokenId The Id of the trusted credit (the id field in the Create Trusted Credit erface above)
    # :param  amount Quantity, please note that the decimal po cannot exceed the precision
    # :param  tokenId The Id of the trusted credit (the id field in the Create Trusted Credit erface above)
    # :param  memo Not Required, release notes, no more than 255 characters
    # :return mixed
    # :throws VctcException

    def fungibleTokenIssue(self, items):
        itemStruct = {
            "type": "fungible-token-issue",
            "args": {
                "id": "",
                "tokenAppId": "",
                "tokenId": "",
                "userId": "",
                "amount": "",
                "memo": ""
            }
        }
        return self.uploadCommonChain(items, itemStruct)

    # After you have issued Trusted Pos, you can transfer money.Each user account is represented by a userId, which is common in the entire YuChain Cloud erface, and each appId is isolated from each other.
    # :param  items dict Containing following keys
    # :param  type ="fungible-token-transfer"
    # :param  args dict Containing following keys
    # :param  id Represents the unique id of self operation, cannot be repeated within the same appId range
    # :param  tokenAppId Create the AppId for the trusted credit
    # :param  tokenId The Id of the trusted credit (the id field in the Create Trusted Credit erface above)
    # :param float amount Quantity, please note that the decimal po cannot exceed the precision
    # :param  tokenId The Id of the trusted credit (the id field in the Create Trusted Credit erface above)
    # :param  memo Not Required, release notes, no more than 255 characters
    # :param  fromUserId Which userId to transfer money from
    # :param  toUserAppId Which userAppId to transfer money to
    # :param  toUserId Not Which userId to transfer money to
    # :return mixed
    # :throws VctcException

    def TransferFungibleToken(self, items):
        itemStruct = {
            "type": "fungible-token-transfer",
            "args": {
                "id": "",
                "tokenAppId": "",
                "tokenId": "",
                "fromUserId": "",
                "toUserAppId": "",
                "toUserId": "",
                "amount": "",
                "memo": ""
            }
        }
        return self.uploadCommonChain(items, itemStruct)

    # endregion

    # region Payment-related erface

    # For all other payment methods, you can directly provide the payment parameters obtained through Yulian Cloud to the WeChat erface.For example, if you want to perform WeChat scan code payment, you only need to call "Create WeChat Scan Code Payment Parameters" and then generate a QR code to allow users to scan.
    # :param  subMerchantId The sub-merchant number that initiated the payment
    # :param  totalAmount Transaction amount, sent as a , Accurate to the cent
    # :param  orderId Order number associated with self exchange
    # :param  extraInfo The additional information associated with self exchange can be set arbitrarily, it is recommended to use JSON format
    # :return mixed
    # :throws VctcException

    def submerchantPay(self, subMerchantId, totalAmount, orderId="", extraInfo=""):
        items = {
            "subMerchantId": subMerchantId,
            "totalAmount": totalAmount,
            "orderId": orderId,
            "extraInfo": extraInfo
        }
        return self.CLIENT.post(self.SUBMERCHANT_PAY_PATH, (), items)

    # Get sub-merchant payment details
    # :param  prepayid Sub-merchant prepayment note number resolved in QR code scene
    # :param  waitForFinish The Not required value is 0 or 1. The default value is 0, which indicates whether to block to wait for real-time payment success notification (strongly recommended)
    # :return mixed
    # :throws VctcException

    def submerchantPrePayInfo(self, prepayid, waitForFinish=0):
        return self.CLIENT.get(self.SUBMERCHANT_PAY_PRE_PAY_PREPAYID_PATH + f"/{prepayid}",
                               {"waitForFinish": waitForFinish})

    # Create WeChat scan code payment parameters
    # :param  prepayid The number of the pre-paid order obtained by creating the pre-paid order
    # :return mixed
    # :throws VctcException

    def wechatScanPay(self, prepayid):
        return self.CLIENT.post(self.SUBMERCHANT_PAY_WECHAT_PAY_NATIVE_PATH, {}, {"prepayid": prepayid})

    # Create WeChat Mini App Payment Parameters
    # :param  prepayid The number of the pre-paid order obtained by creating the pre-paid order
    # :param  openId The openid of the user who placed the order.For security, openid should be obtained by the backend and not passed to the applet, and the API should also return the result to the frontend applet after the backend call.
    # :return mixed
    # :throws VctcException

    def wechatMiniPay(self, prepayid, openId):
        return self.CLIENT.post(self.SUBMERCHANT_PAY_WECHAT_MINI_PAY_PATH, {}, {"prepayid": prepayid, "openId": openId})

    # Create WeChat App Payment Parameters
    # :param  prepayid The number of the pre-paid order obtained by creating the pre-paid order
    # :param  enableProfitSharing Whether to enable order monetization (Not required parameter). Only the monetized merchants contracted with YuChain support self option, otherwise the setting is invalid if the monetization is opened, the funds of the order will not be directly credited to the account, and the monetization erface needs to be called for subsequent processing
    # :return mixed
    # :throws VctcException

    def wechatAppPay(self, prepayid, enableProfitSharing=False):
        return self.CLIENT.post(self.SUBMERCHANT_PAY_WECHAT_APP_PAY_PATH, {},
                                {"prepayid": prepayid, "enableProfitSharing": enableProfitSharing})

    # Refund erface
    # :param  prepayid The number of the pre-paid order obtained by creating the pre-paid order
    # :return mixed
    # :throws VctcException

    def refund(self, prepayid, logoken):
        return self.CLIENT.post(self.SUBMERCHANT_PAY_REFUND_PATH, {"logoken": logoken}, {"prepayid": prepayid})

    # Set merchant payment parameters
    # :param  id Merchant or sub-merchant number
    # :param  paymentChannel To modify the parameter payment channel, we currently support WechatNative (WeChat payment), WechatUnionPayBizSmall (UnionPay WeChat Mini Program Payment)
    # :param  unionPayBizMchId UnionPay Merchant Number
    # :param  terminalId Payment terminal Id
    # :param  notifyCallbackUrl Payment callback address
    # :return mixed
    # :throws VctcException

    def setPaymentParams(self, id, paymentChannel, unionPayBizMchId, terminalId, notifyCallbackUrl):
        post = {
            "id": id,
            "paymentChannel": paymentChannel,
            "parameters": {
                "unionPayBizMchId": unionPayBizMchId,
                "terminalId": terminalId,
                "notifyCallbackUrl": notifyCallbackUrl
            }
        }
        return self.CLIENT.put(self.MERCHANT_PAYMENT_PARAMS_PATH, {}, post)

    # elligent split erface
    # The specific parameter description of the elligent split-run erface is currently only open to our contracted partners

    # endregion
    # region Trusted Credit Related erface

    # Query trusted credit balance
    # :param  _appId The request appId
    # :param  tokenAppId The appId belonged to when the trusted credit was issued
    # :param  tokenId The id when Trusted Pos was created
    # :param  userAppId The appId of the user whose user balance you want to query
    # :param  userId the id of the appId that the user belongs to (that is, the user id of the developer in his own business system self id does not need to be registered or used on Yulian Cloud in advance)
    # :return mixed
    # :throws VctcException

    def getFungibleTokenBalance(self, _appId, tokenAppId, tokenId, userAppId, userId):
        query = {
            "_appId": _appId,
            "tokenAppId": tokenAppId,
            "tokenId": tokenId,
            "userAppId": userAppId,
            "userId": userId,
        }
        return self.CLIENT.get(self.FUNGIBLE_TOKEN_BALANCE_PATH, query)

    # Generate trusted pos deduction QR code
    # :param  _appId The request appId
    # :param  tokenAppId The appId belonged to when the trusted credit was issued
    # :param  tokenId The id when Trusted Pos was created
    # :param  userAppId The appId of the user whose user balance you want to query
    # :param  userId The id of the appId that the user belongs to (that is, the user id of the developer in his own business system self id does not need to be registered or used on Yulian Cloud in advance)
    # :param  maxAmount The maximum amount that can be deducted for self QR code.Beyond self amount, the chargeback will definitely fail
    # :param  uuid The id on the current payment code chain, a purely random 32-bit number and letter
    # :return mixed
    # :throws VctcException

    def everiPayCode(self, _appId, tokenAppId, tokenId, userAppId, userId, maxAmount, uuid):
        query = {
            "_appId": _appId,
            "tokenAppId": tokenAppId,
            "tokenId": tokenId,
            "userAppId": userAppId,
            "userId": userId,
            "maxAmount": maxAmount,
            "uuid": uuid
        }
        return self.CLIENT.get(self.FUNGIBLE_TOKEN_EVERI_PAY_PATH, query)

    # endregion
    # region Donation donation related erface

    # Create a donation project
    # :param  id Required, the project id of the project can be uniquely found in the database of the project party, please make sure that the id is unique and the project status can be queried
    # :param  createTime Not required, the creation time of the project (UNIX timestamp), please pass it as a value
    # :param  title Not required, project name
    # :param  desc Not required, project description
    # :param  founder Not required, initiator
    # :param  category Not required, project category, please provide as an
    # :param  keyWords Not required, custom keywords, please provide in
    # :param  targetAmount Not required. The target amount must be provided according to self format, which represents the minimum amount (the project is unsuccessful if it is below) and the maximum amount (no more fundraising) there must be at least 2 digits after the decimal
    # :return mixed
    # :throws VctcException

    def createDonationProject(self, id, createTime=None, title="", desc="", founder="", category=[], keyWords=[],
                              targetAmount={}):
        post = {
            "id": id,
            "createTime": createTime,
            "title": title,
            "desc": desc,
            "founder": founder,
            "category": category,
            "keyWords": keyWords,
            "targetAmount": targetAmount

        }
        return self.CLIENT.post(self.CREATE_DONATION_PROJECT_PATH, {}, post)

    # Create a donation for a donation project
    # :param  id Mandatory, the id of the donation record can be uniquely found in the project's database, please ensure that the id is unique and the project status can be queried
    # :param  donatorId Not required, the donor id, which is donated by the same donor multiple times, must be the same here
    # :param  donatorPublicKey It is recommended to transmit, the donor's public key address can be used as a proof of donation. If the donor has some everiToken chip-compatible citizen card and transportation card (such as Jiaxing Hangzhou, etc.), it can also be written directly o the card
    # :param  donatorName Not required, donor name
    # :param |null createTime Not required, donation time (UNIX timestamp), please pass it as a value
    # :param  projectId_biz Not required, the project ID corresponding to the donation, the project must exist
    # :param  projectId_bc Not required,the project ID corresponding to the donation. The API ID can be used to query the on-chain id according to `projectId_biz`.
    # :param  amount Not required money, please be sure to provide it in self format "3000.00 RMB", with 2 digits after the decimal po
    # :return mixed
    # :throws VctcException

    def createDonation(self, id, donatorId="", donatorPublicKey="", donatorName="", createTime=None, projectId_biz="",
                       projectId_bc="", amount=""):
        post = {
            "id": id,
            "donatorId": donatorId,
            "donatorPublicKey": donatorPublicKey,
            "donatorName": donatorName,
            "createTime": createTime,
            "projectId_biz": projectId_biz,
            "projectId_bc": projectId_bc,
            "amount": amount

        }

        return self.CLIENT.post(self.CREATE_DONATION_DONATION_PATH, {}, post)

    # Get  on-chain donation's ID
    # :param  type "project" or "donate"
    # :param  originalIds A list of ids to be queried.Query a maximum of 20 batches at a time
    # :return mixed
    # :throws VctcException

    def fetchDonationOnChainIds(self, type, originalIds={}):
        post = {
            "type": type,
            "originalIds": originalIds
        }

        return self.CLIENT.post(self.CREATE_DONATION_FETCH_ONCHAINIDS_PATH, {}, post)

    # endregion

    # region Captcha  related erface

    # Send SMS verification code
    # :param  items dict Containing following keys
    # :param  phoneNumbers Domestic SMS: 11-digit mobile phone number, such as 15951955195 ernational / Hong Kong, Macao, and Taiwan messages: ernational area code + number, such as 85200000000
    # :param  codeType Verification code type, currently only supports egers
    # :param  code SMS verification code
    # :return mixed
    # :throws VctcException

    def sendSmsCode(self, items):
        itemStruct = {
            "phoneNumbers": "",
            "codeType": "",
            "code": ""
        }
        return self.CLIENT.post(self.SEND_SMS_VERIFICATIONCODE_PATH, {}, {"items": items})

    # endregion

    # region Industry Blockchain Browser Class erface

    # Explore Sign
    # :param  appId Your appId
    # :param  signInOnChainId On-chain ID of the sign-in record
    # :param  signOutOnChainId On-chain Id of checkout record
    # :param  parentOnChainId On-chain Id of activity
    # :return mixed HTML s
    # :throws VctcException

    def commonSignExplorer(self, appId, signInOnChainId="", signOutOnChainId="", parentOnChainId=""):
        item = {
            "appId": appId,
            "signInOnChainId": signInOnChainId,
            "signOutOnChainId": signOutOnChainId,
            "parentOnChainId": parentOnChainId,
        }
        return self.CLIENT.get(self.COMMON_SIGN_EXPLORER_PATH, item)

    # Explore donation
    # :param  appId Your appId
    # :param  projectOnChainId On-chain Id for donation activities
    # :param  donateOnChainId On-chain Id of a donation
    # :return mixed HTML s
    # :throws VctcException

    def donationExplorer(self, appId, projectOnChainId="", donateOnChainId=""):
        item = {
            "appId": appId,
            "projectOnChainId": projectOnChainId,
            "donateOnChainId": donateOnChainId,
        }
        return self.CLIENT.get(self.DONATION_EXPLORER_PATH, item)

    # endregion
    # region Merchant Management erface

    # Merchant To Login
    # :param  userId Merchant number or sub-merchant number to log in
    # :param  pw Password
    # :return mixed
    # :throws VctcException

    def merchantLogin(self, userId, pw):
        item = {
            "userId": userId,
            "pw": pw,
        }
        return self.CLIENT.post(self.MERCHANT_LOGIN_PATH, {}, item)

    # :param  type "subMerchant" or "merchant".Create SubMerchant or merchant.
    # :param  displayName Business display name
    # :param  pw Merchant password
    # :param  disabled Whether to disable the business
    # :param  appId The appId to which self business belongs.The `appId` can be different from the` appId` used for signature. Once the setting cannot be modified, the `appId` will have permission to modify various types of information of` merchant` in the future.
    # :param  parentMerchantId (Passed only when creating a child business) The parent business to which the business belongs
    # :return mixed
    # :throws VctcException

    def createMerchant(self, type, displayName, pw, disabled, appId, parentMerchantId=""):
        item = {
            "type": type,
            "parameters": {
                "displayName": displayName,
                "pw": pw,
                "disabled": disabled,
                "appId": appId,
                "parentMerchantId": parentMerchantId
            }
        }
        return self.CLIENT.post(self.CREATE_MERCHANT_PATH, {}, item)

    # endregion
