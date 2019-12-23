import json
from VctcExceptions import VctcException
import requests
import datetime
import hmac
import hashlib
from urllib.parse import urlencode

requests.adapters.DEFAULT_RETRIES = 1


class VctcClient:
    test=""
    def __init__(self, apiPrefix, appId, appSecret):
        self.apiPrefix = apiPrefix
        self.appId = appId
        self.appSecret = appSecret

    def post(self, path, query, body):
        return self.request("POST", path, query, body)
    def get(self, path, query):
        return self.request("GET", path, query, {})
    def put(self, path, query, body):
        return self.request("PUT", path, query, body)
    def delete(self, path, query):
        return self.request("PUT", path, query, {})


     #  Request http api
     # :param method string Method of requesting http
     # :param path string  Path of requesting http
     # :param query dict Query of requesting http
     # :param body dict Body of requesting http
     # :return mixed
     # :throws VctcException

    def request(self, method, path, query, body):
        try:
            query=self.fliterParams(query)
            body=self.fliterParams(body)
            signatures = self.getSignature(method, path, query, body)
            headers = {}
            headers["Content-Type"] = "application/json"
            headers["User-Agent"] = "vctc-sdk/python Version=0.0.1"
            re = requests.request(
                method,
                self.apiPrefix + path + "?" + urlencode(
                    [(k, signatures["fullQueries"][k]) for k in sorted(signatures["fullQueries"].keys())]),
                json=body,
                headers=headers,
                timeout=3

            )
            res=json.loads(re.content);
            if res["error"]:
                raise VctcException(res['error'] + ": " + res['msg'],res["code"])
            return res
        except Exception as e:
            raise e
        finally:
            pass

    def getSignature(self, method, path, query, body):
        if body and not isinstance(body, str):
            body = json.dumps(body)
        if not path:
            raise ("invalid path")

        if (method != "GET" and method != "POST" and method != "DELETE" and method != "PUT"):
            raise ("invalid method, only GET, POST, DELETE and PUT is supported");

        textForSigning = method + " " + path + "\n"

        if not query:
            query = {};

        query["_appid"] = self.appId;
        query["_t"] = int(datetime.datetime.now().timestamp()/10) * 10000
        queryStr = urlencode([(k, query[k]) for k in sorted(query.keys())])
        textForSigning += queryStr

        if body:
            textForSigning += "\n" + body

        query["_s"] = hmac.new(self.appSecret.encode('utf-8'), textForSigning.encode('utf-8'), 'sha256').hexdigest()
        self.test+=textForSigning
        self.test+=str(query["_t"])
        self.test+=query["_s"]
        return {
            "fullQueries": query,
            "signature": query["_s"],
            "timestamp": query["_t"]
        }

     # Filter parameters with empty  values
     # @param dict kv Parameters to Filter
    def fliterParams(self,kv):
        for k in list(kv.keys()):
            if not kv[k]:
                del kv[k]
            elif  isinstance (kv[k],dict) :
                kv[k]=self.fliterParams(kv[k])
            elif isinstance (kv[k],list) :
                for i in range(0,len(kv[k])):
                    if isinstance (kv[k][i],dict):
                        temp=self.fliterParams(kv[k][i])
                        if temp:
                            kv[k][i]=temp
                        else:
                            del kv[k][i]


        return  kv


