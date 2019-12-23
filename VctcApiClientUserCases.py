import unittest
from VctcApiClient import  VctcApiClient


class VctcApiClientUserCases(unittest.TestCase): 
    def tearDown(self):
       pass

    def setUp(self):
       pass

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):
        self.vctcApiClient = VctcApiClient("AzE5", 'u4VcwCrZ0tD$ozhE')

    def test_CommonSignExplorer(self):
        pass

    def test_createMerchant(self):
        re = self.vctcApiClient.createMerchant("merchant", "bgbgbg", "123", False, "555a", "")
        self.assertIsNotNone(re)

    def test_SubmerchantPrePayInfo(self):
        re = self.vctcApiClient.submerchantPrePayInfo("SMFP10293485763", 0)
        self.assertIsNotNone(re)

    def test_CreateDonationProject(self):
        re = self.vctcApiClient.createDonationProject("SMFP10293485763", 0)
        self.assertIsNotNone(re)

    def test_SubmerchantPay(self):
        re = self.vctcApiClient.submerchantPay("SMFP10293485763", 12, "12312423", "bgbbg")
        self.assertIsNotNone(re)

    def test_EveriPay(self):
        itemStruct = {
            "type": "everiPay",
            "args": {
                "id": "123",
                "evtLink": "3123",
                "amount": 12,
                "payee": "2342"
            }
        }
        re = self.vctcApiClient.everiPay([itemStruct])
        self.assertIsNotNone(re)

    def test_Refund(self):
        re = self.vctcApiClient.refund("1231241", "fasfasf")
        self.assertIsNotNone(re)

    def test_WechatMiniPay(self):
        re = self.vctcApiClient.wechatMiniPay("1231241", "fasfasf")
        self.assertIsNotNone(re)

    def test_WechatAppPay(self):
        re = self.vctcApiClient.wechatAppPay("1231241", False)
        self.assertIsNotNone(re)

    def test_FungibleTokenIssue(self):
        itemStruct = {"type": "fungible-token-issue",
                      "args": {
                          "id": "123",
                          "tokenAppId": "123",
                          "tokenId": "123",
                          "userId": "123",
                          "amount": "123",
                          "memo": "123"
                      }}
        re = self.vctcApiClient.fungibleTokenIssue([itemStruct])
        self.assertIsNotNone(re)

    def test_CreateDataitem(self):
        itemStruct = {"type": "data-item-create",
                      "args": {
                          "id": "123",
                          "parentId": "123",
                          "data": [
                              {"key": "123",
                               "type": "13",
                               "value": "2131"
                               }
                          ]}}

        re = self.vctcApiClient.createDataitem([itemStruct])
        self.assertIsNotNone(re)

    def test_UploadCommonChain(self):
        pass

    def test_FetchOnChainIds(self):
        pass

    def test_SendSmsCode(self):
        itemStruct = {
            "phoneNumbers": "13071888562",
            "codeType": "integer",
            "code": "132123"
        }
        re = self.vctcApiClient.sendSmsCode([itemStruct])
        self.assertIsNotNone(re)

    def test_EveriPass(self):
        itemStruct = {
            "type": "everiPass",
            "args": {
                "evtLink": "123",
                "actionMemo": "123"
            }
        }
        re = self.vctcApiClient.everiPass([itemStruct])
        self.assertIsNotNone(re)

    def test_RegisterVoluntaryActivity(self):
        itemStruct = {"type": "voluntary-activity-register",
                      "args": {
                          "id": "123",
                          "createTime": "123",
                          "organizationId": "123",
                          "title": "132",
                          "desc": "132",
                          "organization": "123",
                          "organizationId": "321",
                          "openTime": "132",
                          "closeTime": "312",
                          "district": "312",
                          "address": "13",
                          "memo": "31",
                          "categories": [],
                          "x": [],
                      }}
        re = self.vctcApiClient.registerVoluntaryActivity([itemStruct])
        self.assertIsNotNone(re)

    def test_RegisterDataBucket(self):
        itemStruct = {"type": "data-bucket-register", "args": {"id": "123"}}
        re = self.vctcApiClient.registerDataBucket([itemStruct])
        self.assertIsNotNone(re)

    def test_RegisterFungibleTokenSymbol(self):
        itemStruct = {
            "type": "fungible-token-symbol-register",
            "args": {
                "id": "123",
                "name": "123",
                "fullName": "123",
                "totalSupply": "312",
                "precision": 5,
                "icon": "321"
            }
        }
        re = self.vctcApiClient.registerFungibleTokenSymbol([itemStruct])
        self.assertIsNotNone(re)

    def test_GetSignature(self):
        pass

    def test_EveriPayCode(self):
        re = self.vctcApiClient.everiPayCode("123", "123", "123", "123", "123", "123", "123")
        self.assertIsNotNone(re)

    def test_GetFungibleTokenBalance(self):
        re = self.vctcApiClient.getFungibleTokenBalance("123", "123", "123", "123", "123")
        self.assertIsNotNone(re)

    def test_SignVoluntaryActivity(self):
        itemStruct = {"type": "voluntary-activity-signIn",
                      "args": {
                          "id": "123",
                          "parentId": "123",
                          "userId": "123",
                          "durationInMinutes": "123",
                          "memo": "123",
                          "createTime": "123",
                          "x": {
                              "signerName": "133",
                              "gps": [],
                          }
                      }
                      }
        re = self.vctcApiClient.signVoluntaryActivity([itemStruct])
        self.assertIsNotNone(re)

    def test_WechatScanPay(self):
        re = self.vctcApiClient.wechatScanPay("q34eqw")
        self.assertIsNotNone(re)

    def test_CreateDonation(self):
        re = self.vctcApiClient.createDonation("q34eqw", "q34eqw", "q34eqw", "q34eqw", 123, "q34eqw", "q34eqw",
                                               "q34eqw")
        self.assertIsNotNone(re)

    def test_FetchDonationOnChainIds(self):
        re = self.vctcApiClient.fetchDonationOnChainIds("q34eqw", {"1231", "12314"})
        self.assertIsNotNone(re)

    def test_MerchantLogin(self):
        re = self.vctcApiClient.merchantLogin("q34eqw", "34234")
        self.assertIsNotNone(re)

    def test_RegisterIntelligentDoorlock(self):
        itemStruct = {
            "type": "intelligent-doorlock-register",
            "args": {
                "id": "rrrrr",
                "ownerUserId": "qwewqeq",
                "memo": ""
            }
        }
        re = self.vctcApiClient.registerIntelligentDoorlock([itemStruct])
        self.assertIsNotNone(re)

    def test_SetPaymentParams(self):
        re = self.vctcApiClient.setPaymentParams("qweq", "efwa", "efwa", "efwa", "weqw")
        self.assertIsNotNone(re)

    def test_TransferFungibleToken(self):
        itemStruct = {
            "type": "fungible-token-transfer",
            "args": {
                "id": "wrerwerwrew",
                "tokenAppId": "ewqeqw",
                "tokenId": "wqeeq",
                "fromUserId": "eqw",
                "toUserAppId": "eqw",
                "toUserId": "eqw",
                "amount": 123,
                "memo": "3qweqw"
            }
        }
        re = self.vctcApiClient.transferFungibleToken([itemStruct])
        self.assertIsNotNone(re)

    def test_ModelIntelligentDoorlock(self):
        itemStruct = {"type": "intelligent-doorlock-model", "args": {"id": "fdasfdafda"}}
        re = self.vctcApiClient.modelIntelligentDoorlock([itemStruct])
        self.assertIsNotNone(re)

    def test_DonationExplorer(self):
        pass


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
