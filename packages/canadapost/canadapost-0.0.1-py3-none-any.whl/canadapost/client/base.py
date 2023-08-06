from lxml import etree
from ..exceptions import (
    CanadaPostException,
    CanadaPostThrottleException
)

from ..objects.base import remove_xmlns


class Client(object):

    def __init__(
        self,
        url,
        username,
        password,
        customer_no=None,
        accept_language='en-CA'
    ):
        self.url = url
        self.username = username
        self.password = password
        self.customer_no = customer_no
        self.accept_language = accept_language

    def make_url(self, request):
        params = request.params

        if params is None:
            params = {}
        else:
            params = params.copy()

        if 'mobo' not in params:
            params['mobo'] = self.customer_no

        params['customer_no'] = self.customer_no

        url = request.path % params

        return "%s%s" % (
            self.url,
            url
        )

    def map_server_error(self, content):
        tree = etree.fromstring(content)
        # ns = {
        #    "cp": "http://www.canadapost.ca/ws/messages"
        # }

        remove_xmlns(tree)

        code = tree.xpath('//message/code')[0].text
        description = tree.xpath('//message/description',)[0].text

        if code == 'server':
            raise CanadaPostThrottleException(code, description)
        else:
            raise CanadaPostException(code, description)
