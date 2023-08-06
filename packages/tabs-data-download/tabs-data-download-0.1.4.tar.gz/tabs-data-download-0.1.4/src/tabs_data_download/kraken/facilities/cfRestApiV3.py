import base64
import hashlib
import hmac
import ssl
import time
import urllib.parse as urllib
import urllib.request as urllib2

import ujson
from tabs_settings.config.asset_type import AssetType
from tabs_settings.config.trading_pair import TradingPair


class cfApiMethods(object):
    def __init__(
        self,
        apiPath,
        apiPublicKey="",
        apiPrivateKey="",
        timeout=10,
        checkCertificate=True,
        useNonce=False,
    ):
        self.apiPath = apiPath
        self.apiPublicKey = apiPublicKey
        self.apiPrivateKey = apiPrivateKey
        self.timeout = timeout
        self.nonce = 0
        self.checkCertificate = checkCertificate
        self.useNonce = useNonce

    ##### public endpoints #####

    # returns market data for all instruments
    def get_tickers(self):
        endpoint = "/derivatives/api/v3/tickers"
        return self.make_request("GET", endpoint)

    def _get_partial_historical_elements(self, elementType: str, **params):
        params = {k: v for k, v in params.items() if v is not None}
        postUrl = urllib.urlencode(params)
        return self.make_request_raw("GET", elementType, postUrl)

    def _get_historical_elements(
        self,
        elementType: str,
        trading_pair: TradingPair,
        since: int,
        before: int,
        sort: str | None = None,
        limit: int = 1000,
    ):
        elements = []
        continuationToken = None
        while True:
            res = self._get_partial_historical_elements(
                elementType,
                since=since,
                before=before,
                sort=sort,
                continuationToken=continuationToken,
                pair=trading_pair.exchange_name,
            )

            body = ujson.loads(res.read().decode("utf-8"))
            if "elements" in body:
                # future case
                elements = elements + body["elements"]

                if (
                    res.headers["is-truncated"] is None
                    or res.headers["is-truncated"] == "false"
                ):
                    continuationToken = None
                    break
                else:
                    continuationToken = res.headers["next-continuation-token"]

            elif "result" in body:
                # spot case
                elements = elements + body["result"][trading_pair.exchange_name]
                last = body["result"]["last"]  # given as str nanoseconds
                last = int(int(last) / 10**9)  # before is given with second precision
                if last >= before:
                    # timestamp is in 3rd position
                    elements = [e for e in elements if e[2] < before]
                    break
                else:
                    since = last

            if len(elements) >= limit:
                elements = elements[:limit]
                break
        return elements

    def get_executions(
        self,
        asset_type: AssetType,
        since: int,
        before: int,
        sort=None,
        limit=1000,
    ):
        """
        Retrieves executions of your account. With default parameters it gets the 1000
        newest executions.

        :param since: Timestamp in milliseconds. Retrieves executions starting at this
            time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """

        return self._get_historical_elements(
            "executions", asset_type, since, before, sort, limit
        )

    def get_market_executions(
        self,
        trading_pair: TradingPair,
        since: int,
        before: int,
        sort: str | None = None,
        limit: int = 1000,
    ) -> list | None:
        """
        Retrieves executions of given trading_pair. With default parameters it gets the
        1000 newest executions.

        :param trading_pair: Name of a trading_pair. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves executions starting at this
            time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """
        if trading_pair.asset_type is AssetType.SPOT:
            return self._get_historical_elements(
                "/0/public/Trades",
                trading_pair,
                since,
                before,
                sort,
                limit,
            )
        elif trading_pair.asset_type is AssetType.FUTURE:
            return self._get_historical_elements(
                "/api/history/v2/market/" + trading_pair.exchange_name + "/executions",
                trading_pair,
                since,
                before,
                sort,
                limit,
            )

    # signs a message
    def sign_message(self, endpoint, postData, nonce=""):
        if endpoint.startswith("/derivatives"):
            endpoint = endpoint[len("/derivatives") :]

        # step 1: concatenate postData, nonce + endpoint
        message = postData + nonce + endpoint

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode("utf8"))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secretDecoded = base64.b64decode(self.apiPrivateKey)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secretDecoded, hash_digest, hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64encode(hmac_digest)

    # creates a unique nonce
    def get_nonce(self):
        # https://en.wikipedia.org/wiki/Modulo_operation
        self.nonce = (self.nonce + 1) & 8191
        return str(int(time.time() * 1000)) + str(self.nonce).zfill(4)

    # sends an HTTP request
    def make_request_raw(self, requestType, endpoint, postUrl="", postBody=""):
        # create authentication headers
        postData = postUrl + postBody

        if self.useNonce:
            nonce = self.get_nonce()
            signature = self.sign_message(endpoint, postData, nonce=nonce)
            authentHeaders = {
                "APIKey": self.apiPublicKey,
                "Nonce": nonce,
                "Authent": signature,
            }
        else:
            signature = self.sign_message(endpoint, postData)
            authentHeaders = {"APIKey": self.apiPublicKey, "Authent": signature}

        authentHeaders["User-Agent"] = "cf-api-python/1.0"

        # create request
        if postUrl != "":
            url = self.apiPath + endpoint + "?" + postUrl
        else:
            url = self.apiPath + endpoint

        request = urllib2.Request(url, str.encode(postBody), authentHeaders)
        request.get_method = lambda: requestType

        # read response
        if self.checkCertificate:
            response = urllib2.urlopen(request, timeout=self.timeout)
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib2.urlopen(request, context=ctx, timeout=self.timeout)

        return response

    # sends an HTTP request and read response body
    def make_request(self, requestType, endpoint, postUrl="", postBody=""):
        return (
            self.make_request_raw(requestType, endpoint, postUrl, postBody)
            .read()
            .decode("utf-8")
        )
