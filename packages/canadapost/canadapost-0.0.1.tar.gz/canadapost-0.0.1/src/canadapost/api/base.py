from lxml import etree
from ..https import Methods
from ..objects.base import remove_xmlns


class Request(object):
    def __init__(self, path, headers, params, map_method, data=None, method=None):
        self.path = path
        self.headers = headers
        self.params = params
        self.data = data
        self.method = method
        self.map_method = map_method

    def map(self, content):
        return self.map_method(content)


class BaseApi(object):
    def __init__(self, client):
        self.client = client

    def make_ns(self, ns):
        return {
            "cp": ns
        }

    def val(self, data, xpath, ns):
        return self.elems(data, xpath, ns)[0].text

    def elems(self, data, xpath, ns):
        return data.xpath(xpath, namespaces=ns)

    def parse_xml(self, data):
        node = etree.fromstring(data)
        remove_xmlns(node)
        return node


def make_ns(namespace):
    return {
        'cp': namespace
    }


def method(
    path=None,
    content_type=None,
    xmlns=None,
    method=Methods.GET,
    headers=None,
    **kw
):
    if headers is None:
        headers = {}

    if content_type:
        headers['Content-Type'] = content_type
        headers['Accept'] = content_type

    if xmlns:
        namespace = make_ns(xmlns)
        kw['ns'] = namespace
    else:
        namespace = None

    def wrap(func):
        def _inner(self, data=None, params=None, **kwargs):
            """
            The actual method being called when wrapping the methods of
            the class.

            Attributes:

            self (Api): The API class being passed
            obj (string): xml data being passed for post requests
            params (dict): key/value container for GET params
            """

            if params is None:
                params = {}
            else:
                params = params.copy()

            params.update(kwargs)

            def handle_result_proxy(content):
                return func(self, content, **kw.copy())

            request = Request(
                path=path,
                headers=headers,
                data=data,
                params=params,
                method=method,
                map_method=handle_result_proxy
            )

            # Pass the request to the client and return the response
            return self.client.send_request(request)
        return _inner
    return wrap
