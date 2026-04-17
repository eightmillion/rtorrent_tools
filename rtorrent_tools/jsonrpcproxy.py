import requests
import uuid
import xmlrpc.client
import json
import logging
from urllib.parse import urlsplit, urlunsplit
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("JsonRpcProxy")


class JsonRpcProxy:
    """
    A drop-in JSON-RPC replacement for xmlrpc.client.ServerProxy.
    Supports rTorrent dotted names, native batches, and system.multicall().
    """

    def __init__(self, url, method_name=None, timeout=30, verify=True,
                 verbose=False, retries=3):
        parsed = urlsplit(url)
        self.__dict__['_auth'] = None
        if parsed.username and parsed.password:
            self.__dict__['_auth'] = (parsed.username, parsed.password)

        # Build clean URL
        netloc = parsed.hostname
        if parsed.port:
            netloc += f":{parsed.port}"
        self.__dict__['_url'] = urlunsplit((
            parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment
        ))

        self.__dict__['_method_name'] = method_name
        self.__dict__['_timeout'] = timeout
        self.__dict__['_verify'] = verify
        self.__dict__['_verbose'] = verbose

        # Setup Session with Retry Strategy
        self.__dict__['_session'] = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

    @property
    def multicall(self):
        if self._method_name:
            return self.__getattr__('multicall')
        return JsonRpcMultiCall(self)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        full_name = f"{self._method_name}.{name}" if self._method_name else name
        child = JsonRpcProxy(
            self._url, full_name, timeout=self._timeout,
            verify=self._verify, verbose=self._verbose
        )
        child.__dict__['_session'] = self._session
        child.__dict__['_auth'] = self._auth
        return child

    def __call__(self, *args):
        # 1. Prepare the Payload
        # Intercept manual system.multicall(list_of_structs) for compatibility
        if self._method_name == "system.multicall" and args:
            calls = args[0] if isinstance(args[0], list) else list(args)
            payload = [
                {
                    "jsonrpc": "2.0",
                    "method": c.get('methodName'),
                    "params": c.get('params', []),
                    "id": str(uuid.uuid4())
                } for c in calls
            ]
        else:
            if not self._method_name:
                raise TypeError("Proxy not callable at root")
            payload = {
                "jsonrpc": "2.0",
                "method": self._method_name,
                "params": list(args),
                "id": str(uuid.uuid4())
            }

        if self._verbose:
            logger.info(f"REQ: {json.dumps(payload)}")

        # 2. Execute the Request
        try:
            resp = self._session.post(
                self._url, 
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self._timeout, 
                auth=self._auth, 
                verify=self._verify
            )
            # Raise an exception for 4xx or 5xx status codes
            resp.raise_for_status()
            data = resp.json()
            
        except requests.exceptions.HTTPError as e:
            # Map HTTP errors to native xmlrpc.client.ProtocolError
            raise xmlrpc.client.ProtocolError(
                self._url,
                e.response.status_code,
                e.response.reason,
                e.response.headers
            ) from None
        except Exception as e:
            # Handle connection timeouts, DNS issues, etc.
            raise xmlrpc.client.ProtocolError(
                    self._url, 500, str(e), {}) from None

        # 3. Handle the Response Data
        # Handle Batch Responses (system.multicall compatibility)
        if isinstance(data, list):
            res_map = {r['id']: r for r in data}
            results = []
            for q in (payload if isinstance(payload, list) else [payload]):
                r = res_map.get(q['id'])
                if not r:
                    results.append([None])
                elif "error" in r:
                    err = r["error"]
                    # Map batch errors to Fault objects inside the list
                    results.append(xmlrpc.client.Fault(
                        err.get("code", 1), err.get("message", "")))
                else:
                    # XML-RPC multicall returns results wrapped in a single-item list
                    results.append([r.get("result")])
            return results

        # Handle Single Response Errors
        if "error" in data:
            err = data["error"]
            raise xmlrpc.client.Fault(
                err.get('code', 1), 
                err.get('message', 'Unknown Error')
            )

        return data.get("result")


class JsonRpcMultiCall:

    def __init__(self, server_proxy):
        self._url = server_proxy._url
        self._session = server_proxy._session
        self._timeout = server_proxy._timeout
        self._auth = server_proxy._auth
        self._verify = server_proxy._verify
        self._verbose = server_proxy._verbose
        self._calls = []

    def _add_call(self, method, params):
        self._calls.append({
            "jsonrpc": "2.0", "method": method,
            "params": list(params), "id": str(uuid.uuid4())
        })

    def __getattr__(self, name):
        return JsonRpcMultiCallChild(self, name)

    def _MultiCall__call_list(self, call_list):
        """
        Internal xmlrpc.client compatibility method.
        Accepts a list of tuples/lists: [('methodName', (params,)), ...]
        """
        for method_name, params in call_list:
            self._add_call(method_name, params)
        return self()

    def __call__(self):
        if not self._calls:
            return []
        try:
            resp = self._session.post(
                self._url, json=self._calls,
                headers={'Content-Type': 'application/json'},
                timeout=self._timeout, auth=self._auth, verify=self._verify
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise xmlrpc.client.ProtocolError(
                    self._url, 500, str(e), {}) from None

        res_map = {r['id']: r for r in data}
        final = []
        for q in self._calls:
            r = res_map.get(q['id'])
            if r and "error" in r:
                final.append(xmlrpc.client.Fault(
                    r["error"].get("code", 1), r["error"].get("message", "")))
            else:
                final.append(r.get("result") if r else None)
        self._calls = []
        return final


class JsonRpcMultiCallChild:
    
    def __init__(self, parent, method_path):
        self.parent = parent
        self.method_path = method_path

    def __getattr__(self, name):
        return JsonRpcMultiCallChild(self.parent, f"{self.method_path}.{name}")

    def __call__(self, *args):
        self.parent._add_call(self.method_path, args)
        return None

