from ..https import Methods
from .base import Client
import requests


class SyncClient(Client):

    def send_request(self, request):
        url = self.make_url(request)

        if request.method == Methods.POST:
            req = requests.post(
                url,
                params=request.params,
                data=request.data,
                headers=request.headers,
                auth=(self.username, self.password)
            )
        elif request.method == Methods.GET:
            req = requests.get(
                url,
                params=request.params,
                # data=request.data,
                headers=request.headers,
                auth=(self.username, self.password)
            )

        print(url)

        if req.status_code != 200:
            return self.map_server_error(req.content)

        return request.map(req.content)
